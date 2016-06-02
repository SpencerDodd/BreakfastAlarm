import os

"""
A list of reusable auxillary methods that can be imported to any project of interest.
Useful system-level actions translated into Python
"""

"""
Creates a given directory in the file system if it doesn't exist
"""

def make_dir(dir_to_make):
	if not os.path.exists(dir_to_make):
		print "Creating directory {0}".format(dir_to_make)
		os.makedirs(dir_to_make)
	else:
		print "Directory {} already exists.".format(dir_to_make)

"""
Returns the pwd, minus one level of depth
"""

def one_directory_back(current_directory):
	rev_dir = current_directory[::-1]
	rev_result = ''
	result = ''

	for c in rev_dir:
		if c == '/':
			rev_result += rev_dir[rev_dir.index(c):]
			result = rev_result[::-1]

			return result