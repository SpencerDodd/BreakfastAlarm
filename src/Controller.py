import os
import time
import ntplib
import traceback

"""
This is the controller for the BreakfastAlarm app. It has several functions:
	-alert when a specific time is reached (alarm time)
	-initiate sequence for breakfast creation
	-notify on completion via SMS (twilio)
"""

class Controller:

	def __init__(self):

		self.current_time = time.strftime('%m%d%H%M%Y.%S')

	"""
	This method polls the ntplib library and syncs the device's time with server-side
	time-keeping to account for clock drift, ensuring that the device always begins
	the breakfast sequence at the correct time.
	"""
	def sync_time_with_server(self):
		print "Syncing device clock with current time via server-side correction"
		try:

			client = ntplib.NTPClient()
			response = client.request('pool.ntp.org')
			os.system('date ' + time.strftime('%m%d%H%M%Y.%S',time.localtime(response.tx_time)))
			print('Time synced successfully.')
		except:
			print('Could not sync with time server.')
			print traceback.print_exc()

	"""
	Starts the controller.
	"""
	def start(self):
		while True:
			time.sleep(5)
			self.sync_time_with_server()