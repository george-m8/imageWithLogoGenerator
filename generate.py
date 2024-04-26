import argparse
import os
import requests
from PIL import Image, ImageOps # type: ignore
from io import BytesIO
import logging

# Set up logging config
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler(), logging.FileHandler('logfile.log')])

# User configurable variables:
LOGO_PATH = './logos/white.png' # Path to your logo within 'logos' directory

IMAGE_SIZE = (2560, 1600) # Desired image size (width, height) in pixels

IMAGE_SAVE_LOCATION = './output/' # Output directory for the processed images

# Add your Unsplash access key as an environment variable.
UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')
#print(UNSPLASH_ACCESS_KEY)

# Calculate params from user config vars
if IMAGE_SIZE[0] > IMAGE_SIZE[1]:
    orientation = 'landscape'
elif IMAGE_SIZE[0] < IMAGE_SIZE[1]:
    orientation = 'portrait'
else:
    orientation = 'squareish'
logging.debug(f"Image orientation: {orientation}")

def download_unsplash_images(query=None, total=1):
    """Download images from Unsplash."""
    headers = {'Authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}'}
    if query:
        url = f"https://api.unsplash.com/search/photos?page=1&query={query}&per_page={total}"
        response = requests.get(url, headers=headers).json()
        if 'errors' in response:
            print(response['errors'])
            return []
        images = [img["urls"]["regular"] for img in response["results"]]
    else:
        # Request for random images when no query is specified
        url = f"https://api.unsplash.com/photos/random?count={total}"
        response = requests.get(url, headers=headers).json()
        if 'errors' in response:
            print(response['errors'])
            return []
        # Handle single or multiple random images
        if total == 1:
            images = [response["urls"]["regular"]] if isinstance(response, dict) else [img["urls"]["regular"] for img in response]
        else:
            images = [img["urls"]["regular"] for img in response]
    return images

def process_image(image_url):
    """Crop, resize, and add logo to the image."""
    # Download image
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    
    # Crop to the desired aspect ratio
    image = ImageOps.fit(image, IMAGE_SIZE, Image.Resampling.LANCZOS, 0, (0.5, 0.5))
    
    # Resize image
    image = image.resize(IMAGE_SIZE, Image.Resampling.LANCZOS)
    
    # Add logo
    logo = Image.open(LOGO_PATH).convert("RGBA")
    image.paste(logo, (image.width//2 - logo.width//2, image.height//2 - logo.height//2), logo)
    
    return image

def save_image(image, base_name, idx):
    """Save the processed image, avoiding overwrites."""
    # Ensure the output directory exists
    os.makedirs(IMAGE_SAVE_LOCATION, exist_ok=True)
    
    filename = f"{base_name}_{idx}.png"
    counter = idx
    # Construct the full path with the directory
    full_path = os.path.join(IMAGE_SAVE_LOCATION, filename)
    
    # Check if the file already exists and iterate the number if needed
    while os.path.exists(full_path):
        counter += 1
        filename = f"{base_name}_{counter}.png"
        full_path = os.path.join(IMAGE_SAVE_LOCATION, filename)
    
    image.save(full_path)
    return filename

def main():
    parser = argparse.ArgumentParser(description="Generate images with a logo.")
    parser.add_argument("total", nargs='?', type=int, default=1, help="Number of images to generate (default: 1)")
    parser.add_argument("query", nargs='?', type=str, default=None, help="Search query for Unsplash (default: random)")
    args = parser.parse_args()
    
    images = download_unsplash_images(args.query, args.total)
    for idx, img_url in enumerate(images):
        try:
            processed_image = process_image(img_url)
            # If no query is specified, use a generic name.
            base_name = f"image_{args.query if args.query else 'noQuery'}"
            saved_filename = save_image(processed_image, base_name, idx+1)
            print(f"{saved_filename} saved successfully.")
        except Exception as e:
            print(f"Failed to process image {idx+1}: {e}")

if __name__ == "__main__":
    main()
