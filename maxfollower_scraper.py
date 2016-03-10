from urllib import request
from bs4 import BeautifulSoup
import sys
import os

print('Hello')
try:
    from gitcrawler import collect_details as detail
except:
    sys.path.append('~')
    from gitcrawler import collect_details as detail

if not os.path.exists('~/git-stats'):
    os.mkdir('~/git-stats')
filename = '~/git-stats/status.txt'
f = open(filename,'w')
try:
	max_follow_list = []
	crawl_list = []
	print(crawl_list)
	username = input('Enter a GIT-Hub username: ')
	crawl_list.append(username)
	print (crawl_list)
	count = 0
	for user in crawl_list:
		count += 1
		follower_list = detail.get_followers(user,list_flag=True)
		max_follow_list.append([detail.get_followers_number(user), user])
		for each in crawl_list:
			if each not in crawl_list:
				crawl_list.append(each)
		for each in detail.get_following(user,list_flag=True):
			if each not in crawl_list:
				crawl_list.append(each)
		print ('process #%s' % count)
		#print (crawl_list)
except:
	f.close()
finally:
	print ('Program execution successfully completed')
	print (max_follow_list)
	max_follow_list.sort(reverse=True)
	print (max_follow_list)
	for itr in range(100):
		f.write('-'*40)
		f.write('\n%-30s%-10s\n' % (max_follow_list[itr][1],max_follow_list[itr][0]))
	f.close()
	os.system('notify-send -i face-wink "Program Execution complete\nCheck for Results"')
