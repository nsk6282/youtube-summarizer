import os
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import openai

# Set up your OpenAI API key
#pip install openai==0.28
#pip install google-api-python-client
#pip install youtube_transcript_api


# Set up your YouTube Data API key
youtube_api_key = 'Youtubeapi-key'

def fetch_video_data(video_id):
    youtube = build('youtube', 'v3', developerKey=youtube_api_key)
    request = youtube.videos().list(part='snippet', id=video_id)
    response = request.execute()
    return response['items'][0]['snippet']

def fetch_video_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text = ''
    for line in transcript:
        text += line['text'] + ' '
    return text

def summarize_text_with_gpt(text, max_tokens=150):
    openai.api_key = 'openapi-key'  
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=text,
        max_tokens=max_tokens,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response['choices'][0]['text'].strip()

if __name__ == "__main__":
    video_id = 'youtube-video-id'  # Replace with the ID of the YouTube video you want to summarize
    video_data = fetch_video_data(video_id)
    video_title = video_data['title']
    video_description = video_data['description']
    video_transcript = fetch_video_transcript(video_id)
    summary = summarize_text_with_gpt(video_transcript)

    print(f"Video Title: {video_title}")
    print(f"Video Description: {video_description}")
    print(f"Video Summary: {summary}")
