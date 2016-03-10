from bs4 import BeautifulSoup
from urllib import request
import pprint

'''
Module Name
-----------
collect_details

Methods
-------
    get_username
    generate_user_url
    get_allrepo
    get_followers
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

    Example
    -------
        >> from gitcrawler import collect_details
        >> username = collect_details.get_username()
        >> url = generate_user_url(username)
    '''
    url = 'https://www.github.com/' + username
    return url

if __name__ == '__main__':
    print(generate_user_url('laxmena'))


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

    Example:
        >> from gitcrawler import collect_details
        >> collect_details.get_username()
    '''
    username = input('Enter your git-User-name: ')
    return username

if __name__ == '__main__':
    print('Gets username')
    print (get_username())

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

    Example
    -------
        >> from gitcrawler import collect_details
        >> collect_details.get_allrepo(username)
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

##if __name__ == '__main__':
##    print ('Gets all repository')
##    username = get_username()
##    pprint.pprint(get_allrepo(username))

def get_followers_number(username):
    user = username
    username = generate_user_url(username)
    url = request.urlopen(username)
    data = url.read()
    url.close()
    soup = BeautifulSoup(data)
    del data,url
    hr = '/' + user + '/followers'
    followers_list = soup.find_all('a',class_='vcard-stat',href = hr)
    followers_num = 0
    for i in followers_list:
        followers_num = i.get_text(strip=True)[:-9]
    return followers_num

if __name__ == '__main__':
    print (get_followers_number('sils1297'))

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

    Example
    -------
        >> from gitcrawler import collect_details
        >> collect_details.get_followers('laxmena')

    Example
    -------
        >> from gitcrawler import collect_details
        >> collect_details.get_followers('laxmena',list_flag = True)
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

if __name__ == '__main__':
    print('Get followers')
    username = get_username()
    pprint.pprint(get_followers(username))

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

    Example
    -------
        >> from gitcrawler import collect_details
        >> collect_details.get_following(username)
        >> collect_details.get_following(username,list_flag = True)
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

if __name__ == '__main__':
    username = get_username()
    pprint.pprint(get_following(username))


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

    Example
    -------
        >> from gitcrawler import collect_details
        >> collect_details.get_contribution(username)
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

if __name__ == '__main__':
    print ('Contribution')
    username = get_username()
    print (get_contribution(username))

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

    Example
    -------
        >> from gitcrawler import collect_details
        >> collect_details.personal_details('laxmena')
    
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

if __name__ == '__main__':
    print ('personal_details')
    username = get_username()
    print (personal_details(username))
