# coding=utf8
"""Tools

Useful python functions that don't belong in any specific module/package
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-03-18"

# Limit exports
__all__ = [
	'clone', 'combine', 'compare', 'eval', 'get_client_ip', 'keys_to_ints',
	'lfindi', 'lfindd', 'merge', 'without'
]

# Python imports
import sys

# Pip imports
from jobject import jobject

def clone(src):
	"""Clone

	Goes through the dict and any child dicts copying the values so that we
	don't have any references

	Arguments:
		src (dict): The source dict

	Returns:
		dict
	"""

	# Check the argument
	if not isinstance(src, dict):
		raise ValueError('%s is not a valid value for src argument of %s' % (str(src), sys._getframe().f_code.co_name))

	# Initialise the new dict
	if isinstance(src, jobject):
		dRet = jobject()
	else:
		dRet = {}

	# Get each key of the source dict
	for k in src:

		# If the key points to another dict
		if isinstance(src[k], dict):

			# Call clone on it
			dRet[k] = clone(src[k])

		# Else if the key points to a list
		elif isinstance(src[k], list):

			# Use list magic to copy it
			dRet[k] = src[k][:]

		# Else it's a standard variable
		else:
			dRet[k] = src[k]

	# Return the new dict
	return dRet

def combine(first, second):
	"""Combine

	Generates a new dict by combining the two passed, values in second will
	overwrite values in first

	Arguments:
		first (dict): The dict to be changed/overwritten
		second (dict): The dict that will do the overwriting

	Returns:
		dict
	"""

	# Make sure both arguments are actual dicts
	if not isinstance(first, dict):
		raise ValueError('%s is not a valid value for first of %s' % (str(first), sys._getframe().f_code.co_name))
	if not isinstance(second, dict):
		raise ValueError('%s is not a valid value for second of %s' % (str(second), sys._getframe().f_code.co_name))

	# Copy the first dict
	dRet = clone(first)

	# Call merge to avoid duplicate code and return the cloned dict
	return merge(dRet, second)

def compare(a: any, b: any) -> bool:
	"""Compare

	Compares two values of any type to see if they contain the same data or not

	Arguments:
		a (any): The first value
		b (any): The second value

	Returns:
		True if the same, else False
	"""

	# If they're literally the same object
	if a is b:
		return True

	# If they're both arrays
	if isinstance(a, list) and isinstance(b, list):

		# If they don't have the same length
		if len(a) != len(b):
			return False

		# Compare the values
		for i in range(len(a)):
			if not compare(a[i], b[i]):
				return False

	# Else if they're both objects
	elif isinstance(a, dict) and isinstance(b, dict):

		# If they don't have the same keys
		if not compare(sorted(a.keys()), sorted(b.keys())):
			return False

		# Compare each key
		for k in a:
			if not compare(a[k], b[k]):
				return False

	# Else, compare as is
	else:
		if a != b:
			return False

	# Return equal
	return True

def eval(src, contains):
	"""Eval(uate)

	Goes through a dict looking for keys from `contains`

	Arguments:
		src (dict): The dict we are evaluating
		contains (list): A list of values to check for, if the value is a dict
			rather than a string, expects keys to be keys pointing to further
			lists of keys

	Return:
		list | None
	"""

	# Initialise the list of errors
	lErrs = []

	# Go through each contains value
	for s in contains:

		# If the value is a string
		if isinstance(s, str):

			# If value does not exist in the source
			if s not in src or (isinstance(src[s], str) and not src[s]):
				lErrs.append(s)

		# Else, if we got a dict
		elif isinstance(s, dict):

			# Go through the key/value pairs in the dict
			for k,v in s.items():

				# If the key doesn't exist in the source or has no value
				if k not in src or not src[k]:
					lErrs.append(k)

				# Else, check the children
				else:

					# Call the eval on the child dict
					lChildErrs = eval(src[k], v)

					# Add errors to the list
					if lChildErrs:
						for sErr in lChildErrs:
							lErrs.append(k + '.' + sErr)

		# We got an unknown type of key
		else:
			lErrs.append(str(s))

	# If there's any errors
	if lErrs:
		raise ValueError(*lErrs)

def get_client_ip(environ):
	"""Get Client IP

	Returns the IP of the client based on all the environment data passed to
	the current webserver request

	Arguments:
		environ (dict): A dictionary of environment variables

	Returns:
		str
	"""

	# Init return var
	sIP	= '0.0.0.0'

	# Check common environment variables
	if 'HTTP_CLIENT_IP' in environ:
		sIP = environ['HTTP_CLIENT_IP']
	elif 'HTTP_X_CLIENTIP' in environ:
		sIP = environ['HTTP_X_CLIENTIP']
	elif 'HTTP_X_FORWARDED_FOR' in environ:
		sIP = environ['HTTP_X_FORWARDED_FOR']
	elif 'HTTP_X_RN_XFF' in environ:
		sIP = environ['HTTP_X_RN_XFF']
	elif 'REMOTE_ADDR' in environ:
		sIP = environ['REMOTE_ADDR']

	# If there's multiple IPs
	if sIP.find(','):
		lIPs = sIP.split(',')
		sIP = lIPs[-1].strip()

	# Return the IP
	return sIP

def keys_to_ints(src):
	"""Keys To Ints

	Recursively goes through a dictionary and converts all keys that are
	numeric but stored as strings to integers. Returns a new dict and doesn't
	alter the original.

	PLEASE NOTE: this method is not useful for classes, or anything complex, it
	is meant primarily for converting JSON objects which don't allow ints as
	keys. Passing a set, tuple, or iterable class will not result in the
	expected result

	Arguments:
		src (dict|list): The dict we are modifying, accepts lists in order to
							handle recursive following the data

	Returns:
		dict|list
	"""

	# If we got a dict
	if isinstance(src, dict):

		# Init the return value to an empty dict
		mRet = isinstance(src, jobject) and jobject() or {}

		# Go through the each key of the source
		for k in src:

			# Is the value numeric?
			try: mK = int(k)
			except ValueError: mK = k

			# If we got a dict or list, recurse it
			if isinstance(src[k], (dict,list)):
				mRet[mK] = keys_to_ints(src[k])

			# Else, store as is
			else:
				mRet[mK] = src[k]

	# Else, if we got a list
	elif isinstance(src, list):

		# Init the result value to a list
		mRet = []

		# Go through each item in the list
		for i in range(len(src)):

			# If we got a dict or list, recurse it
			if isinstance(src[i], (dict,list)):
				mRet.append(keys_to_ints(src[i]))

			# Else, store as is
			else:
				mRet.append(src[k])

	# Else, raise an error
	else:
		raise ValueError('src of %s must be a dict or list, received %s' % (sys._getframe().f_code.co_name, str(type(src))))

	# Return the new data
	return mRet

def lfindi(l: list, k: str, v: any) -> int:
	"""List Find Index

	Finds a specific dict in a list based on key name and value and returns its
	index. Returns -1 on failure to find

	Arguments:
		l (list): The list to search
		k (str): The key to check in each dict
		v (any): The value of the key

	Returns:
		int
	"""
	for i in range(len(l)):
		if l[i][k] == v:
			return i
	return -1

def lfindd(l: list, k: str, v: any) -> dict | None:
	"""List Find Dictionary

	Finds a specific dict in a list based on key name and value and returns it.
	Returns None on failure to find

	Arguments:
		l (list): The list to search
		k (str): The key to check in each dict
		v (any): The value of the key

	Returns:
		dict | None
	"""
	for d in l:
		if d[k] == v:
			return d
	return None

def merge(first, second):
	"""Merge

	Overwrites the first dict by adding the values from the second. Returns the
	first for chaining / ease of use

	Arguments:
		first (dict): The dict to be changed/overwritten
		second (dict): The dict that will do the overwriting

	Returns:
		dict
	"""

	# Make sure both arguments are actual dicts
	if not isinstance(first, dict):
		raise ValueError('%s is not a valid value for first of %s' % (str(first), sys._getframe().f_code.co_name))
	if not isinstance(second, dict):
		raise ValueError('%s is not a valid value for second of %s' % (str(second), sys._getframe().f_code.co_name))

	# Get each key of the second dict
	for m in second:

		# If the value is another dict and it exists in first as well
		if isinstance(second[m], dict) and m in first and isinstance(first[m], dict):

			# Call merge
			merge(first[m], second[m])

		# else we overwrite the value as is
		else:
			first[m] = second[m]

	# Return the new dict
	return first

def without(data: dict | list[dict], keys: str | list[str]) -> dict | list[dict]:
	"""Without

	Copies one or more dictionaries and returns them without the key or keys
	passed

	Arguments:
		data (dict | dict[]): The dictionary(s) to remove keys from
		keys (str | str[]): The key or keys to remove

	Returns:
		dict | dict[]
	"""

	# If we have a list
	if isinstance(data, list):

		# Init the return list
		lRet = []

		# Go through each index
		for d in data:
			lRet.append(
				without(d, keys)
			)

		# Return the new list
		return lRet

	# Else, if we have a dict
	elif isinstance(data, dict):

		# Clone the object
		dRet = clone(data)

		# If we have a single string
		if isinstance(keys, str):
			try: del dRet[keys]
			except KeyError: pass

		# Else, if we have multiple
		elif isinstance(keys, list):
			for k in keys:
				try: del dRet[k]
				except KeyError: pass

		# Else, error
		else:
			raise ValueError('keys', keys)

		# Return the new object
		return dRet

	# Else, error
	else:
		ValueError('data', data)