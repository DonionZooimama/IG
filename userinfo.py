import sys

argList = sys.argv

if argList[1] == 'help':
	print('userinfo.py username [start date dd/mm/yy] [end date dd/mm/yy]')
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

	

	if startDate != None and endDate != None:
		start = startDate.split('/')[0] + startDate.split('/')[1] + startDate.split('/')[2]
		end = endDate.split('/')[0] + endDate.split('/')[1] + endDate.split('/')[2]
		for log in csvList:
			currentdate = log[0] + log[1] + log[2]
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
		start = startDate.split('/')[0] + startDate.split('/')[1] + startDate.split('/')[2]
		for log in csvList:
			currentdate = log[0] + log[1] + log[2]
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