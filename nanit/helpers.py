import os
import urllib.parse

import requests

from .client import NanitClient


def download_video(client: NanitClient, baby_uid: str, event_uid: str, output: str = None):
    event = client.camera_event(baby_uid=baby_uid, event_uid=event_uid)
    video_url = event["playlist"]["media_segments"][0]["video_url"]
    parts = urllib.parse.urlparse(video_url)
    filename = output or os.path.basename(parts.path)
    response = requests.get(video_url)
    with open(filename, "wb") as handler:
        handler.write(response.content)
