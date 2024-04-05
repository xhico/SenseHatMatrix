# -*- coding: utf-8 -*-
# !/usr/bin/python3

import colorsys
import json
import logging
import os
import random
import signal
import sys
import time
import traceback

import requests
from sense_hat import SenseHat

from Misc import sendEmail


def signal_handler(sig, frame):
    if sig == signal.SIGTERM:
        logger.info("Script terminated by SIGTERM")

        logger.info("Turning off SenseHat")
        sense.clear()

        logger.info("Turning off LED Strip")
        resp = requests.post("https://monitor.rpi4.xhico/ledircontroller/btn", data={"value": "off"})
        logger.info(resp.json()["message"])

        sys.exit(0)


signal.signal(signal.SIGTERM, signal_handler)


def display_random():
    """
    Display a random pattern on the Sense HAT's LED matrix.

    This function generates random LED colors and positions, creating a dynamic display.

    Returns:
        None
    """

    # Clear the LED matrix
    sense.clear()

    start_time = time.time()
    while time.time() - start_time < config["RANDOM_DURATION"]:
        # Generate a random number of pixels to light up (between 1 and 64)
        num_pixels = random.randint(1, 64)

        for _ in range(num_pixels):
            # Generate a random LED pixel color (RGB values)
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)

            # Set a random LED pixel on the Sense HAT
            x = random.randint(0, 7)
            y = random.randint(0, 7)
            sense.set_pixel(x, y, r, g, b)

        # Pause for a short duration to display the random pixels
        time.sleep(1 / random.randint(1, 9))

        # Clear the LED matrix
        sense.clear()

    return


def display_rainbow():
    """
    Display a rainbow pattern on the Sense HAT's LED matrix.

    This function creates a moving rainbow pattern on the LED matrix.

    Returns:
        None
    """

    # Clear the LED matrix
    sense.clear()

    for i in range(1, 10, 1):

        # Adjust the speed based on iteration
        speed = config["RAINBOW_SPEED"] / i

        # Set LED color based on rainbow pattern
        for x in range(8):
            for y in range(8):
                r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb((x + y) / (8 + 8), 1, 1)]
                sense.set_pixel(x, y, r, g, b)
                time.sleep(speed)

        # Turn off LEDs
        for x in range(8 - 1, -1, -1):
            for y in range(8 - 1, -1, -1):
                sense.set_pixel(x, y, 0, 0, 0)  # Turn off LEDs
                time.sleep(speed)

        # Set LED color based on rainbow pattern
        for x in range(8 - 1, -1, -1):
            for y in range(8 - 1, -1, -1):
                r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb((x + y) / (8 + 8), 1, 1)]
                sense.set_pixel(x, y, r, g, b)
                time.sleep(speed)

        # Turn off LEDs
        for x in range(8 - 1, -1, -1):
            for y in range(8 - 1, -1, -1):
                sense.set_pixel(x, y, 0, 0, 0)
                time.sleep(speed)

    # Clear the LED matrix after the rainbow animation
    sense.clear()
    return


def main():
    """
    The main function of the script.

    This function repeatedly displays the rainbow and random patterns on the Sense HAT's LED matrix.

    Returns:
        None
    """

    logger.info("Starting Show")
    while True:
        display_rainbow()
        display_random()


if __name__ == '__main__':
    # Set logging configuration
    LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{os.path.abspath(__file__).replace('.py', '.log')}")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()])
    logger = logging.getLogger()

    # Log the start of the script
    logger.info("----------------------------------------------------")

    # Load configuration from JSON file
    configFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
    with open(configFile) as inFile:
        config = json.load(inFile)

    # Create sense hat
    sense = SenseHat()

    try:
        # Call the main function
        main()
    except Exception as ex:
        # Log the error and send an email notification
        logger.error(traceback.format_exc())
        sendEmail(os.path.basename(__file__), str(traceback.format_exc()))
    finally:
        # Log the end of the script
        sense.clear()
        logger.info("End")
