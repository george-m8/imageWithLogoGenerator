# Logo Image Generator

This tool generates high-resolution images using the Unsplash API with a centered logo image superimposed. It's designed to fetch images based on a search query or randomly select them from Unsplash, preparing them for use as wallpapers or backgrounds that include your custom logo.

## Features

- Downloads high-quality images from Unsplash based on a search query or randomly.
- Superimposes a specified logo in the center of each image.

## How to Use

### Setup

1. **Create a Virtual Environment:** To avoid conflicts with other Python projects, create a virtual environment in your project directory.

    ```bash
    python3 -m venv venv
    ```

2. **Activate the Virtual Environment:**

    - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

    - On Windows:

        ```cmd
        .\venv\Scripts\activate
        ```

3. **Install Dependencies:** Install the required Python packages from `requirements.txt`.

    ```bash
    pip install -r requirements.txt
    ```

4. **Unsplash API Key:** Set your Unsplash Access Key as an environment variable by adding it to your `.bashrc`, `.zshrc`, or equivalent profile:

    ```bash
    export UNSPLASH_ACCESS_KEY=your_unsplash_access_key_here
    ```

    Ensure to replace `your_unsplash_access_key_here` with your actual Unsplash Access Key.

### Running the Script

- Generate a default image (1 random image):

    ```bash
    python generate.py
    ```

- Specify the number of images and a search query:

    ```bash
    python generate.py 5 nature
    ```
  
    Generates 5 images matching the query "nature".

- Generate a specific number of random images:

    ```bash
    python generate.py 10
    ```

    Downloads 10 random images from Unsplash.

### Customizing the Script

To tailor the script to your needs, such as changing the image resolution, logo, or output directory, you can modify the following variables in `generate.py`:

- **Resolution:** The default resolution is set to `2560 x 1600` to match MacBook M1 screens. To change it, adjust the `IMAGE_SIZE` variable.

    ```python
    IMAGE_SIZE = (2560, 1600)  # Adjust to desired dimensions
    ```

- **Logo:** To change the logo that is superimposed on each image, modify the `LOGO_PATH` variable to the path of your logo image.

    ```python
    LOGO_PATH = 'path/to/your/logo.png'  # Update with the actual path to your logo
    ```

- **Output Folder:** Images are saved in a default output directory. To change this, adjust the `IMAGE_SAVE_LOCATION` variable.

    ```python
    IMAGE_SAVE_LOCATION = './output/'  # Change to your desired output directory
    ```

### To Do

- [ ] **Include Photographer Credit:** Future updates will add the photographer's name and profile URL from Unsplash as a credit in the image's bottom right corner.
- [ ] **Customization Options:** Expand customization options, including different placements for the logo and selectable text fonts for credits.
- [ ] **Ensure API Usage Meets Guidelines:** Ensure that images are downloaded correctly using the API and correct calls to gain production API license.
- [ ] **Automatically Choose Logo Based On Image Colours:** Logo should be black or white if more legible on image.

## License

This project is open-source and available under the MIT License.
