import os
from google import genai
from google.genai import types
import time
from .gcs_service import upload_media_to_gcs 

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise EnvironmentError("GOOGLE_API_KEY environment variable is not set. Please set it to proceed.")

client = genai.Client(api_key=API_KEY)

VIDEO_STYLE_PROMPTS = {
    "cinematic": "High-quality, cinematic film look, 4K, dramatic lighting.",
    "fantasy": "Vibrant colors, fantasy setting, intricate details.",
    "documentary": "Natural lighting, handheld camera, realistic grain.",
}

def generate_video_with_veo(prompt: str, style_key: str) -> str:
    style_text = VIDEO_STYLE_PROMPTS.get(style_key, "")
    full_prompt = prompt + (f", Style: {style_text}" if style_text else "")

    print("Starting Video Generation")
    try:
        # Starting generation
        operation = client.models.generate_videos(
            model="veo-3.1-generate-preview",
            prompt=full_prompt,
        )

        # polling the completion
        while not operation.done:
            print("Waiting for video generation to complete...")
            time.sleep(10)
            operation = client.operations.get(operation)

        print("Video generation complete.")

        if not operation.response.generated_videos:
            raise ValueError("Video generation returned no video data.")

        generated_video = operation.response.generated_videos[0]
        video_file = generated_video.video

        print("Downloading video using SDK...")
        
        
        client.files.download(file=video_file)

        video_bytes = video_file.data

        if not video_bytes:
            raise Exception("Downloaded video is empty")
        signed_url = upload_media_to_gcs(video_bytes, "mp4")

        print(f"Uploaded to GCS URL: {signed_url}")
        return signed_url

    except Exception as e:
        print(f"API Error or model error: {e}")
        return ""
