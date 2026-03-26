import os

from dotenv import find_dotenv, load_dotenv

from utils import clean_title

import yt_dlp

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

TEMP_FOLDER = os.getenv("TEMP_FOLDER")


def download_mp3_from_yt(url):
    os.makedirs(TEMP_FOLDER, exist_ok=True)
    ydl_options = {
        'quiet': True,
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(TEMP_FOLDER, '%(title)s.%(ext)s'),
        'nocheckcertificate': True,
        # 'writethumbnail': True,
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },
            # {
            #     'key': 'FFmpegThumbnailsConvertor',
            #     'format': 'jpg',
            # },
            # {
            #     # 3. Embed the thumbnail into the MP3
            #     'key': 'EmbedThumbnail',
            # },
            # {
            #     # 4. Add metadata (Title, Artist, etc.)
            #     'key': 'FFmpegMetadata',
            #     'add_metadata': True,
            # }
        ],
        # 'postprocessor_args': {
        #     'ffmpeg': [
        #         # '-vf', 'crop=ih:ih,scale=500:500',  # Crops to center square & resizes
        #         '-q:v', '5'  # Adjusts JPG quality (2-5 is good)
        #     ]
        # }
    }

    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        title = clean_title(info_dict.get('title', None))
        filename = ydl.prepare_filename(info_dict)

        # Apply clean_title to the mp3 filename as well
        dirty_mp3 = os.path.splitext(filename)[0] + ".mp3"
        clean_mp3 = os.path.join(os.path.dirname(dirty_mp3), title + ".mp3")

        # Rename the file on disk to match the clean title
        if os.path.exists(dirty_mp3) and dirty_mp3 != clean_mp3:
            os.rename(dirty_mp3, clean_mp3)

        return clean_mp3, title
