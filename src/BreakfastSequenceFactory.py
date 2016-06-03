from BreakfastSequenceEggsAndToast import BreakfastSequenceEggsAndToast
from AuxillaryMethods import one_directory_back, make_dir
import os
import logging

"""
Parent class for sequences carried out by the controller. All breakfast sequences are
subclasses of Sequences
"""

class BreakfastSequenceFactory:

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

		self.name = "BreakfastSequenceFactory"

	"""
	Returns a breakfast_sequence 
	"""
	def get_sequence(self, breakfast_sequence):
		self.logger.info("Getting breakfast sequence for {}".format(breakfast_sequence))

		if breakfast_sequence['meat'] == 'boiled egg' and \
						breakfast_sequence['carb'] == 'toast':

			new_breakfast_sequence = BreakfastSequenceEggsAndToast()
			self.logger.info("Returning created {}".format(new_breakfast_sequence))
			return new_breakfast_sequence