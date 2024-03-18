import io
import cloudinary.uploader
from cloudinary.api import resource
from googleapiclient.discovery import build
from pytube import YouTube


def search_yt(query, api_key, cname, cloud_key, secret_key):
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Search for videos on YouTube
    search_response = youtube.search().list(
        q=query,
        part='snippet',
        maxResults=1,
        type='video'

    ).execute()

    if search_response['items']:
        video_id = search_response['items'][0]['id']['videoId']
        video_title = search_response['items'][0]['snippet']['title']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        uploader_name = search_response['items'][0]['snippet']['channelTitle']
        audio_link = download_and_upload_youtube_audio(video_url, cname, cloud_key, secret_key)
        if audio_link is False:
            return "Sorry, the file is too large to download. Please try another video."

        return {
            'yt_id': f'{video_id}',
            'title': video_title,
            'video_url': video_url,
            'uploader': uploader_name,
            'audio_link': audio_link,
        }
    else:
        return None


def sanitize_filename(filename):
    # Define a set of characters that are not allowed in filenames and Cloudinary public_ids
    invalid_chars = '<>:"/\\|?*&'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    # Replace spaces with underscores to avoid issues
    filename = filename.replace(' ', '_')
    # Optional: replace other problematic characters like dashes if necessary
    filename = filename.replace('-', '_')
    return filename


def download_and_upload_youtube_audio(video_url, cname, apikey, secret_key, cloudinary_folder='audio_files'):
    # Initialize Cloudinary
    cloudinary.config(
        cloud_name=cname,
        api_key=apikey,
        api_secret=secret_key
    )
    try:
        yt = YouTube(video_url)
        try:
            public_id = f'audio_files/{yt.video_id}'
            response = resource(public_id, resource_type='video')
            print('File already uploaded:', response.get('url'))
            return response.get('url')
        except Exception as e:
            print('File not found, proceed with upload:', str(e))

        audio_stream = yt.streams.filter(only_audio=True).first()
        print(f"Downloading audio: {yt.title}...")
        file_size = audio_stream.filesize
        print(f"File size: {file_size} bytes")

        if file_size > 20_000_000:  # Limit to 20MB for this example
            return "Sorry, the file is too large to download. Please try another video."

        audio_buffer = io.BytesIO()
        audio_stream.stream_to_buffer(buffer=audio_buffer)
        audio_buffer.seek(0)

        response = cloudinary.uploader.upload(
            file=audio_buffer,
            resource_type='video',
            folder=cloudinary_folder,
            public_id=yt.video_id,
            format='mp3',
        )
        print('Uploaded MP3 URL:', response.get('url'))

        audio_buffer.close()

        print("Cleaned Stream")
        return response.get('url')
    except Exception as e:
        return f"An error occurred: {str(e)}"
