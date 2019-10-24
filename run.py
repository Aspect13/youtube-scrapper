from pymongo import MongoClient

from settings import MONGO_CONNECTION_STRING_PATH
from yt_api import youtube_init
from core import store_channel_data, store_activities_data, store_videos_data


def main(channel_ids):
	connection_string = open(MONGO_CONNECTION_STRING_PATH, 'r').read()
	client = MongoClient(connection_string)
	db = client.youtube

	yt_instance = youtube_init(debug=True)
	for channel_id in channel_ids:
		try:
			channel_db_id = store_channel_data(db.channels, channel_id, youtube=yt_instance)
		except IndexError:
			print('Channel {} does not exist'.format(channel_id))
			continue
		store_activities_data(
			db.activities,
			channel_id,
			channel_db_id,
			youtube=yt_instance,
			other_activities_collection='activities_other'
		)
	store_videos_data(db)


if __name__ == '__main__':
	channel_ids = [
		'UCMCgOm8GZkHp8zJ6l7_hIuA',
	]
	main(channel_ids)
