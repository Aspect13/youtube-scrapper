# -*- coding: utf-8 -*-

# https://developers.google.com/youtube/v3
# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python
import json
import os
from pathlib import Path

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from settings import API_KEY_PATH, OUTPUT_PATH

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
		DEVELOPER_KEY = open(API_KEY_PATH, 'r').read()
		return googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)


def channel_list(channel_id, debug=False, youtube=None):
	if not youtube:
		youtube = youtube_init(debug=debug)

	request = youtube.channels().list(
		part='brandingSettings,status,statistics,snippet,topicDetails',
		id=channel_id
	)
	response = request.execute()
	return response


def activities(user_id, debug=False, youtube=None):
	if not youtube:
		youtube = youtube_init(debug=debug)
	request = youtube.activities().list(
		part='contentDetails,snippet',
		channelId=user_id
	)
	response = request.execute()
	return response


def video_info(video_id, debug=False, youtube=None):
	if not youtube:
		youtube = youtube_init(debug=debug)
	request = youtube.videos().list(
		part='contentDetails,snippet,statistics',
		id=video_id
	)
	response = request.execute()
	return response


def dump_to_json(name, data):
	with open(Path(OUTPUT_PATH, f'{name}.json'), 'w', encoding='utf8') as out:
		json.dump(data, out, indent=2, ensure_ascii=False)
