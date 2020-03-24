import asyncio
import json
import logging

from pyppeteer.launcher import connect


def patch_pyppeteer():
    import pyppeteer.connection

    original_method = pyppeteer.connection.websockets.client.connect

    def new_method(*args, **kwargs):
        kwargs["ping_interval"] = None
        kwargs["ping_timeout"] = None
        return original_method(*args, **kwargs)

    pyppeteer.connection.websockets.client.connect = new_method


patch_pyppeteer()


async def scrape(ROOT_URL, DEBUG_URL, MIN_TRIES=40):
    MORE_TO_FETCH = [1] * MIN_TRIES

    async def process_response(response):
        last_more_to_fetch = getattr(process_response, "last_more_to_fetch", MIN_TRIES)

        if "conversations.history" in response.url:
            data = await response.json()

            messages = data.get("messages", [])
            for message in messages:
                message_json = json.dumps(message)
                print(message_json, flush=True)

            diff = last_more_to_fetch - len(MORE_TO_FETCH)

            MORE_TO_FETCH.extend([1] * diff)
            last_more_to_fetch = setattr(
                process_response, "last_more_to_fetch", len(MORE_TO_FETCH)
            )

    browser = await connect({"browserWSEndpoint": DEBUG_URL})
    page = await browser.newPage()
    await page.setCacheEnabled(False)
    page.on("response", process_response)

    await page.goto(ROOT_URL)

    await page.click(
        "body > div.p-client_container > div > div > div.p-workspace__primary_view"
    )

    while MORE_TO_FETCH:
        await page.keyboard.press("PageUp")
        await asyncio.sleep(0.5)
        MORE_TO_FETCH.pop(0)
        logging.error(f"{len(MORE_TO_FETCH)} more to fetch")

    logging.error("exiting")


def run_scraper(ROOT_URL, DEBUG_URL):
    asyncio.get_event_loop().run_until_complete(scrape(ROOT_URL, DEBUG_URL))
