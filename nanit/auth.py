import argparse
import json
import logging
import sys

import requests

from .constants import NANIT_AUTH_FILE, NANIT_API_URL, NANIT_API_HEADERS


class NanitAuth:

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def auth(self, save_file):
        payload = {
            "email": self.email,
            "password": self.password,
        }
        response = requests.post(f'{NANIT_API_URL}/login',
                                 data=payload,
                                 headers=NANIT_API_HEADERS)
        content = response.json()

        mfa = input("Enter the MFA token:")
        payload.update({
            "chennel": "sms",
            "mfa_token": content.get("mfa_token", ""),
            "mfa_code": mfa.strip(),
        })
        response = requests.post(f'{NANIT_API_URL}/login',
                                 data=payload,
                                 headers=NANIT_API_HEADERS)

        with open(save_file, "w") as handler:
            json.dump(response.json(), handler, indent=2)

        return True

    @staticmethod
    def main():
        parser = argparse.ArgumentParser()
        parser.add_argument("-e", "--email", required=True,
                            help="email login for Nanit App")
        parser.add_argument("-p", "--password", required=True,
                            help="password for Nanit App")
        parser.add_argument("-s", "--save_file", default=NANIT_AUTH_FILE,
                            help="output file (JSON) to save the access token")
        parser.add_argument("-v", "--verbose", action="store_true",
                            help="enable verbose logging to console")
        args = parser.parse_args()

        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if args.verbose else logging.INFO)


        client = NanitAuth(args.email, args.password)
        return 0 if client.auth(args.save_file) else 1


if __name__ == "__main__":
    exit(NanitAuth.main())
