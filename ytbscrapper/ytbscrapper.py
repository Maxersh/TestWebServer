'''
Python Client Docs
https://github.com/googleapis/google-api-python-client/blob/master/docs

Youtube API Docs
https://developers.google.com/youtube/v3/docs
'''
import os
import json
import datetime as DT
import googleapiclient.discovery
from ytbscrapper.securetransport import SecureTransport

def get_video_info(youtube, video_ids):
    data = {}
    count = 0
    part_videos = ['snippet', 'statistics']
    while True:
        slice = video_ids[count*50:count*50+50]
        if not slice:
            break
        count += 1
        request = youtube.videos().list(
            part=part_videos,
            id=slice,
            maxResults=50,
        )
        response = request.execute()
        for item in response['items']:
            id = item['id']
            date = item['snippet']['publishedAt']
            if 'tags' in item['snippet']:
               tags = item['snippet']['tags']
            else:
                tags = []
            view = int(item['statistics']['viewCount'])
            like = int(item['statistics']['likeCount'])
            comment = int(item['statistics']['commentCount'])
            dct = {
                'date': date,
                'view': view,
                'like': like,
                'comment': comment,
                'tags': tags
            }
            data[id] = dct
    return data

def get_channel_info(youtube, channel_id):
    request = youtube.channels().list(
        part='contentDetails',
        id=channel_id
    )
    try:
        response = request.execute()
    except Exception as ex:
        print(ex)
    uploads = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    return uploads

def get_video_ids(youtube, uploads):
    next_page_token = ''
    video_id_list = []
    while True:
        request = youtube.playlistItems().list(
            part='snippet',
            playlistId=uploads,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()
        for item in response['items']:
            video_id_list.append(item['snippet']['resourceId']['videoId'])
        if 'nextPageToken' in response:
            next_page_token = response['nextPageToken']
        else:
            break

    return video_id_list

def get_info(channel_id, path=''):
    secure = SecureTransport()
    secure.disable()
    now = DT.datetime.now()
    now_str = DT.datetime.strftime(now, "%Y-%m-%dT%H-%M-%SZ")
    if not path:
        path = 'C:\\Users\\d.abramov\\PycharmProjects' \
           '\\WebScrappingYoutube\\'
    video_path = 'video_ids_{}_{}.json'.format(now_str, channel_id)
    info_path = 'video_info_{}_{}.json'.format(now_str, channel_id)
    API_KEY = "AIzaSyASBeMw6E_uKXocqyBBydhzgrzM6Cq9dbQ"
    api_service_name = 'youtube'
    api_version = 'v3'
    file_name_video_ids = path + video_path
    file_name_info = path + info_path
    # Create an API client
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=API_KEY)

    # Create video ids file
    if not os.path.isfile(file_name_video_ids):
        uploads = get_channel_info(youtube, channel_id=channel_id)
        video_id_list = get_video_ids(youtube, uploads)
        with open(file_name_video_ids, 'w', encoding='utf-8') as file:
            json.dump(video_id_list, file, indent=2, ensure_ascii=False)

    with open(file_name_video_ids, 'r') as file:
        video_ids = json.load(file)

    # Create info dict file
    if not os.path.isfile(file_name_info):
        dct = get_video_info(youtube, video_ids)
        with open(file_name_info, 'w') as file:
            json.dump(dct, file, indent=2, ensure_ascii=False)

    secure.enable()
    return file_name_video_ids, file_name_info
