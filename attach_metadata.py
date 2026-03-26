import requests
from mutagen.id3 import ID3, TIT2, TPE1, TALB, APIC, ID3NoHeaderError
from ytmusicapi import YTMusic


def attach_metadata(mp3_file, title):
    yt = YTMusic()
    results = yt.search(title, filter="songs")

    if not results:
        print("No results found.")
        return

    top_result = results[0]
    title = top_result.get("title", "Unknown Title")
    album = top_result["album"].get("name", "Unknown Album")
    artists = [artist_data.get("name", "Unknown") for artist_data in top_result["artists"]]
    thumbnail_url = top_result["thumbnails"][-1].get("url", "")

    # Load or create ID3 tags
    try:
        tags = ID3(mp3_file)
    except ID3NoHeaderError:
        tags = ID3()

    # Write text tags
    tags["TIT2"] = TIT2(encoding=3, text=title)
    tags["TPE1"] = TPE1(encoding=3, text=artists)
    tags["TALB"] = TALB(encoding=3, text=album)

    # Download and embed thumbnail as cover art
    if thumbnail_url:
        response = requests.get(thumbnail_url)
        if response.status_code == 200:
            tags["APIC:"] = APIC(
                encoding=3,  # UTF-8
                mime="image/jpeg",
                type=3,  # 3 = Cover (front)
                desc="Cover",
                data=response.content
            )

    tags.save(mp3_file)
    # print(f"Metadata attached: '{title}' by {artists} | Album: {album}")
    return mp3_file
