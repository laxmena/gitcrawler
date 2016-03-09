import os
import sys

try:
    from gitcrawler import collect_details as detail
except:
    sys.append('/media/laxmena/Bazinga/Crawler/GIT-beta')
    from gitcrawler import collect_details as detail

count = 0
crawl_list = []
#Get initial Username from the User
username = detail.get_username()
crawl_list.append(username)

if not os.path.exists('/home/laxmena/gitcrawler'):
    os.mkdir('/home/laxmena/gitcrawler')
for i in crawl_list:
    try:
        file_name = '/home/laxmena/gitcrawler/' + i + '.txt'
        f = open(file_name,'w')
        f.write('Personal Details:\n')
        f.write('-'*50 + '\n')

        print ('Scraping Details of %s' % i)
        for itr in detail.personal_details(i):
            f.write(itr)
            f.write('\n')
        f.write('\n\nAll Repositories:\n')
        f.write('-'*50 + '\n')
        f.write('Repository Name\n')
        f.write('-'*50 + '\n')

        print ('Scraping Repository deatils of %s' % i)
        repo = detail.get_allrepo(i)
        if len(repo) == 0:
            f.write('None\n')
        else:
            for itr in repo:
                f.write(itr)
                f.write('\n')
                
        f.write('\n\nFollowers:\n')
        f.write('-'*50 + '\n')
        f.write('Username\n')
        f.write('-'*50+ '\n')
        print ('Scraping followers details of %s' % i)

        followers = detail.get_followers(i,list_flag=True)
        if len(followers) == 0:
            f.write('None\n')
        else:
            for itr in followers:
                f.write(itr)
                f.write('\n')
                if itr not in crawl_list:
                    crawl_list.append(itr)

        f.write('\n\nFollowing:\n')
        f.write('-'*50 + '\n')
        f.write('Username\n')
        f.write('-'*50 + '\n')
        
        print ('Scraping people who are following %s' % i)
        following = detail.get_following(i,list_flag=True)
        if len(following) == 0:
            f.write('None\n')
        else:
            for itr in following:
                f.write(itr)
                f.write('\n')
                if itr not in crawl_list:
                    crawl_list.append(itr)
        f.write('\n\nContribution:\n')
        f.write('-'*50 + '\n')
        f.write('%-24s%-26s\n' % ('Date','No. of Contributions'))
        f.write('-'*50 + '\n')

        print ('Scraping information about contributions by %s' % i)
        for itr in detail.get_contribution(i):
            f.write('%-24s%-26s' % (itr[0],itr[1]))
            f.write('\n')
        f.close()
        print ('Task # %d complete' % count)
        count += 1
    except:
        f.close()
