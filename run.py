from main import channel_list, activities, video_info, dump_to_json

if __name__ == '__main__':
	channel_id = 'UCMCgOm8GZkHp8zJ6l7_hIuA'
	video_id = '7JrIAY5G7jE'
	dump_to_json(
		f'channel_list_{channel_id}',
		channel_list(channel_id, debug=True)
	)
	dump_to_json(
		f'activities_{channel_id}',
		activities(channel_id, debug=True)
	)
	dump_to_json(
		f'video_info_{video_id}',
		video_info(video_id, debug=True)
	)

