## Logo image generator
# Generates images using Unsplash API at specified resolution with a centered logo image superimposed in the center.

# How to use:
- Create a virtual environment and install dependencies from the requirements file.
- Run the generate.py script using:
```bash
python generate.py
```

Alternatively, arguments can be passed for number of images and search query, for example:
```bash
python generate.py 5 nature
```
This will generate 5 images matching the query "nature".

```bash
python generate.py 10
```
This will generate 10 images selected from Unsplash at random

# Unsplash API
Your Unsplash API should be added as a environmental variable within the suitible profile, for example in .bashrc:
```text
export UNSPLASH_ACCESS_KEY=your_unsplash_access_key_here
```
