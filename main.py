# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python
import json
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ['https://www.googleapis.com/auth/youtube.readonly']


def youtube_init(debug=False, with_oauth=False):
	# Disable OAuthlib's HTTPS verification when running locally.
	# *DO NOT* leave this option enabled in production.
	if not debug:
		os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
	api_service_name = 'youtube'
	api_version = 'v3'

	if with_oauth:
		client_secrets_file = './secure/client_secret_657237296259-obte2mu832ld7trllc5qnn76qf8t9bro.apps.googleusercontent.com.json'


		# Get credentials and create an API client
		flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
		credentials = flow.run_console()
		return googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)
	else:
		DEVELOPER_KEY = open('./secure/api_key.txt', 'r').read()
		return googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)


def channel_list(user_id, debug=False):
	youtube = youtube_init(debug=debug)

	request = youtube.channels().list(
		part='brandingSettings,status,statistics,snippet,topicDetails',
		channelId=user_id
	)
	response = request.execute()

	print(response)
	with open(f'channel_list_{user_id}.json', 'w', encoding='utf8') as out:
		json.dump(response, out, indent=2, ensure_ascii=False)


def activities(user_id, debug=False):
	youtube = youtube_init(debug=debug)
	request = youtube.activities().list(
		part='contentDetails,snippet',
		channelId=user_id
	)
	response = request.execute()

	print(response)
	with open(f'activities_{user_id}.json', 'w', encoding='utf8') as out:
		json.dump(response, out, indent=2, ensure_ascii=False)


def video_info(video_id, debug=False):
	youtube = youtube_init(debug=debug)
	request = youtube.videos().list(
		part='contentDetails,snippet,statistics',
		id=video_id
	)
	response = request.execute()

	print(response)
	with open(f'video_info_{video_id}.json', 'w', encoding='utf8') as out:
		json.dump(response, out, indent=2, ensure_ascii=False)


if __name__ == "__main__":
	user_id = 'UCMCgOm8GZkHp8zJ6l7_hIuA'
	video_id = 'XFqayVEIJwE'
	activities(user_id, debug=True)
	video_info(video_id, debug=True)
