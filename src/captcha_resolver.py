#!/usr/bin/env python

import os
import sys

from pathlib import Path
from typing import AnyStr, Union

from dotenv import dotenv_values
from twocaptcha import TwoCaptcha


# extract environmental variables from .env file
config = dotenv_values(".env")


class CaptchaResolver:
    def __init__(self, resolvable_captcha: Path):
        self.resolvable_captcha: Path = resolvable_captcha

    def resolve_captcha(self) -> Union[AnyStr, None]:
        api_key = os.getenv("2CAPTCHA_API_KEY", "2CAPTCHA_PRIVATE_API_KEY")
        solver = TwoCaptcha(api_key)

        try:
            result = solver.normal(str(self.resolvable_captcha.absolute()))
            print("solved captcha: " + str(result))
            return result
        except Exception as e:
            print(f"Exception occurred: {e}")
            sys.exit(e)
