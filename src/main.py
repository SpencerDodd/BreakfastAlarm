from Controller import Controller
from AuxillaryMethods import one_directory_back, make_dir
import os
import logging
import subprocess

# root dir of application
root_dir = one_directory_back(os.getcwd())
# make the logging dir if it doesn't exist
log_dir = "{}logs/".format(root_dir)
make_dir(log_dir)
# logger for debug and output
logger = logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# handler to log to file
handler = logging.FileHandler("{}log.txt".format(log_dir))
handler.setLevel(logging.INFO)
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(handler)

# GLOBAL VARIABLES
user_id = 0
user_password = 'password'

"""
Polls the home base server and gets the breakfast profile for the device user.
"""

def get_breakfast_profile():
	logger.info("Getting breakfast profile for {}".format(user_id))
	return {"meat" : "boiled egg", "carb" : "toast", "error" : "No errors"}


"""
Main class that runs the BreakfastAlarm app.
"""

def main():
	# set up logging for the application
	
	logger.info("Starting BreakfastAlarm App for user: {}".format(user_id))

	controller = Controller(user_id, logger)
	controller.set_profile(get_breakfast_profile())
	controller.start()

if __name__ == "__main__":
	main()