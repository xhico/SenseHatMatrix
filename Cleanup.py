# -*- coding: utf-8 -*-
# !/usr/bin/python3

import os
import traceback
import SenseHatMatrix
from Misc import get911, sendEmail

if __name__ == '__main__':

    # Set logging configuration
    logger = SenseHatMatrix.logger
    sense = SenseHatMatrix.sense

    try:
        # Call the main function
        logger.info("Stopping Show")
        logger.info("Clear Sense Matrix")
        sense.clear()
    except Exception as ex:
        # Log the error and send an email notification
        logger.error(traceback.format_exc())
        sendEmail(os.path.basename(__file__), str(traceback.format_exc()))
    finally:
        # Log the end of the script
        logger.info("End")
