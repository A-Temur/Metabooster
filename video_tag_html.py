import json
import os
import datetime
import subprocess
import easygui

def get_video_duration(video_path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "json", video_path],
        capture_output=True, text=True
    )
    metadata = json.loads(result.stdout)
    duration = float(metadata["format"]["duration"])
    minutes = int(duration // 60)
    seconds = int(duration % 60)
    iso_duration = f"PT{minutes}M{seconds}S"
    return iso_duration

def get_video_metadata(video_path):

    name = os.path.basename(video_path).replace("_", " ").replace(".mp4", "")[0],

    return {
        "@context": "https://schema.org",
        "@type": "VideoObject",
        "@id": f"#{name}",
        "name": name,
        "description": "Media for OG-Brain.com",
        "thumbnailUrl": "https://example.com/video-thumbnail.jpg",
        "uploadDate": datetime.datetime.now().isoformat(),
        "contentUrl": f"https://og-brain.com/{os.path.basename(video_path)}",
        "duration": get_video_duration(video_path)
    }

video_metadata = easygui.diropenbox("select folder")

for root, _, files in os.walk(video_metadata):
    for file in files:
        file_path = os.path.join(root, file)
        if file.lower().endswith((".mp4", ".mov")):
            print(get_video_metadata(file_path))
        else:
            print(f"Skipping unsupported file: {file_path}")


# with open("video_metadata.json", "w") as json_file:
#     json.dump(video_metadata, json_file, indent=4)
