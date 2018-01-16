import json
import requests
from WebScraper import *

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
url_liked_post_list = 'https://www.instagram.com/graphql/query/?query_id=17864450716183058&variables={"shortcode":"%s","first":1000}'

user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 ""(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")
accept_language = 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'

def getuserid(session, user):
	try:
		url_info = url_user_info % (user)
		info = session.get(url_info)
		info = json.loads(info.text)
		return info['user']['id']
	except:
		return False

def getfollowingcount(session, user):
	try:
		url_info = url_user_info % (user)
		info = session.get(url_info)
		info = json.loads(info.text)
		return info['user']['follows']['count']
	except:
		return False

def getfollowinglist(session, id):
	try:
		url_info = url_following_list % (id)
		info = session.get(url_info)
		info = json.loads(info.text)
		tempList = info['data']['user']['edge_follow']['edges']
		returnList = []
		for user in tempList:
			returnList.append(user['node'])
		return returnList
	except:
		return False

def getuserinfo(session, user):
	try:
		url_info = url_account % (user)
		post = session.get(url_info)
		return findJson(post.text, '<script type="text/javascript">window._sharedData = ', ';</script>')
	except:
		return post.status_code

def followUser(session, id):
	try:
		url_info = url_follow % (id)
		post = session.post(url_info)
		return post.status_code
	except:
		return False

def unfollowUser(session, id):
	try:
		url_info = url_unfollow % (id)
		post = session.post(url_info)
		return post.status_code
	except:
		return False