#!/usr/bin/env python

import re
import base64

from uuid import uuid4
from pathlib import Path
from typing import AnyStr
from datetime import datetime

import requests

from bs4 import BeautifulSoup
from dotenv import dotenv_values


# extract environmental variables from .env file
config = dotenv_values(".env")


class AppointmentBookingHTMLHandler:
    def __init__(self):
        self.session = requests.Session()

    def check_site_availability(self):
        try:
            r = self.session.get(config.get("CAPTCHA_URL"))
            if r.status_code in range(400, 500):
                print(f"Site is not available, status code: {r.status_code}")
                raise Exception(f"Site is not available, status code: {r.status_code}")
        except Exception as e:
            print(f"Exception occurred: {e}")
            raise Exception from e

    def extract_and_save_captcha_pic(self) -> Path:
        response = self.session.get(config.get("CAPTCHA_PAGE_URL"))
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the captcha div using style attribute
        captcha_div = soup.find("div", {"style": re.compile(r"url\(\'data:image/jpg;base64,(.*?)\'\)")})

        # Extract the base64-encoded image from the style attribute
        style_attribute = captcha_div["style"]
        base64_image = re.search(
            r"url\(\'data:image/jpg;base64,(.*?)\'\)", style_attribute
            ).group(1)
        # Save the base64 string to an image file in target directory
        captcha_unique_name = f"captcha_image_{uuid4().hex}.jpg"
        captcha_location = Path(
            Path.cwd().parents[1], config.get("CAPTCHA_IMAGE_STORING_DIR"),
            captcha_unique_name
        )
        with open(captcha_location, "wb") as image_file:
            image_file.write(base64.b64decode(base64_image))

        print(f"Captcha image extracted and saved as {captcha_unique_name}")
        return captcha_location

    def extract_appointment_datetime(self):
        response = self.session.get(config.get("APPOINTMENT_BOOKING_PAGE_URL"))
        soup = BeautifulSoup(response.content, "html.parser")
        h4elems = soup.find("div", {"id": "content"}).find_all("h4")  # todo ensure that css selector is correct

        for elem in h4elems:
            tokens = elem.text.strip().split(" ")
            date_tokens = tokens[1].split(".")
            # todo complete date element extraction and notification logic

