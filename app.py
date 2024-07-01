from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
import google.generativeai as genai

# Initialize APIs
youtube_api_key = 'YOUR_YOUTUBE_API_KEY'
google_api_key = 'YOUR_GOOGLE_API_KEY'
youtube = build('youtube', 'v3', developerKey=youtube_api_key)
genai.configure(api_key=google_api_key)

prompt = """You are an agent to help a buyer make an informed decision about a product.
You will be taking the transcript text from a YouTube video review and providing a summary in points
that highlights the pros and cons of the product within 250 words. Please provide the summary of the text given here: """

def search_top_video(query, youtube):
    search_response = youtube.search().list(
        part='snippet',
        maxResults=1,
        q=query,
        order='relevance'
    ).execute()
    for item in search_response['items']:
        if item['id']['kind'] == 'youtube#video':
            return item['id']['videoId']
    return None

def get_video_captions(video_id):
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    captions = " ".join([entry['text'] for entry in transcript_list])
    return captions

def generate_gemini_content(transcript_text):
    combined_text = prompt + transcript_text
    response = genai.generate_text(model='models/text-bison-001', prompt=combined_text)
    return response.result
