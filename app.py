import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
import google.generativeai as genai

# Replace 'YOUR_YOUTUBE_API_KEY' and 'YOUR_GOOGLE_API_KEY' with your actual API keys
youtube_api_key = 'Add_Your_API_Keys'
google_api_key = 'Add_Your_API_Keys'

# Initialize APIs
youtube = build('youtube', 'v3', developerKey=youtube_api_key)
genai.configure(api_key=google_api_key)

prompt = """You are an agent to help a buyer make an informed decision about a product.
You will be taking the transcript text from a YouTube video review and providing a summary in points
that highlights the pros and cons of the product within 250 words. Please provide the summary of the text given here: """

# Function to search for the top video
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

# Function to get video captions
def get_video_captions(video_id):
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    captions = " ".join([entry['text'] for entry in transcript_list])
    return captions

# Function to generate content using Google Gemini API
def generate_gemini_content(transcript_text):
    combined_text = prompt + transcript_text
    response = genai.generate_text(model='models/text-bison-001', prompt=combined_text)  # Ensure 'models/text-bison-001' is the correct model ID
    return response.result

# Main function to fetch and process video details
def main():

    st.title("Product reviews powered by YT video")

    # Add a text input field for the user to enter the product name
    product_name = st.text_input("Enter the product name:")

    # Construct the search query by appending "review" to the product name
    query = f"{product_name} review"

    if product_name != "":
        video_id = search_top_video(query, youtube)
        if video_id:
            st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

            if st.button("Get Pros and Cons Summary"):
                captions = get_video_captions(video_id)
                if captions:
                    summary = generate_gemini_content(captions)
                    st.markdown("## Pros and Cons Summary:")
                    st.write(summary)
                else:
                    st.write("No captions found for the video.")
        else:
            st.write("No video found for the query.")

if __name__ == "__main__":
    main()
