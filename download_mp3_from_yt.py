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
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        title = clean_title(info_dict.get('title', None))
        filename = ydl.prepare_filename(info_dict)
        mp3_file = os.path.splitext(filename)[0] + ".mp3"
        return mp3_file, title
