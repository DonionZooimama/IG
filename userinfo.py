import sys
from datetime import datetime

argList = sys.argv

if len(argList) <= 1 or argList[1] == 'help':
	print('userinfo.py help\n')
	print('\tGet info from start of file to end of file')
	print('\tuserinfo.py username\n')
	print('\tGet info from start date till now')
	print('\tuserinfo.py username [start date dd/mm/yy]\n')
	print('\tGet info from start date till end date')
	print('\tuserinfo.py username [start date dd/mm/yy] [end date dd/mm/yy]\n')
	print('\tGet info from today')
	print('\tuserinfo.py username today\n')
else:
	username = argList[1]

	try:
		startDate = argList[2]
	except:
		startDate = None
	try:
		endDate = argList[3]
	except:
		endDate = None

	print ('-')*80

	directory = 'users/' + username + '/'

	f = open(directory + "logs.csv","r")

	csvList = [];
	for lines in f:
		tempList = lines.split(',')
		csvList.append(tempList)

	errors = 0
	errorsList = []
	follows = 0
	unfollows = 0

	
	if startDate == 'today' or startDate == 'Today':
		currentDateTime = str(datetime.now())
		splitBySpace = currentDateTime.split(' ')
		date = splitBySpace[0].split('-')
		year = date[0]
		month = date[1]
		day = date[2]
		start = int(date[0]) + int(date[1]) + int(date[2])

		for log in csvList:
			currentdate = int(log[0]) + int(log[1]) + int(log[2])
			if currentdate >= start:
				if log[6] == 'success':
					if log[7] == 'follow':
						follows += 1
					elif log[7] == 'unfollow':
						unfollows += 1
				else:
					errors += 1
					errorsList.append(log)
		print('From today till now\n')
		print('Followed: ' + str(follows) + ' users')
		print('Unfollowed: ' + str(unfollows) + ' users')
		print('Errors: ' + str(errors))
		if errors > 0:
			print('\nHere are the logs:')
			for error in errorsList:
				formattedDate = '['+ error[0] + '/' + error[1] + '/' + error[2] + ' ' + error[3] + ':' + error[4] + ':'+ error[5] + ']'
				print (formattedDate + "Error when action '" + error[7] + "' was preformed. Error code: " + error[8][:-1])
	elif startDate != None and endDate != None:
		start = int(startDate.split('/')[0]) + int(startDate.split('/')[1]) + int(startDate.split('/')[2])
		end = int(endDate.split('/')[0]) + int(endDate.split('/')[1]) + int(endDate.split('/')[2])
		for log in csvList:
			currentdate = int(log[0]) + int(log[1]) + int(log[2])
			if currentdate >= start and currentdate <= end:
				if log[6] == 'success':
					if log[7] == 'follow':
						follows += 1
					elif log[7] == 'unfollow':
						unfollows += 1
				else:
					errors += 1
					errorsList.append(log)
		print('From ' + startDate + ' to ' + endDate + '\n')
		print('Followed: ' + str(follows) + ' users')
		print('Unfollowed: ' + str(unfollows) + ' users')
		print('Errors: ' + str(errors))
		if errors > 0:
			print('\nHere are the logs:')
			for error in errorsList:
				formattedDate = '['+ error[0] + '/' + error[1] + '/' + error[2] + ' ' + error[3] + ':' + error[4] + ':'+ error[5] + ']'
				print (formattedDate + "Error when action '" + error[7] + "' was preformed. Error code: " + error[8][:-1])
	elif startDate != None:
		start = int(startDate.split('/')[0]) + int(startDate.split('/')[1]) + int(startDate.split('/')[2])
		for log in csvList:
			currentdate = int(log[0]) + int(log[1]) + int(log[2])
			if currentdate >= start:
				if log[6] == 'success':
					if log[7] == 'follow':
						follows += 1
					elif log[7] == 'unfollow':
						unfollows += 1
				else:
					errors += 1
					errorsList.append(log)
		print('From ' + startDate + ' till now\n')
		print('Followed: ' + str(follows) + ' users')
		print('Unfollowed: ' + str(unfollows) + ' users')
		print('Errors: ' + str(errors))
		if errors > 0:
			print('\nHere are the logs:')
			for error in errorsList:
				formattedDate = '['+ error[0] + '/' + error[1] + '/' + error[2] + ' ' + error[3] + ':' + error[4] + ':'+ error[5] + ']'
				print (formattedDate + "Error when action '" + error[7] + "' was preformed. Error code: " + error[8][:-1])
	else:
		for log in csvList:
			if log[6] == 'success':
				if log[7] == 'follow':
					follows += 1
				elif log[7] == 'unfollow':
					unfollows += 1
			else:
				errors += 1
				errorsList.append(log)
		print('From file creation till now\n')
		print('Followed: ' + str(follows) + ' users')
		print('Unfollowed: ' + str(unfollows) + ' users')
		print('Errors: ' + str(errors))
		if errors > 0:
			print('\nHere are the logs:')
			for error in errorsList:
				formattedDate = '['+ error[0] + '/' + error[1] + '/' + error[2] + ' ' + error[3] + ':' + error[4] + ':'+ error[5] + ']'
				print (formattedDate + "Error when action '" + error[7] + "' was preformed. Error code: " + error[8][:-1])

	print ('-')*80