# -*- coding: utf-8 -*-

# https://developers.google.com/youtube/v3
# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python
# import asyncio
import json
import os
from collections import Iterable
from pathlib import Path

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from settings import API_KEY_PATH, OUTPUT_PATH, CLIENT_SECRET_PATH, USE_OAUTH

scopes = ['https://www.googleapis.com/auth/youtube.readonly']


def youtube_init(debug=False):
	# Disable OAuthlib's HTTPS verification when running locally.
	# *DO NOT* leave this option enabled in production.
	if not debug:
		os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
	api_service_name = 'youtube'
	api_version = 'v3'

	if USE_OAUTH:
		client_secrets_file = CLIENT_SECRET_PATH

		# Get credentials and create an API client
		flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
		credentials = flow.run_console()
		return googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)
	else:
		DEVELOPER_KEY = open(API_KEY_PATH, 'r').read()
		return googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)


def get_channel_list(channel_id, debug=False, youtube=None):
	if not youtube:
		youtube = youtube_init(debug=debug)

	request = youtube.channels().list(
		part='brandingSettings,status,statistics,snippet,topicDetails',
		id=channel_id
	)
	response = request.execute()
	return response


def get_activities(channel_id, debug=False, youtube=None, max_results=50, next_page_token=None):
	if not youtube:
		youtube = youtube_init(debug=debug)

	kwargs = {
		'part': 'contentDetails',
		'channelId': channel_id,
		'maxResults': max_results
	}
	if next_page_token:
		kwargs['pageToken'] = next_page_token

	request = youtube.activities().list(**kwargs)
	response = request.execute()
	return response


def get_video_info(video_ids, debug=False, youtube=None, max_results=50, next_page_token=None):
	if not isinstance(video_ids, str) and isinstance(video_ids, Iterable):
		ids = ','.join(video_ids)
	else:
		ids = video_ids
	if not youtube:
		youtube = youtube_init(debug=debug)

	kwargs = {
		'part': 'contentDetails,snippet,statistics',
		'id': ids,
		'maxResults': max_results
	}
	if next_page_token:
		kwargs['pageToken'] = next_page_token

	request = youtube.videos().list(**kwargs)
	response = request.execute()
	return response


def get_search_videos(channel_id, debug=False, youtube=None, max_results=50, next_page_token=None):
	if not youtube:
		youtube = youtube_init(debug=debug)
	kwargs = {
		'part': 'snippet,statistics',
		'channelID': channel_id,
		'maxResults': max_results
	}
	if next_page_token:
		kwargs['pageToken'] = next_page_token

	request = youtube.search().list(**kwargs)
	response = request.execute()
	return response


def dump_to_json(name, data):
	with open(Path(OUTPUT_PATH, f'{name}.json'), 'w', encoding='utf8') as out:
		json.dump(data, out, indent=2, ensure_ascii=False)
