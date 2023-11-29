import time
import os

from instabot import Bot
from utils import downloadMediaFromUrl, getExeFromUrl, \
    extractDataFromUserForAccCreation, getUsernameBasicInfo, \
    generateSimilarIGUsername, convert_webp_to_jpg, \
    get_files_in_directory

def isAccUsable(username, password, cookies=None):
    bot = Bot(username, password, cookies=cookies)
    bot.open()
    time.sleep(10)

    if(bot.isAccountLoggedOut()):
        bot.login()
        time.sleep(5)

    if not bot.isAccountLoggedOut():
        return bot

    try:
        if(bot.isAccountIsSusspended()):
            bot.close()
            return False
    except:
        bot.close()
        return False

    bot.close()
    return False

def downloadPhotos(urls, imageNum):
    postsAbsolutePath=[]
    for index, url in enumerate(urls):
        absolutePath = f"{os.getcwd()}/data/images/{index}{imageNum}.{getExeFromUrl(url)}"
        time.sleep(2)
        downloadMediaFromUrl(url, absolutePath)
        postsAbsolutePath.append(absolutePath)
    return postsAbsolutePath


def downloadDataForNewIg(username_to_profile_info, username_to_get_images, profileNum):
    try:
        usersData = extractDataFromUserForAccCreation(username_to_get_images)
    except:
        return 0
    try:
        profile_info = getUsernameBasicInfo(username_to_profile_info)
        usersData['fullname'] = profile_info['fullname']
        usersData['bio'] = profile_info['fullname']
        usersData['username'] = profile_info['username']
    except:
        return 1

    postsAbsolutePath = downloadPhotos(usersData['postsPicUrls'], profileNum)
    profileAbsolutePath = f"{os.getcwd()}/data/images/profilePic{profileNum}.{getExeFromUrl(usersData['profilePicUrl'])}"
    downloadMediaFromUrl(usersData['profilePicUrl'], profileAbsolutePath)

    # Converting webp files into jpg
    for path in postsAbsolutePath:
        try:
            ext = path.split('.')[len(path.split('.')) - 1]
            name = path[::-1]
            name = name[:name.index('/')][::-1].split('.')[0]
            if (ext == 'webp'):
                convert_webp_to_jpg(path, f'{os.getcwd()}/data/images/{name}.jpg')
                os.system(f"rm {path}")
        except Exception as err:
            print('Err at replaceNewInfoInIG', err)
    postsAbsolutePath = [f'{os.getcwd()}/data/images/{n}' for n in get_files_in_directory('./data/images')[0:-1]]


    return {
        "usersData": usersData,
        "postsAbsolutePath": postsAbsolutePath,
        "profileAbsolutePath": profileAbsolutePath
    }


def replaceNewInfoInIG(bot,data_to_use, usernameToReplace):
    try:
        usersData = data_to_use['usersData']
        profileAbsolutePath = data_to_use['profileAbsolutePath']
        postsAbsolutePath = data_to_use['postsAbsolutePath']
        print('postsAbsolutePath',len(postsAbsolutePath))

        try:
            bot.completeProfile(usersData['fullname'], usernameToReplace, usersData['bio'], profileAbsolutePath ,postsAbsolutePath)
        except Exception as e:
            print('Err at replaceNewInfoInIG, 93', e)
            return False

        cookies = bot.getInfoForCurrentSession()
    except Exception as e:
        print('Err at replaceNewInfoInIG, 71', e)
        return False
    bot.close()
    return cookies

