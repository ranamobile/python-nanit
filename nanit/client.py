import argparse
import json
import logging
import os
import urllib.parse

import requests

from .constants import NANIT_AUTH_FILE, NANIT_API_URL, NANIT_API_HEADERS


class NanitClient:

    def __init__(self, auth_file):
        self.auth_file = auth_file
        with open(auth_file, "r") as handler:
            self.auth_json = json.load(handler)
        assert "access_token" in self.auth_json, "Missing access_token in auth file"

        self.session = requests.Session()
        self.session.headers.update(NANIT_API_HEADERS)
        self.session.headers.update({"authorization": f'Bearer {self.auth_json["access_token"]}'})

    def _request(self, path):
        response = self.session.get(f'{NANIT_API_URL}{path}')
        assert response.status_code == 200, "Invalid request or token"
        print(response.headers)
        content = response.json()
        filename = path.replace("/", "_") + '.json'
        with open(filename, "w") as handler:
            json.dump(content, handler, indent=2)
        return content

    def current_user(self):
        return self._request(f'/user')

    def cameras(self):
        return self._request(f'/babies')

    def camera_status(self, camera_uid):
        return self._request(f'/focus/cameras/{camera_uid}/connection_status')

    def camera_events(self, baby_uid):
        return self._request(f'/babies/{baby_uid}/events?limit=10')

    def camera_event(self, baby_uid, event_uid):
        return self._request(f'/babies/{baby_uid}/events/{event_uid}')

    def camera_latest_event(self, baby_uid):
        return self._request(f'/babies/{baby_uid}/events/last')

    def camera_event_clip(self, baby_uid, event_uid):
        return self._request(f'/babies/{baby_uid}/events/{event_uid}/clip')

    def camera_users(self, baby_uid):
        return self._request(f'/babies/{baby_uid}/users')

    def camera_permissions(self, baby_uid):
        return self._request(f'/babies/{baby_uid}/permissions')

    def camera_subscriptions(self, baby_uid):
        return self._request(f'/babies/{baby_uid}/subscriptions')

    def camera_messages(self, baby_uid):
        return self._request(f'/babies/{baby_uid}/messages')

    def camera_night_settings(self, baby_uid):
        return self._request(f'/babies/{baby_uid}/night_settings')

    def cards(self):
        return self._request(f'/cards')

    @staticmethod
    def main():
        parser = argparse.ArgumentParser()
        parser.add_argument("-a", "--auth_file", default=NANIT_AUTH_FILE,
                            help="auth file (JSON) to containing the access token")
        parser.add_argument("-v", "--verbose", action="store_true",
                            help="enable verbose logging to console")
        args = parser.parse_args()

        logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

        client = NanitClient(args.auth_file)
        cameras = client.cameras()
        baby_uid = cameras["babies"][0]["uid"]
        camera_uid = cameras["babies"][0]["camera"]["uid"]

        #events = client.camera_events(baby_uid)
        status = client.camera_status(camera_uid)
        # for event in events["events"]:
        #     video_url = event["playlist"]["media_segments"][0]["video_url"]
        #     parts = urllib.parse.urlparse(video_url)
        #     filename = os.path.basename(parts.path)
        #     response = requests.get(video_url)
        #     with open(filename, "wb") as handler:
        #         handler.write(response.content)

if __name__ == "__main__":
    exit(NanitClient.main())
