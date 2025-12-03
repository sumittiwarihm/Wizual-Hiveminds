# File: Backend/api/services/imagen_service.py

import os
from google import genai
from google.genai import types
from .gcs_service import upload_media_to_gcs 


API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise EnvironmentError("GOOGLE_API_KEY environment variable is not set. Please set it to proceed.")

try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    raise RuntimeError(f"Failed to initialize GenAI client: {e}")


IMAGE_STYLE_PROMPTS = {
    "no_style": "",
    "photo": "photorealistic, high detail, DSLR style, hyper-realistic, 8k",
    "illustration": "flat vector illustration, clean lines, minimalist design",
    "3d": "3D render, cinematic lighting, product render, Octane render",
    "cartoon_fun": "colorful cartoon, playful fun style, high saturation",
    "comic": "comic book style, bold ink outlines, halftone shading, vibrant",
    "dark": "dark, moody lighting, dramatic shadows, noir style",
    "watercolor": "soft watercolor painting, gentle gradients, wet-on-wet technique",
    "pixel_art": "8-bit pixel art, retro video game style, low resolution detail",
    "oil_painting": "oil painting with textured brush strokes, impasto technique",
    "nature": "nature aesthetic, vibrant greens and blues, serene landscape",
    "ink_print": "ink print, monochrome sketch with ink lines, block print texture",
    "pencil": "pencil sketch, grayscale, hand-drawn look, detailed shading",
    "retrowave": "1980s retrowave neon, vaporwave, synthwave glow, chromatic aberration",
}


def generate_image_with_imagen3(prompt: str, style_key: str) -> list[str]:
    
    style_text = IMAGE_STYLE_PROMPTS.get(style_key, "")
    full_prompt = prompt + (f", Style: {style_text}" if style_text else "")

    print(f"[Imagen Service] Generating with prompt: {full_prompt}")

    try:
        response = client.models.generate_images(
            model="imagen-4.0-generate-001", 
            prompt=full_prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1, 
                aspect_ratio="1:1"
            )
        )
    except AttributeError:
        raise RuntimeError("Image generation failed. Ensure your 'google-genai' SDK is up-to-date (pip install --upgrade google-genai).")
    except Exception as e:
        raise RuntimeError(f"Imagen API call failed. Check quota, permissions, or network connectivity: {e}") 

    
    if not response.generated_images: 
        raise ValueError("Image generation returned no image data in the response.")
        
    
    image_urls = []
    for generated_image in response.generated_images: 
        image_bytes = generated_image.image.image_bytes
        
        image_url = upload_media_to_gcs(image_bytes, file_extension="png")
        image_urls.append(image_url)
    
    return image_urls