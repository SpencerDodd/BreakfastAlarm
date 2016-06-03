from AuxillaryMethods import one_directory_back, make_dir
import os
import time
import logging

class BreakfastSequenceEggsAndToast():

	def __init__(self):
		self.logger = logging.getLogger(__name__)
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
		handler.setLevel(logging.DEBUG)
		# create a logging format
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		handler.setFormatter(formatter)
		# add the handlers to the logger
		self.logger.addHandler(handler)

		self.name = 'EggsAndToast'

	def initiate(self):
		self.logger.info("Initiating Breakfast Sequence")