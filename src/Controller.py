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
		self.user_id = user_id
		self.current_date = time.strftime('%m%d%Y')
		self.current_time = time.strftime('%H%M.%S')
		self.logger = logger or logging.getLogger(__name__)

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
			logger.error('Failed to sync time', exc_info=True)


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
		else:
			self.logger.debug("Could not set breakfast profile.")

	def set_alarm_time(self):
		old_alarm_time = self.alarm_time
		new_alarm_time = '0600'
		self.alarm_time = new_alarm_time
		self.logger.info("Alarm time changed from {} to {}".format(old_alarm_time, new_alarm_time))


	"""
	Runs all of the guts.
	"""
	def mainloop(self):
		pass


	"""
	Starts the controller.
	"""
	def start(self):
		self.sync_time_with_server()
		self.mainloop()