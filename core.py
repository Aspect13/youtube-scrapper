from bson import DBRef, ObjectId
from pymongo.errors import DuplicateKeyError

from yt_api import get_channel_list, get_activities, get_video_info

from settings import LESS_TRANSACTIONS


def store_channel_data(collection, channel_id, youtube=None):
	data = collection.find_one({'id': channel_id}, {})
	if data:
		print('Channel {} already exists'.format(channel_id))
		return data['_id']
	else:
		data = get_channel_list(channel_id, youtube=youtube)['items'][0]
		return collection.insert_one(data).inserted_id


def _get_ref(collection, ref_id):
	return DBRef(collection=collection, id=ObjectId(ref_id), database='youtube')


def store_activities_data(collection, channel_id, ref_id, page_token=None, youtube=None, other_activities_collection=None):
	print('Storing activities for channel {} on page {}'.format(channel_id, page_token if page_token else 'start'))
	# ref_name = 'db_channel'
	# ref_value = _get_ref('channels', ref_id)
	ref_name = 'db_channel'
	ref_value = ref_id
	activities = get_activities(channel_id, youtube=youtube, next_page_token=page_token)
	next_page_token = activities.get('nextPageToken')
	if LESS_TRANSACTIONS:
		new_activities = []
		while activities['items']:
			activity = activities['items'].pop()
			try:
				video_id = activity['contentDetails']['upload']['videoId']
				data = collection.find_one({'contentDetails.upload.videoId': video_id}, {})
				if data:
					print('Activity for video {} is already in database'.format(video_id))
					continue
				else:
					activity[ref_name] = ref_value
					new_activities.append(activity)
			except KeyError:
				if other_activities_collection:
					activity[ref_name] = ref_value
					other_activities_collection.insert_one(activity)
		if new_activities:
			collection.insert_many(new_activities)
	else:
		for activity in activities['items']:
			activity[ref_name] = ref_value
			try:
				collection.insert_one(activity)  # try except unique
			except DuplicateKeyError:
				pass

	if next_page_token:
		store_activities_data(collection, channel_id, ref_id, page_token=next_page_token, youtube=youtube)


def store_videos_data(db, limit=50):
	print('Saving videos...')
	page = 0
	while True:
		query = db.activities.find({}, {'contentDetails.upload.videoId'}).skip(page*limit).limit(limit)
		query_count = query.count(True)
		print('Found {} videos on page {}'.format(query_count, page))
		if not query_count:
			break
		video_ids = set(map(lambda x: x['contentDetails']['upload']['videoId'], query))

		# tmp = 1
		# for i in video_ids:
		# 	print(tmp + page * limit, i)
		# 	tmp += 1

		if LESS_TRANSACTIONS:
			existent = set(map(lambda x: x['id'], db.videos.find({'id': {'$in': list(video_ids)}}, {'id'})))
			video_ids = video_ids ^ existent
			print('{} are new'.format(len(video_ids)))

		if video_ids:
			print('Making request to api...')
			video_data = get_video_info(video_ids)
			print('Saving to mongo...')
			if LESS_TRANSACTIONS:
				db.videos.insert_many(video_data['items'])
			else:
				for video in video_data['items']:
					try:
						db.videos.insert_one(video)  # try except unique
					except DuplicateKeyError:
						pass
		if query_count < limit:
			break
		page += 1
