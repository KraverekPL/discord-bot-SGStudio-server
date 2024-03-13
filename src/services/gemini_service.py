import logging
import os
import re

import discord
import vertexai
import io
from PIL import Image
from google.generativeai.notebook import text_model
from google.oauth2 import service_account
from vertexai import generative_models
from vertexai.generative_models import GenerativeModel, HarmCategory, HarmBlockThreshold

# Configure the generative AI model
message_history = {}
MAX_HISTORY = 12
text_generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}
image_generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 2048,
}
safety_settings = {
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
}

# Google Cloud Settings
PROJECT_ID = os.getenv('project_name')
LOCATION = os.getenv('location')

credentials = service_account.Credentials.from_service_account_file(
    "credentials.json"
)

# Load Gemini Pro
text_model = GenerativeModel(model_name="gemini-1.0-pro", generation_config=text_generation_config,
                             safety_settings=safety_settings)
# Load Gemini Pro Vision
image_model = GenerativeModel(model_name="gemini-1.0-pro-vision", generation_config=image_generation_config,
                              safety_settings=safety_settings)


async def chat_with_gemini(message):
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    user_input = message.content.strip()
    cleaned_text = clean_discord_message(user_input)

    async with message.channel.typing():
        if message.attachments:
            logging.info("Message (image) from:" + str(message.author.name) + ": " + cleaned_text)
            await message.add_reaction('🎨')
            if message.attachments:
                attachment = message.attachments[0]
                logging.info(f"Attachment url: {attachment.url}")
                image_data = await attachment.read()
                with Image.open(io.BytesIO(image_data)) as img:
                    resized_img = resize_image_with_aspect_ratio(img, 256)
                    resized_img_data = io.BytesIO()
                    resized_img.save(resized_img_data, format='JPEG')
                    resized_img_data.seek(0)
                # await message.channel.send(file=discord.File(resized_img_data, filename='resized_image.jpg'))
                image = generative_models.Part.from_data(resized_img_data.getvalue(),
                                                         mime_type=get_correct_mimetype(attachment.url))
                prompt = "Dokładnie opisz zdjęcie"
                if not cleaned_text:
                    cleaned_text = prompt
                logging.info(f"prompt: {cleaned_text}")
                model_response = image_model.generate_content([cleaned_text, image])
                logging.info("Response:" + model_response.text)
                await message.reply(model_response.text)
        else:
            chat = text_model.start_chat()
            responses = chat.send_message(cleaned_text)
            logging.info("Message from:" + str(message.author.name) + ": " + cleaned_text)
            logging.info("Response:" + str(responses.text))
            await message.reply(responses.text)


def clean_discord_message(input_string):
    bracket_pattern = re.compile(r'<[^>]+>')
    cleaned_content = bracket_pattern.sub('', input_string)
    return cleaned_content


def get_correct_mimetype(image_path):
    image_path = image_path.split('?')[0]
    logging.info(f"Image url: {image_path}")
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg', '.ico', '.raw']
    if any(image_path.lower().endswith(ext) for ext in image_extensions):
        if image_path.lower().endswith('.jpg') or image_path.lower().endswith('.jpeg'):
            mime_type = 'image/jpeg'
        elif image_path.lower().endswith('.png'):
            mime_type = 'image/png'
        elif image_path.lower().endswith('.gif'):
            mime_type = 'image/gif'
        elif image_path.lower().endswith('.bmp'):
            mime_type = 'image/bmp'
        elif image_path.lower().endswith('.tiff'):
            mime_type = 'image/tiff'
        elif image_path.lower().endswith('.webp'):
            mime_type = 'image/webp'
        elif image_path.lower().endswith('.svg'):
            mime_type = 'image/svg+xml'
        elif image_path.lower().endswith('.ico'):
            mime_type = 'image/x-icon'
        elif image_path.lower().endswith('.raw'):
            mime_type = 'image/x-raw'
    logging.info(f"mime_type: {mime_type}")
    return mime_type


def resize_image_with_aspect_ratio(image, target_size):
    width, height = image.size
    aspect_ratio = width / height
    if width > height:
        new_width = target_size
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = target_size
        new_width = int(new_height * aspect_ratio)
    resized_img = image.resize((new_width, new_height))
    return resized_img
