from googleapiclient.discovery import build
import pandas as pd

API_KEY = "AIzaSyCLqIYFpdOxYB2_fsuBBfclAYKWYBkdQts"

youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_channel_videos(channel_id):
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=50,
        order="date"
    )
    response = request.execute()
    
    video_ids = []
    for item in response['items']:
        if item['id']['kind'] == 'youtube#video':
            video_ids.append(item['id']['videoId'])
    
    return video_ids


def get_video_details(video_ids):
    all_data = []
    
    request = youtube.videos().list(
        part="snippet,statistics",
        id=",".join(video_ids)
    )
    response = request.execute()
    
    for video in response['items']:
        data = dict(
            title=video['snippet']['title'],
            views=int(video['statistics'].get('viewCount', 0)),
            likes=int(video['statistics'].get('likeCount', 0)),
            comments=int(video['statistics'].get('commentCount', 0)),
            published=video['snippet']['publishedAt']
        )
        all_data.append(data)
    
    return pd.DataFrame(all_data)


channel_id = "UC_x5XG1OV2P6uZZ5FSM9Ttw"

video_ids = get_channel_videos(channel_id)
df = get_video_details(video_ids)

df.to_csv("youtube_data.csv", index=False)

print("✅ Data saved successfully!")