#!/usr/bin/env python
# -*-coding:utf-8 -*-
import asyncio
import csv
import json
import logging
from io import BytesIO

import constants
import img_converter
from requests_html import AsyncHTMLSession

logger = logging.getLogger(__name__)


class DoorplateHandler:
    def __init__(self, sleep_between_requests=0):
        self.payload = constants.PAYLOAD_TEMPLATE
        self.sleep_between_requests = sleep_between_requests
        self.retry_times = 0

    @property
    def asession(self):
        return AsyncHTMLSession()

    async def request_data(self, payload):
        await asyncio.sleep(self.sleep_between_requests)

        resp = await self.asession.post(constants.TARGET_URL, data=payload)
        resp.raise_for_status()

        return resp

    async def get_captcha_img(self, captcha_key):
        """Get captcha image by captcha key from URL"""

        await asyncio.sleep(self.sleep_between_requests)

        code_img_url = constants.get_captcha_img_url(captcha_key)
        resp = await self.asession.get(code_img_url)
        resp.raise_for_status()

        content_length = resp.headers.get("Content-Length", None)
        if content_length == "0":
            logger.error("Got no data from code image url !")
            return

        return BytesIO(resp.content)

    async def get_data(self, payload=None, results=None):
        if results is None:
            results = []

        if payload is None:
            payload = self.payload

        resp = await self.request_data(payload)
        resp = resp.json()

        error_msg = json.loads(resp["errorMsg"])
        error = error_msg.get("error", False)
        token = error_msg.get("token", None)

        if error:
            captcha_key = error_msg.get("captcha", None)
            img = await self.get_captcha_img(captcha_key)

            # Convert an captcha image to string
            captcha_input = img_converter.convert(img)

            # For debug purpose
            # captcha_input = input("Please enter captcha code: ")
            captcha_data = {"captchaKey": captcha_key, "captchaInput": captcha_input}
            payload.update(captcha_data)

            if self.retry_times <= constants.RETRY_TIMES:
                self.retry_times += 1
                sleep_time = constants.get_next_request_interval()
                logger.warning(
                    f"Waiting {sleep_time}s for the {self.retry_times} retry times !"
                )
                self.sleep_between_requests = sleep_time

                # Recursively retry
                return await self.get_data(payload)

        if token:
            next_page = resp.get("page") + 1
            total_page = resp.get("total")
            data = resp.get("rows")
            results.extend(data)

            if next_page <= total_page:
                next_page_data = {"page": next_page, "token": token}
                payload.update(next_page_data)

                sleep_time = constants.get_next_request_interval()
                logger.info(f"Waiting {sleep_time}s for getting page {next_page} data")
                self.sleep_between_requests = sleep_time

                # Recursively get data
                return await self.get_data(payload)

        return results

    @staticmethod
    def save_to_csv(fp, col_names, results):
        with open(fp, "w") as csvfile:
            writer = csv.DictWriter(csvfile, col_names)
            writer.writeheader()
            for result in results:
                writer.writerow(result)

        logger.info(f"Saved {fp} successfully !")


def main():
    handler = DoorplateHandler()
    try:
        results = asyncio.run(handler.get_data())
        if results != []:
            handler.save_to_csv("./results.csv", ["v1", "v2", "V3"], results)
        else:
            logger.warning("No data parsed yet")

    except IOError:
        logger.error("I/O error")
    except Exception as err:
        logger.error(err)


if __name__ == "__main__":
    format = "%(asctime)s %(thread)d %(name)s %(levelname)s: %(message)s"
    logging.basicConfig(format=format, level=logging.DEBUG)
    main()
