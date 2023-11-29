import random
import time
from unittest import result
import urllib.request
import requests
import json
import enchant
import base64
from fake_useragent import UserAgent
import random
import re
from PIL import Image
import os
import string

from reqHeaders import webUserProfile, owner_media,defaultHeaders,resetPassHeaders,instaPostLikers

def shortcode_to_id(shortcode):
    code = ('A' * (12-len(shortcode)))+shortcode
    return int.from_bytes(base64.b64decode(code.encode(), b'-_'), 'big')

def convertFileLinesIntoArray(filename: str) -> list[str]:
    lines = []
    with open(filename, 'r', encoding="utf-8") as f:
        for line in f:
            lines.append(line.strip())
    return lines

def getExeFromUrl(url):
    exTention = url[0: url.index('?')]
    revString = exTention[::-1]
    exTention = revString[0:revString.index('.')]
    exTention = exTention[::-1]
    return exTention

def getUsernameData(username):
    userData = requests.get(f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}", headers=webUserProfile)

    return json.loads(userData.text)['data']['user']

def checkIfUsernameIsSuspended(username, userData=False):
    if userData == False:
        try:
            userData = getUsernameData(username)
        except: return True

    if(userData == None):
        return True
    return False

def checkIfUsernameHas0Followers(username, userData=False):
    if userData == False:
        userData = getUsernameData(username)

    followersCount = userData['edge_followed_by']['count']

    if followersCount < 100:
        return True
    return False

def checkIfUsernameHas0Posts(username, userData=False):
    if userData == False:
        userData = getUsernameData(username)

    userData = getUsernameData(username)
    mediaCount = userData['edge_owner_to_timeline_media']['count']

    if mediaCount == 0:
        return True
    return False

def checkIfUsernameHasNoLink(username, userData = False):
    if userData == False:
        userData = getUsernameData(username)

    external_url = userData['external_url']

    if external_url == None:
        return True

    if "sofianikitina" in external_url:
        return False

    return True


def checkIfUsernamePrivate(username):
    userData = getUsernameData(username)
    external_url = userData['is_private']

    return external_url

def getUsersMedia(username, length):
    userData = requests.get(
        f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}", headers=webUserProfile)

    userPics = [edge['node']['display_url'] for edge in
                json.loads(userData.text)['data']['user']['edge_owner_to_timeline_media']['edges']]
    return userPics[0: length]

    userData = json.loads(userData.text)['data']['user']

    # iguser_id = userData['id']
    # edges = []
    # end_cursor = False
    # while (len(edges) < length):
    #     if (end_cursor):
    #         mediasRes = requests.get(
    #             f"https://i.instagram.com/api/v1/feed/user/{iguser_id}/?count=12&max_id={end_cursor}", headers=owner_media())
    #     else:
    #         mediasRes = requests.get(
    #             f"https://i.instagram.com/api/v1/feed/user/{iguser_id}/?count=12", headers=owner_media())
    #     mediasRes = json.loads(mediasRes.text)
    #
    #     try:
    #         end_cursor = mediasRes['next_max_id']
    #     except:
    #         pass
    #     if('items' in mediasRes):
    #         edges.extend(mediasRes['items'])
    #     if ('more_available' not in mediasRes or mediasRes['more_available'] == False):
    #         break
    #     time.sleep(15)

    # return edges[0:length]
def getUsersVideosUrl(username, length=12):
    edges = getUsersMedia(username, length)
    videosURL = []
    for edge in edges:
        if edge['is_unified_video']:
            videosURL.append(edge['video_versions'][0]['url'])
    return videosURL
def getUsersPhotos(username, length=12):
    return getUsersMedia(username, length)
    # edges = getUsersMedia(username, length)
    # photosURL = []
    # for edge in edges:
    #     if 'image_versions2' in edge:
    #         bestVersion = edge['image_versions2']['candidates'][0]
    #         for v in edge['image_versions2']['candidates']:
    #             if (v['width'] > bestVersion['width']):
    #                 bestVersion = v
    #         photosURL.append(bestVersion['url'])
    # return photosURL
def downloadMediaFromUrl(url, name):
    try:
        urllib.request.urlretrieve(url, name)
    except Exception as e:
        print(e)

def getUsernameBasicInfo(username):
    userData = requests.get(
        f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}", headers=webUserProfile)
    userData = userData.json()['data']['user']

    time.sleep(1)
    return {
        "username": username,
        "fullname": userData['full_name'],
        "bio": userData["biography_with_entities"]["raw_text"],
        "profilePicUrl": userData["profile_pic_url_hd"],
    }

def requestUsername(username):
    userData = requests.get(
        f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}", headers=webUserProfile)
    return json.loads(userData.text)

def extractDataFromUserForAccCreation(username):
    return {
        **getUsernameBasicInfo(username),
        "postsPicUrls": getUsersPhotos(username, random.randint(5,12))
    }
def isIGUsernameAvailable(username, partToNotChange=""):
    data = f"email=&username={username}{partToNotChange}&first_name=&opt_into_one_tap=false"
    res = requests.post("https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/",data=data,headers=resetPassHeaders)
    errors = json.loads(res.text)["errors"]
    if 'username' in errors:
        return False
    return True
# def generateSimilarIGUsername(username, partToNotChange=""):
#     username = username.replace(" ", "").lower()
#     username = username[::-1]
#
#     charsToReplace = {
#         "o":{
#             'o': '0',
#             '0': 'o',
#         },
#         "O":{
#             'O': '0',
#             '0': 'O',
#         },
#         "e":{
#             'e': '3',
#             '3': 'e',
#         },
#         "E":{
#             'E': '3',
#             '3': 'E',
#         },
#         "i":{
#             'i': '1',
#             '1': 'i',
#         },
#         "I":{
#             'I': '1',
#             '1': 'I',
#         },
#         "t":{
#             't': '7',
#         },
#         "t":{
#             't': '7',
#         },
#         "b":{
#             'b': '8',
#         },
#         "z":{
#             'z': 'b',
#         },
#         "l":{
#             'l': '1',
#         },
#         "g":{
#             'g': '9',
#         },
#         "s":{
#             's': '5',
#         },
#     }
#     listOfCombinations = []
#
#     for cat in range(len(charsToReplace.keys())):
#         usernameToChange = username
#         for cat in charsToReplace:
#             for mode in range(0,2):
#                 if(mode == 1):
#                     usernameToChange = usernameToChange[::-1]
#                 for charToBeReplaced in cat:
#                     charToReplace = charsToReplace[cat][charToBeReplaced]
#                     if charToBeReplaced in usernameToChange:
#                         for _ in range(usernameToChange.count(charToBeReplaced)):
#                             usernameToChange = usernameToChange.replace(charToBeReplaced, charToReplace, 1)
#                             if(usernameToChange[::-1] not in listOfCombinations ):
#                                 listOfCombinations.append(usernameToChange[::-1])
#                         break
#
#         del charsToReplace[list(charsToReplace.keys())[0]]
#
#     for i, username in enumerate(listOfCombinations):
#         if(isIGUsernameAvailable(username,partToNotChange)):
#             return f'{username}{partToNotChange}'
#
#         if (isIGUsernameAvailable(f'{username}{partToNotChange}{i}')):
#             return f'{username}{partToNotChange}{i}'
#
#     for username in listOfCombinations:
#         for a in range(1, 999):
#             toReturn = f'{username}{partToNotChange}{a}'
#             if(isIGUsernameAvailable(toReturn)):
#                 return toReturn
#
#     username = username[::-1]
#     for a in range(1, 999):
#         toReturn = f'{username}{partToNotChange}{a}'
#         if(isIGUsernameAvailable(toReturn)):
#             return toReturn

def generateSimilarIGUsername(username):
    username = username.replace(" ", "").lower()

    similarUsername = f'{username[:6]}_{username[6:]}'

    if isIGUsernameAvailable(similarUsername):
        return similarUsername

    similarUsername = f'{username[:6]}{username[6:]}_'

    if isIGUsernameAvailable(similarUsername):
        return similarUsername


    similarUsername = f'{username[:6]}.{username[6:]}'

    if isIGUsernameAvailable(similarUsername):
        return similarUsername

    similarUsername = f'{username[:6]}.{username[6:]}_'

    if isIGUsernameAvailable(similarUsername):
        return similarUsername

    for a in range(100):
        similarUsername = f'{username[:6]}{username[6:]}{a}'

        if isIGUsernameAvailable(similarUsername):
            return similarUsername

def giveIGAccountFollowersWithSMM(username, quantity):
    api_url = "https://smmfollows.com/api/v2"
    api_key = "3f0b8e22d6c506623c55e42bd022d286"
    jsonData = {
        "key":api_key,
        "action": "add",
        "service": "1816",
        "link": f"https://www.instagram.com/{username}/",
        "quantity": quantity
    }
    res = requests.post(api_url, data=jsonData)
    print("res", res, res.text)
    return res

def getUsersMediaAll(username, length=12):
    userData = getUsernameData(username)

    iguser_id = userData['id']
    edges = []
    end_cursor = False


    while (len(edges) < length):
        if (end_cursor):
            mediasRes = requests.get(f"https://i.instagram.com/api/v1/feed/user/{iguser_id}/?count=12&max_id={end_cursor}", headers=owner_media())
        else:
            mediasRes = requests.get(f"https://i.instagram.com/api/v1/feed/user/{iguser_id}/?count=12", headers=owner_media())
        mediasRes = json.loads(mediasRes.text)

        try:
            end_cursor = mediasRes['next_max_id']
        except:
            pass
        if('items' in mediasRes):
            edges.extend(mediasRes['items'])
        if ('more_available' not in mediasRes or mediasRes['more_available'] == False):
            break
        time.sleep(15)

    return edges[0:length]

def getUsersPhotosImagesUrl(username, length=12):
    edges = getUsersMediaAll(username, length)
    photosURL = []
    for edge in edges:
        if 'image_versions2' in edge:
            bestVersion = edge['image_versions2']['candidates'][0]
            for v in edge['image_versions2']['candidates']:
                if (v['width'] > bestVersion['width']):
                    bestVersion = v
            photosURL.append(bestVersion['url'])
    return photosURL

def getPostLikers(postUrl):
    media_short_code = postUrl[28:-1]
    sessionId = "62671482041%3AJd2Kqr7zIr9xHF%3A15%3AAYfevje-EuDQUHAU5f6p8Xeb1FnrK8eRS7HgvIPtNg;"
    response = requests.get(f'https://www.instagram.com/api/v1/media/{shortcode_to_id(media_short_code)}/likers/', headers=instaPostLikers(sessionId))

    usernames = [user['username'] for user in json.loads(response.text)['users']]
    return usernames

def getPostLikersForUsername(username) -> list[str]:
    postsUrl = [F'https://www.instagram.com/p/{postData["code"]}/' for postData in getUsersMediaAll(username, 3)]
    usernamesL = [username for usernamesL in [getPostLikers(postUrl) for postUrl in postsUrl] for username in usernamesL]
    return usernamesL

def getRandomLastName() -> str:
    lastNames = convertFileLinesIntoArray('./data/last-names.txt')
    return lastNames[random.randint(0, len(lastNames)-1)]

def getRandomUserAgent() -> str:
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.3',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/114.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6,2 Safari/605.1.1',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.1 Safari/605.1.1',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.3'
    ]

    random_user_agent = user_agents[random.randint(0, len(user_agents) - 1)]
    return random_user_agent

def filterOFValidUsernames(usernames):
    d = enchant.Dict("en_US")
    filteredUsernames = []

    def checkIfListPasses(list):
        for word in list:
            if d.check(word):
                return True
        return False

    for i, username in enumerate(usernames):
        print('i', i)
        try:
            userData = getUsernameData(username)
            bio = userData['biography']
            bioWords = bio.strip().split()
            if not checkIfListPasses(bioWords):
                continue

            pronouns = userData['pronouns']
            if "she" in pronouns or "her" in pronouns:
                continue

            if userData['is_business_account'] == True or userData['is_professional_account'] == True:
                continue

            filteredUsernames.append(username)
        except Exception as err:
            open('./data/scrape/filteredOFusernames.txt', 'a').write('\n'.join(filteredUsernames))
            filteredUsernames = []
            print("err", err)

    open('./data/scrape/filteredOFusernames.txt', 'a').write('\n'.join(filteredUsernames))
    return filteredUsernames

def convert_webp_to_jpg(webp_path, jpg_path):
    try:
        # Open the WebP image
        webp_image = Image.open(webp_path)
        # Save the image in JPG format
        webp_image.convert("RGB").save(jpg_path, "JPEG")
    except Exception as e:
        print(f"Error converting: {webp_path} - {e}")

def get_files_in_directory(directory_path):
    file_list = []
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            file_list.append(filename)
    return file_list

def generateRandomNumAlphabet(length):
    # Define the characters you want to include in the random string
    characters = string.ascii_letters + string.digits  # includes both letters and numbers

    # Generate a random 20-character string
    random_string = ''.join(random.choice(characters) for _ in range(length))

    return random_string

def suspendedUsernames(usernames):
    susU = []

    for i, username in enumerate(usernames):
        print('i', i)
        if(checkIfUsernameIsSuspended(username)):
            print(username)
            susU.append(username)

    return susU