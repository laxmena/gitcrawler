import os
import sys
from bs4 import BeautifulSoup
from urllib import request
import pprint

'''
Methods
-------
    get_username
    generate_user_url
    get_allrepo
    get_followers
    get_following
    get_contrribution
'''

#Generates Github for the given Username
def generate_user_url(username):
    '''
    Method
    ------
    generate_user_url(username)

    Parameters
    ----------
    username                :       GitHub User name

    Return
    ------
    String

    Function
    --------
    generates GitHub URL for the given username

    '''
    url = 'https://www.github.com/' + username
    return url

#Get github username from user
def get_username():
    '''
    Method
    ------
    get_username():

    Parameters
    ----------
    None

    Return
    ------
    String

    Function
    --------
    Gets the Username from the user
    '''
    username = input('Enter your git-User-name: ')
    return username

#Retrives all repositories associated with the Given u
def get_allrepo(username):
    '''
    Method
    ------
    get_allrepo(username)

    Parameters
    ----------
    username                :       Gets GitHub username

    Return
    ------
    list                    :       list of all Repositories names associated
                                    with the given username

    Function
    --------
    Get all the Repositories associated with the user
    '''
    repository = []
    username += '?tab=repositories'
    url = request.urlopen(generate_user_url(username))
    data = url.read()
    url.close()
    soup = BeautifulSoup(data)
    repo_list = soup.find_all('a',itemprop ="name codeRepository")
    for repo in repo_list:
        repository.append(repo.get_text(strip = True))
    del repo_list
    return repository

def get_followers(username,list_flag=False):
    '''
    Method
    ------
    get_followers(username)

    Parameters
    ----------
    username                :       GitHub Username
    list_flag               :       Flag to indicate the return type
                                    True for List
                                    Flase for Dict

    Function
    --------
    Gets username of all the followers of the given user

    Return
    ------
    List of followers name 'string' for the given user or
    Dictionary of Followers name and username as key and value
    '''
    username += '/followers'
    url = request.urlopen(generate_user_url(username))
    data = url.read()
    url.close()
    soup = BeautifulSoup(data)
    del data,url
    followers_list = soup.find_all('h3',class_ = "follow-list-name")
    if list_flag == False:
        followers = {}
        for name in followers_list:
            followers[name.get_text(strip = True)] = name.find('a').get('href')[1:]
    else:
        followers = []
        for name in followers_list:
            followers.append(name.find('a').get('href')[1:])
    return followers

def get_following(username,list_flag = False):
    '''
    Method
    ------
    get_following(username)

    Parameters
    ----------
    username                :       GitHub Username
    list_flag               :       Flag to indicate the return type
                                    True for List
                                    Flase for Dict

    Function
    --------
    Gets username of all the accounts that the user follows

    Return
    ------
    List of usernames 'string' that the given user follows if list_flag is True.
    Dictionay of User's real name and his Github username as key and value.

    '''
    username += '/following'
    url = request.urlopen(generate_user_url(username))
    data = url.read()
    url.close()
    soup = BeautifulSoup(data)
    del data,url
    following_list = soup.find_all('h3',class_ = "follow-list-name")
    if list_flag == False:
        following = {}
        for name in following_list:
            following[name.get_text(strip = True)] = name.find('a').get('href')[1:]
    else:
        following = []
        for name in following_list:
            following.append(name.find('a').get('href')[1:])
    return following


def get_contribution(username):
    '''
    Method
    ------
    get_contribution(username)

    Parameters
    ----------
    usernames                   :          GitHub username

    Function
    --------
    Retrives the contribution details about the user

    Return
    ------
    List of tuples containing Date and Number of contributions of the given
    user

    '''
    username = generate_user_url(username)
    url = request.urlopen(username)
    data = url.read()
    url.close()
    soup = BeautifulSoup(data)
    contribution = []
    contribution_details = soup.find_all('rect',
                                         class_= 'day',
                                         width='11',
                                         height='11')
    contribution_details_active = soup.find_all('rect',
                                                class_= 'day active',
                                                width='11',
                                                height='11')
    contribution_details += contribution_details_active
    del contribution_details_active
    for contribute in contribution_details:
        num_of_c = contribute.get('data-count')
        date = contribute.get('data-date')
        if num_of_c != '0':
            temp_tuple = (date, num_of_c)
            contribution.append(temp_tuple)
    del data,url, contribution_details, soup
    return contribution


def personal_details (username):
    '''
    Method
    ------
    personal_details(username)

    Parameters
    ----------
    usernames                   :          GitHub username

    Function
    --------
    Retrives basic information of the user from the user's Github page

    Return
    ------
    List containing the details about the user
    
    '''
    username = generate_user_url(username)
    url = request.urlopen(username)
    data = url.read()
    url.close()
    soup = BeautifulSoup(data)
    details_list = []
    name = soup.find('div',class_='vcard-fullname',itemprop='name').get_text()
    details_list.append(name)
    details = soup.find_all('li',class_ = 'vcard-detail py-1 css-truncate \
                            css-truncate-target')
    for each in details:
        details_list.append(each.get_text(strip = True))
    del url, username, data,soup, name, details
    return details_list




count = 0
crawl_list = []
#Get initial Username from the User
username = get_username()
crawl_list.append(username)

if not os.path.exists('~/gitcrawler'):
    os.mkdir('~/gitcrawler')
for i in crawl_list:
    try:
        file_name = '~/gitcrawler/' + i + '.txt'
        f = open(file_name,'w')
        f.write('Personal Details:\n')
        f.write('-'*50 + '\n')

        print ('Scraping Details of %s' % i)
        for itr in personal_details(i):
            f.write(itr)
            f.write('\n')
        f.write('\n\nAll Repositories:\n')
        f.write('-'*50 + '\n')
        f.write('Repository Name\n')
        f.write('-'*50 + '\n')

        print ('Scraping Repository deatils of %s' % i)
        repo = get_allrepo(i)
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

        followers = get_followers(i,list_flag=True)
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
        following = get_following(i,list_flag=True)
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
        for itr in get_contribution(i):
            f.write('%-24s%-26s' % (itr[0],itr[1]))
            f.write('\n')
        f.close()
        print ('Task # %d complete' % count)
        count += 1
    except:
        f.close()
