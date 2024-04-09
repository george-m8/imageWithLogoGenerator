import argparse
import os
import requests
from typing import List
from PIL import Image, ImageOps, ImageFilter # type: ignore
from io import BytesIO

# User configurable variables:
LOGO_PATH = './logos/example_logo.png' # Path to your logo within 'logos' directory

IMAGE_SIZE = (2560, 1600) # Desired image size (width, height) in pixels

IMAGE_SAVE_LOCATION = './output/' # Output directory for the processed images

# Add your Unsplash access key as an environment variable.
UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')

def query_unsplash_image_urls(query=None, total=1) -> List[str]:
    """Download images from Unsplash."""
    headers = {'Authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}'}
    if query:
        url = f"https://api.unsplash.com/search/photos?page=1&query={query}&per_page={total}"
        response = requests.get(url, headers=headers).json()
        images = [img["urls"]["regular"] for img in response["results"]]
    else:
        # Request for random images when no query is specified
        url = f"https://api.unsplash.com/photos/random?count={total}"
        response = requests.get(url, headers=headers).json()
        # Handle single or multiple random images
        if total == 1:
            images = [response["urls"]["regular"]] if isinstance(response, dict) else [img["urls"]["regular"] for img in response]
        else:
            images = [img["urls"]["regular"] for img in response]
    return images

def download_unsplash_image(image_url) -> Image.Image:
    """Download the image from the URL."""
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    return image

def process_image(image: Image.Image, bg_blur: float = 0.) -> Image.Image:
    """Crop, resize, and add logo to the image.
    
    Args:
        bg_blur: float - The amount of blur to apply to the background
          image (default: 0.)
    """    
    # Crop to the desired aspect ratio
    image = ImageOps.fit(image, IMAGE_SIZE, Image.Resampling.LANCZOS, 0, (0.5, 0.5))
    
    # Resize image
    image = image.resize(IMAGE_SIZE, Image.Resampling.LANCZOS)

    # Add blur effect
    if bg_blur > 0:
        image = image.filter(ImageFilter.GaussianBlur(radius=bg_blur))
    
    # Add logo
    logo = Image.open(LOGO_PATH).convert("RGBA")
    image.paste(logo, (image.width//2 - logo.width//2, image.height//2 - logo.height//2), logo)
    
    return image

def save_image(image, base_name, idx):
    """Save the processed image, avoiding overwrites."""
    # Ensure the output directory exists
    os.makedirs(IMAGE_SAVE_LOCATION, exist_ok=True)

    def construct_filepath(base_name, counter):
        while True:
            counter += 1
            filename = f"{base_name}_{counter}.png"
            full_path = os.path.join(IMAGE_SAVE_LOCATION, filename)
            if not os.path.exists(full_path):
                return filename, full_path
            
    filename, full_path = construct_filepath(base_name, idx)
    image.save(full_path)
    return filename

def main():
    parser = argparse.ArgumentParser(description="Generate images with a logo.")
    parser.add_argument("total", nargs='?', type=int, default=1, help="Number of images to generate (default: 1)")
    parser.add_argument("query", nargs='?', type=str, default=None, help="Search query for Unsplash (default: random)")
    parser.add_argument("--bg_blur", type=float, default=0., help="Amount of blur to apply to the background image (default: 0.)")
    args = parser.parse_args()
    
    images_urls = query_unsplash_image_urls(args.query, args.total)
    
    for idx, img_url in enumerate(images_urls):
        try:
            image = download_unsplash_image(img_url)
            processed_image = process_image(image, bg_blur=args.bg_blur)
            # If no query is specified, use a generic name.
            base_name = f"image_{args.query if args.query else 'noQuery'}"
            saved_filename = save_image(processed_image, base_name, idx+1)
            print(f"{saved_filename} saved successfully.")
        except Exception as e:
            print(f"Failed to process image {idx+1}: {e}")

if __name__ == "__main__":
    main()
