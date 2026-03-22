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
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(TEMP_FOLDER, '%(title)s.%(ext)s'),
        'nocheckcertificate': True,
        'writethumbnail': True,
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },
            {
                'key': 'FFmpegThumbnailsConvertor',
                'format': 'jpg',
            },
            {
                # 3. Embed the thumbnail into the MP3
                'key': 'EmbedThumbnail',
            },
            {
                # 4. Add metadata (Title, Artist, etc.)
                'key': 'FFmpegMetadata',
                'add_metadata': True,
            }
        ],
        'postprocessor_args': {
            'ffmpeg': [
                # '-vf', 'crop=ih:ih,scale=500:500',  # Crops to center square & resizes
                '-q:v', '5'  # Adjusts JPG quality (2-5 is good)
            ]
        }
    }

    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        title = clean_title(info_dict.get('title', None))
        filename = ydl.prepare_filename(info_dict)
        mp3_file = os.path.splitext(filename)[0] + ".mp3"
        return mp3_file, title
