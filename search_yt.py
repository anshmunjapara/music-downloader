import json

import yt_dlp


def search_yt(query: str, max_results: int = 5):
    ydl_options = {
        'quiet': True,
        'extract_flat': True,  # Don't download, just get metadata
        'force_generic_extractor': False,
        'nocheckcertificate': True,
    }

    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        results = ydl.extract_info(f"ytsearch{max_results}:{query}", download=False)
        print(results)
        videos = []
        for entry in results["entries"]:
            videos.append({
                "title": entry.get("title"),
                "url": entry.get("url"),
                "channel": entry.get("channel"),
                "thumbnail": entry.get("thumbnails")[0].get("url"),
            })

        return videos

