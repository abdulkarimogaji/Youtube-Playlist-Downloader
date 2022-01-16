from googleapiclient.discovery import build


api_key = 'AIzaSyB7YZcm-TbNDWiti4O7VV9bjLQGciTyDpU'

youtube = build('youtube', 'v3', developerKey=api_key)
PLAYLIST_ID = 'PLLAZ4kZ9dFpMGXTKXsBM_ZNpJwowfsP49'


def get_title_and_link(playlist_id, token=''):
    titles = []
    while True:
        request = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            pageToken=token
        )
        response = request.execute()

        for item in response['items']:
            titles.append((item['snippet']['title'], item['snippet']['resourceId']['videoId']))

        try:
            token = response['nextPageToken']
        except KeyError:
            break
        else:
            continue
    return titles


def get_download_links():
    for title, videoId in get_title_and_link(PLAYLIST_ID):
        # use video Id to generate url that is going to ssYoutube.com
        url = f'https://www.ssyoutube.com/watch?v={videoId}'
        