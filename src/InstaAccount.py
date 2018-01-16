import requests
import time
import json
import random
from datetime import datetime
import smtplib
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

from WebScraper import *
from instalib import *

class Account(threading.Thread):

	url = 'https://www.instagram.com/'
	url_tag = 'https://www.instagram.com/explore/tags/%s/?__a=1'
	url_likes = 'https://www.instagram.com/web/likes/%s/like/'
	url_unlike = 'https://www.instagram.com/web/likes/%s/unlike/'
	url_comment = 'https://www.instagram.com/web/comments/%s/add/'
	url_follow = 'https://www.instagram.com/web/friendships/%s/follow/'
	url_unfollow = 'https://www.instagram.com/web/friendships/%s/unfollow/'
	url_login = 'https://www.instagram.com/accounts/login/ajax/'
	url_logout = 'https://www.instagram.com/accounts/logout/'
	url_media_detail = 'https://www.instagram.com/p/%s/?__a=1'
	url_user_info = 'https://www.instagram.com/%s/?__a=1'
	url_account = 'https://www.instagram.com/%s/'

	url_following_list = 'https://www.instagram.com/graphql/query/?query_id=17874545323001329&variables={"id":%s,"first":9999}'
	url_liked_post_list = 'https://www.instagram.com/graphql/query/?query_id=17864450716183058&variables={"shortcode":"%s","first":200}'

	user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 ""(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")
	accept_language = 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'

	def __init__(self, username, password, targetAudience, followPerHour, unfollowPerHour, minFollowing, maxFollowingPerDay):
		threading.Thread.__init__(self)

		self.username = username.lower()
		self.password = password
		self.targetAudience = targetAudience
		self.id = None

		self.accountStatus = False
		self.accountSuspended = False

		self.minFollowing = minFollowing
		self.maxFollowingPerDay = maxFollowingPerDay
		self.followingCount = 0
		self.dayFollowingCount = 0

		self.followTimer = 3600 / followPerHour
		self.unfollowTimer = 3600 / unfollowPerHour
		self.suspendedUnfollowTimer = int(self.unfollowTimer * 3)
		self.suspentionTimer = 3600
		self.refreshTimer = 3600

		self.currentFollowTimer = 99999999
		self.currentUnfollowTimer = 99999999
		self.currentSuspentionTimer = 0
		self.currentRefreshTimer = 0

		self.followIndex = 0
		self.unfollowIndex = 0

		self.followList = []
		self.unfollowList = []

		self.targetAccounts = self.getTargetAccounts()

		self.directory = 'users/' + self.username + '/'

		if not os.path.exists(self.directory):
			os.makedirs(self.directory)

		self.session = requests.Session()
		self.login()
	
	def run(self):
		while True:
			current_hour = self.gethour()
			if current_hour >= 8 and current_hour <= 24:
				start = time.time()
				
				if self.accountStatus:
					self.update()
				else:
					self.login()

				time.sleep(1)

				self.updateTimer(start)
			else:
				if self.dayFollowingCount != 0:
					self.dayFollowingCount = 0
				if self.currentFollowTimer <= 9999:
					self.currentFollowTimer = 9999
				if self.currentUnfollowTimer != 9999:
					self.currentUnfollowTimer = 9999
				if self.accountSuspended == True:
					self.accountSuspended = False
				time.sleep(3600)

	def login(self):
		tempLog = ('-'*80) + '\n%s[%s] Attempting to login' % (self.getTimeStamp(), self.username)
		self.writeLog(tempLog)

		self.session.cookies.update({
			'sessionid': '',
			'mid': '',
			'ig_pr': '1',
			'ig_vw': '1920',
			'csrftoken': '',
			's_network': '',
			'ds_user_id': ''
		})
		self.login_post = {
			'username': self.username,
			'password': self.password
		}
		self.session.headers.update({
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': self.accept_language,
			'Connection': 'keep-alive',
			'Content-Length': '0',
			'Host': 'www.instagram.com',
			'Origin': 'https://www.instagram.com',
			'Referer': 'https://www.instagram.com/',
			'User-Agent': self.user_agent,
			'X-Instagram-AJAX': '1',
			'X-Requested-With': 'XMLHttpRequest'
		})
		r = self.session.get(self.url)
		self.session.headers.update({'X-CSRFToken': r.cookies['csrftoken']})
		time.sleep(0.1)
		login = self.session.post(self.url_login, data=self.login_post, allow_redirects=True)
		self.session.headers.update({'X-CSRFToken': login.cookies['csrftoken']})
		self.csrftoken = login.cookies['csrftoken']
		time.sleep(0.1)

		if login.status_code == 200:
		    r = self.session.get('https://www.instagram.com/')
		    finder = r.text.find(self.username)
		    if finder != -1:
		        self.id = getuserid(self.session, self.username)
		        self.followingCount = int(getfollowingcount(self.session, self.username))
		        self.accountStatus = True
		        tempLog = '%s[%s] Login successful' % (self.getTimeStamp(), self.username)
		        self.writeLog(tempLog)
		    else:
		        self.accountStatus = False
		        tempLog = '%s[%s] !!!Login error, Incorrect login info!!!' % (self.getTimeStamp(), self.username)
		        self.sendEmail(tempLog)
		        self.writeLog(tempLog)
		else:
			tempLog = "%s[%s] !!!Login error, Connection error!!!" % (self.getTimeStamp(), self.username)
			self.sendEmail(tempLog)
			self.writeLog(tempLog)

	def getTimeStamp(self):
		currentDateTime = str(datetime.now())
		splitBySpace = currentDateTime.split(' ')
		date = splitBySpace[0].split('-')
		year = date[0]
		month = date[1]
		day = date[2]

		date = month + '/' + day + '/' + year
		time = splitBySpace[1].split('.')[0]
		
		return '[' + date + " " + time + ']'

	def gethour(self):
		currentDateTime = str(datetime.now())
		splitBySpace = currentDateTime.split(' ')

		time = splitBySpace[1].split('.')[0]
		hour = time.split(':')[0]
		
		return int(hour)

	def writeLog(self, data):
		try:
			print data
			f = open(self.directory + "logs.txt","a")
			f.write(data + '\n')
			f.close()
		except:
			f = open(self.directory + "logs.txt","w") 
			f.close()
			self.writeLog(data)

	def writeCSV(self, status, event, data):
		try:
			currentDateTime = str(datetime.now())
			splitBySpace = currentDateTime.split(' ')
			date = splitBySpace[0].split('-')
			time = splitBySpace[1].split('.')[0]
			time = time.split(':')

			# day, month, year, hours, minutes, seconds, event
			log = str(date[2]) + ',' + str(date[1]) + ',' + str(date[0]) + ',' + str(time[0]) + ',' + str(time[1]) + ',' + str(time[2]) + ',' + status + ',' + event + ',' + data

			f = open(self.directory + "logs.csv","a")
			f.write(log + '\n')
			f.close()
		except:
			f = open(self.directory + "logs.csv","w") 
			f.close()
			self.writeCSV(status, event, data)

	def writePreviouslyFollowed(self, data):
		f = open(self.directory + "previous_user.txt","a")
		f.write(data + '\n')
		f.close()

	def previouslyFollowed(self, user):
		try:
			f = open(self.directory + "previous_user.txt","r") 
			tempList = []
			for line in f: 
				 if user == line[:-1]:
					f.close()
					return True

			f.close()
			return False
		except:
			f = open(self.directory + "previous_user.txt","w") 
			return False
		

	def sendEmail(self, log):
		mail = smtplib.SMTP('smtp.gmail.com', 587)
		mail.starttls()
		mail.login('daniel.ziorli@gmail.com', 'CandyZ1999')

		msg = MIMEMultipart()
		msg['From'] = 'daniel.ziorli@gmail.com'
		msg['To'] = 'daniel.ziorli@gmail.com'
		msg['Subject'] = 'Instagram Server Status Update'

		msg.attach(MIMEText(log, 'plain'))
		text = msg.as_string()

		mail.sendmail('daniel.ziorli@gmail.com', 'daniel.ziorli@gmail.com', text)
		mail.close()

	def getTargetAccounts(self):
		f = open("src/TargetAudiences/" + self.targetAudience + ".txt","r") 
		tempList = []
		for line in f: 
			 tempList.append(line[:-1])
		return tempList

	def getMediaLikersList(self, id):
		try:
			r = random.randrange(len(self.targetAccounts)-1)

			url_info = self.url_account % (self.targetAccounts[r])
			data = self.session.get(url_info)
			data = findJson(data.text, '<script type="text/javascript">window._sharedData = ', ';</script>')
			code = data['entry_data']['ProfilePage'][0]['user']['media']['nodes'][0]['code']
			
			url_info = self.url_liked_post_list % code
			data = self.session.get(url_info)
			data = json.loads(data.text)
			tempList = data['data']['shortcode_media']['edge_liked_by']['edges']

			returnList = []
			for user in tempList:
				returnList.append(user['node'])

			return returnList
		except:
			tempLog = "%s[%s] !!!Error getting media likers list connection timed out!!!" % (self.getTimeStamp(), self.username)
			self.writeLog(tempLog)
			self.accountStatus = False
			return None

	def followsequence(self):
		if self.dayFollowingCount < self.maxFollowingPerDay:
			current_user = self.followList[self.followIndex]
			user_status = self.canfollow(current_user)

			if user_status:
				follow_request = followUser(self.session, current_user['id'])
				if follow_request == 200:
					tempLog = "%s[%s] Successfully followed user: %s" % (self.getTimeStamp(), self.username, current_user['username'])
					self.writeLog(tempLog)
					self.writeCSV('success', 'follow', current_user['username'])
					self.writePreviouslyFollowed(current_user['username'])
					self.followingCount += 1
					self.followIndex += 1
					self.currentFollowTimer = 0
				else:
					if follow_request == 400:
						self.accountSuspended = True
						tempLog = "%s[%s] !!!Error following user: %s Error code: %s !!!" % (self.getTimeStamp(), self.username, current_user['username'], str(follow_request))
						self.writeLog(tempLog)
						self.writeCSV('error', 'follow', str(follow_request))
						self.sendEmail(tempLog)
					else:
						tempLog = "%s[%s] !!!Error following user: %s Error code: %s!!!" % (self.getTimeStamp(), self.username, current_user['username'], str(follow_request))
						self.writeLog(tempLog)
						self.writeCSV('error', 'follow', str(follow_request))
						self.sendEmail(tempLog)

	def unfollowsequence(self):
		if self.followingCount >= self.minFollowing:
			current_user = self.unfollowList[self.unfollowIndex]
			unfollow_request = unfollowUser(self.session, current_user['id'])
			if unfollow_request == 200:
				tempLog = "%s[%s] Successfully unfollowed user: %s" % (self.getTimeStamp(), self.username, current_user['username'])
				self.writeLog(tempLog)
				self.writeCSV('success', 'unfollow', current_user['username'])
				self.followingCount -= 1
				self.currentUnfollowTimer = 0
				self.unfollowIndex += 1
			else:
				tempLog = "%s[%s] !!!Error unfollowing user: %s Error code: %s!!!" % (self.getTimeStamp(), self.username, current_user['username'], str(unfollow_request))
				self.writeLog(tempLog)
				self.writeCSV('error', 'unfollow', str(unfollow_request))
				self.sendEmail(tempLog)
				self.currentUnfollowTimer = 0

	def getnewfollowlist(self):
		self.followList = self.getMediaLikersList(self.id)
		self.followIndex = 0

	def getnewunfollowlist(self):
		self.unfollowList = getfollowinglist(self.session, self.id)
		self.unfollowList = self.unfollowList[::-1]
		self.unfollowIndex = 0

	def canfollow(self, user):
		info = getuserinfo(self.session, user['username'])
		try:
			followers = info['entry_data']['ProfilePage'][0]['user']['followed_by']['count']
		except:
			empLog = "%s[%s] !!!Error checking if user can be followed: %s!!!" % (self.getTimeStamp(), self.username, user['username'])
			self.writeLog(tempLog)
			self.writeCSV('error', 'canfollow', str(info))
			self.sendEmail(tempLog)
			return False

		if user['followed_by_viewer'] or user['requested_by_viewer']:
			tempLog = "%s[%s] Already following user: %s" % (self.getTimeStamp(), self.username, user['username'])
			self.writeLog(tempLog)
			self.followIndex += 1
		elif self.previouslyFollowed(user['username']):
			tempLog = "%s[%s] %s has been followed before" % (self.getTimeStamp(), self.username, user['username'])
			self.writeLog(tempLog)
			self.followIndex += 1
		elif user['is_verified'] == True or followers > 2000:
			tempLog = "%s[%s] %s is verified or is a big account" % (self.getTimeStamp(), self.username, user['username'])
			self.writeLog(tempLog)
			self.followIndex += 1
		else:
			return True

	def refresh(self):
		self.followingCount = int(getfollowingcount(self.session, self.username))

	def update(self):
		if self.currentRefreshTimer > self.refreshTimer:
			self.refresh()

		if self.accountSuspended == False:
			if self.followIndex >= len(self.followList) - 1:
				self.getnewfollowlist()

			if self.currentFollowTimer > self.followTimer:
				self.followsequence()

			if self.unfollowIndex >= len(self.unfollowList) - 1:
				self.getnewunfollowlist()

			if self.currentUnfollowTimer > self.unfollowTimer:
				self.unfollowsequence()

		else:
			if self.unfollowIndex >= len(self.unfollowList) - 1:
				self.getnewunfollowlist()

			if self.currentUnfollowTimer > self.suspendedUnfollowTimer:
				self.unfollowsequence()
							
		if self.accountSuspended == True and self.currentSuspentionTimer > self.suspentionTimer:
			self.accountSuspended = False
			self.currentSuspentionTimer = 0



	def updateTimer(self, startTime):
		time_to_add = (time.time() - startTime)
		self.currentFollowTimer += time_to_add
		self.currentUnfollowTimer += time_to_add
		self.currentRefreshTimer += time_to_add
		if self.accountSuspended:
			self.currentSuspentionTimer += time_to_add