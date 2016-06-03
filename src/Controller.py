from BreakfastSequenceFactory import BreakfastSequenceFactory
from AuxillaryMethods import one_directory_back, make_dir
import os
import time
import ntplib
import logging
import traceback

"""
This is the controller for the BreakfastAlarm app. It has several functions:
	-alert when a specific time is reached (alarm time)
	-initiate sequence for breakfast creation
	-notify on completion via SMS (twilio)
"""

class Controller:

	def __init__(self, user_id, logger=None):
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

		self.user_id = user_id
		self.current_date = time.strftime('%m%d%Y')
		self.current_time = time.strftime('%H%M.%S')
		self.breakfast_profile = None
		self.breakfast_sequence = None
		self.breakfast_initiated = False
		self.alarm_time = None
	"""
	This method polls the ntplib library and syncs the device's time with server-side
	time-keeping to account for clock drift, ensuring that the device always begins
	the breakfast sequence at the correct time.
	"""
	def sync_time_with_server(self):
		self.logger.info("Syncing device clock with current time via server-side correction")
		try:

			self.logger.info("Old time: {}".format(self.current_time))

			client = ntplib.NTPClient()
			response = client.request('pool.ntp.org')
			os.system('date ' + time.strftime('%m%d%H%M%Y.%S',time.localtime(response.tx_time)))
			self.current_date = time.strftime('%m%d%Y')
			self.current_time = time.strftime('%H%M.%S')

			self.logger.info("New time: {}".format(self.current_time))
			self.logger.info('Time synced successfully.')
		except Exception, e:
			self.logger.error('Failed to sync time', exc_info=True)


	"""
	Sets the breakfast profile of the current user. The profile is given in the format:
		{
			meat : eggs,
			carb : toast
		}
	"""
	def set_profile(self, breakfast_profile):
		if breakfast_profile["error"] == "No errors":
			self.logger.info("Setting breakfast_profile for user: {}".format(breakfast_profile))
			self.breakfast_profile = breakfast_profile
			self.set_alarm_time(breakfast_profile["alarm_time"])
		else:
			self.logger.debug("Could not set breakfast profile.")

	"""
	Sets the time of the alarm
	"""
	def set_alarm_time(self, new_alarm_time):
		old_alarm_time = self.alarm_time
		self.alarm_time = new_alarm_time
		self.logger.info("Alarm time changed from {} to {}".format(old_alarm_time, new_alarm_time))


	"""
	Runs all of the guts.
	"""
	def mainloop(self):
		while True:
			# if it is the time of the alarm and breakfast hasn't been made yet today,
			# initate the breakfast sequence
			if self.is_time_of_alarm() and not self.breakfast_initiated:
				self.logger.info("Initiating breakfast sequence")
				self.breakfast_initiated = True
				self.breakfast_sequence.initiate()

			# reset the breakfast_initiated variable after it cannot be triggered
			# again on the same day
			if not self.is_time_of_alarm() and self.breakfast_initiated:
				self.breakfast_initiated = False


	"""
	Checks to see if the current time is of the time of the alarm. (only checks H:M)
	"""
	def is_time_of_alarm(self):
		int_alarm = int(self.alarm_time)
		int_current_time = int(time.strftime("%H%M"))

		if int_alarm == int_current_time:
			return True

	"""
	Starts the controller. Creates a new BreakfastSequence object if there is a
	breakfast profile that has been given to the Controller.
	"""
	def start(self):
		if self.breakfast_profile is not None and self.alarm_time is not None:
			self.breakfast_sequence = BreakfastSequenceFactory().get_sequence(self.breakfast_profile)
			self.sync_time_with_server()
			self.mainloop()
		else:
			raise IllegalArgumentException("Must have a breakfast sequence to start")