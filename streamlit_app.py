import streamlit as st
from app import search_top_video, get_video_captions, generate_gemini_content

def main():
    st.title("Product Reviews Powered by YouTube Videos")

    product_name = st.text_input("Enter the product name:")
    query = f"{product_name} review"

    if product_name:
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
