import pandas as pd 
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def get_comments(api_key, video_id, max_results=50):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.commentThreads().list(
            part='snippet',
            maxResults=max_results,
            videoId=video_id,
            textFormat='plainText'
        )
        response = request.execute()
        return response
    except HttpError as e:
        if 'invalidVideoId' in str(e):
            pass
        else:
            pass
        return None

def get_comment_details(api_key, comment_id):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.comments().list(
            part='snippet',
            id=comment_id
        )
        response = request.execute()
        return response['items'][0]['snippet']
    except HttpError as e:
        pass
        return None

def process_videos(api_key, video_ids):
    for video_id in video_ids:
        all_comments = []
        comments_data = get_comments(api_key, video_id)
        if comments_data:
            comment_threads = comments_data.get('items', [])
            for comment in comment_threads:
                top_level_comment_snippet = comment['snippet']['topLevelComment']['snippet']

                # Get additional details for the top-level comment
                comment_id = comment['id']
                comment_details = get_comment_details(api_key, comment_id)

                comment_text = top_level_comment_snippet['textDisplay']
                author_name = top_level_comment_snippet['authorDisplayName']
                author_channel_id = top_level_comment_snippet['authorChannelId']
                author_channel_url = f"https://www.youtube.com/channel/{author_channel_id}"
                publish_time = top_level_comment_snippet['publishedAt']
                like_count = top_level_comment_snippet['likeCount']
                reply_count = comment['snippet']['totalReplyCount']

                # Additional details for the top-level comment
                replied_channel_id = comment_details['authorChannelId']
                replied_channel_name = comment_details['authorDisplayName']

                all_comments.append([reply_count, like_count, publish_time, author_name, comment_text, author_channel_id, author_channel_url,
                                     replied_channel_id, replied_channel_name])

            # Convert the list of comments into a DataFrame
            df_comments = pd.DataFrame(all_comments, columns=['ReplyCount', 'LikeCount', 'PublishTime', 'AuthorName', 'Text', 'AuthorChannelID', 'AuthorChannelURL',
                                                              'RepliedChannelID', 'RepliedChannelName'])

            # Save the DataFrame as a CSV file with the video_id as the filename
            df_comments.to_csv(f'Video_{video_id}.csv', index=False)

def main():
    api_key = 'Input Your YouTube API Key'

    # Read the CSV file containing video IDs
    df = pd.read_csv('YourInput File Name.csv')

    # Extract the video IDs
    video_ids = df['Name of Coloumn Where Video Id Exists'].tolist()

    # Get comments for each video ID and store them in separate CSV files
    process_videos(api_key, video_ids)

if __name__ == '__main__':
    main()
