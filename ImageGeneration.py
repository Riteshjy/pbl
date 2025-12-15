import asyncio
import os
from random import randint
from PIL import Image
import requests
from dotenv import get_key
from time import sleep

# Function to open and display images based on a given prompt
def open_images(prompt: str):
    folder_path = r"Data"  # Folder where the images are stored
    prompt = prompt.replace(" ", "_")  # Replace spaces in prompt with underscores

    # Generate filenames for the images
    files = [f"{prompt}_{i}.jpg" for i in range(1, 5)]

    for jpg_file in files:
        image_path = os.path.join(folder_path, jpg_file)
        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)  # Pause for 1 second before showing the next image
        except IOError:
            print(f"Unable to open {image_path}")

# API details for the Hugging Face Stable Diffusion model
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
API_KEY = get_key(".env", "HuggingFaceAPIKey")
headers = {"Authorization": f"Bearer {API_KEY}"}

# Async function to send a query to the Hugging Face API
async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    return response.content

# Async function to generate images based on the given prompt
# Async function to generate images based on the given prompt
async def generate_images(prompt: str):
    tasks = []

    # Create 4 image generation tasks
    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, ultra high details, high resolution, seed={randint(0, 10000)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    # Wait for all tasks to complete
    image_bytes_list = await asyncio.gather(*tasks)

    # Save the generated images to files
    os.makedirs("Data", exist_ok=True)
    for i, image_bytes in enumerate(image_bytes_list, start=1):
        file_path = fr"Data/{prompt.replace(' ', '_')}_{i}.jpg"
        with open(file_path, "wb") as f:
            f.write(image_bytes)
        print(f"Saved: {file_path}")


# Wrapper function to generate and open images
def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))  # Run the async image generation
    open_images(prompt)                   # Open the generated images


# Main loop to monitor for image generation requests
while True:
    try:
        # Read the status and prompt from the data file
        with open(r"Frontend\Files\ImageGeneration.data", "r") as f:
            data: str = f.read().strip()

        # Skip if file is empty or improperly formatted
        if not data or ", " not in data:
            sleep(1)
            continue

        prompt, status = data.split(", ")

        # If the status indicates an image generation request
        if status.strip().lower() == "true":
            print("Generating Images...")
            GenerateImages(prompt=prompt.strip())

            # Reset the status in the file after generating images
            with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
                f.write("False, False")

            break  # Exit the loop after processing the request
        else:
            sleep(1)  # Wait for 1 second before checking again

    except:
        pass