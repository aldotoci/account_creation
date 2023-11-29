import os,time
from config import db
from data.shallowIGAccs import mockUsernames
from instabot import Bot
from utils import getUsersVideosUrl,downloadMediaFromUrl,getUsersPhotos,extractDataFromUserForAccCreation,\
    getUsernameBasicInfo,getExeFromUrl,generateSimilarIGUsername,giveIGAccountFollowersWithSMM, convert_webp_to_jpg,\
    get_files_in_directory, convertFileLinesIntoArray
from random import randint
import threading
from selenium.webdriver.common.action_chains import ActionChains
import requests

imageNum = 0
profileNum = 0

def getRightAcc(username, password, cookies=None):
    bot = Bot(username, password, cookies=cookies)
    bot.open()
    time.sleep(10)

    if(bot.isAccountLoggedOut()):
        bot.login()
        time.sleep(2)

    cookies = bot.getInfoForCurrentSession()
    try:
        if(bot.isAccountIsSusspended()):
            bot.close()
            return False
    except:
        bot.close()
        return False
    if any(cookie["name"] == "sessionid" for cookie in cookies):
        return bot
    bot.close()
    return False

def downloadPhotos(urls):
    global imageNum
    imageNum+=1
    postsAbsolutePath=[]
    for index, url in enumerate(urls):
        absolutePath = f"{os.getcwd()}/data/images/{index}{imageNum}.{getExeFromUrl(url)}"
        time.sleep(2)
        downloadMediaFromUrl(url, absolutePath)
        postsAbsolutePath.append(absolutePath)
    return postsAbsolutePath

def downloadDataForNewIg(usernameToExtract, usernameToGetFullname):
    global profileNum
    time.sleep(5)
    profileNum+=1
    try:
        usersData = extractDataFromUserForAccCreation(usernameToExtract)
    except:
        return 0
    try:
        usersData['fullname'] = getUsernameBasicInfo(usernameToGetFullname)['fullname']
    except:
        return 1

    postsAbsolutePath = downloadPhotos(usersData['postsPicUrls'])
    profileAbsolutePath = f"{os.getcwd()}/data/images/profilePic{profileNum}.{getExeFromUrl(usersData['profilePicUrl'])}"
    downloadMediaFromUrl(usersData['profilePicUrl'], profileAbsolutePath)
    return {
        "usersData": usersData,
        "postsAbsolutePath": postsAbsolutePath,
        "profileAbsolutePath": profileAbsolutePath
    }

def addImagesInAccs(usernames):
    for username in usernames:
        user = db.newlyCreatingAcc.find_one({'username': username})
        bot = Bot(username=user['username'], password=user['password'], cookies=user['cookies'])

        bot.open()

        try:
            if(bot.isAccountLoggedOut()):
                bot.login()
                db.newlyCreatingAcc.find_one_and_update({'username': username}, {'$set': {'cookies': bot.getInfoForCurrentSession()}})

            usernameToExtract = user['originalUsername']
            usernameToGetFullname = user['usernameToExtractInfo']

            data = downloadDataForNewIg(usernameToExtract, usernameToGetFullname)
            profileAbsolutePath = data['profileAbsolutePath']
            postsAbsolutePath = data['postsAbsolutePath']

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

            try:
                bot.completeProfile(profilePic=profileAbsolutePath,imagesPaths=postsAbsolutePath)
            except Exception as e:
                print('Err at replaceNewInfoInIG, 65', e)
        except Exception as err:
            print('err', err)

        bot.close()

def replaceNewInfoInIG(bot,usersData,usernameToExtractInfo,originalUsername,profileAbsolutePath,postsAbsolutePath,gender,tableToStore):
    try:
        usernameToReplace = generateSimilarIGUsername(originalUsername)
        print('postsAbsolutePath',len(postsAbsolutePath))

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

        try:
            bot.completeProfile(usersData['fullname'], usernameToReplace, usersData['bio'], profileAbsolutePath ,postsAbsolutePath)
        except Exception as e:
            print('Err at replaceNewInfoInIG, 65', e)

        cookies = bot.getInfoForCurrentSession()
        tableToStore.insert_one({"username": usernameToReplace, "usernameToExtractInfo": usernameToExtractInfo, "originalUsername": originalUsername,"mockUsername":bot.username, "password": bot.password,"cookies":cookies,"gender": gender,"usedQuantity": 0, "currentDate": 0})
    except Exception as e:
        print('Err at replaceNewInfoInIG, 71', e)
    bot.close()


# usernamesToStartIndexKey = "fastRappersToGetInfoStartI"
usernamesToStartIndexKey = "fastRappersToGetInfoStartI"
config = db.config.find_one({"name": "completeIGProfile"})
oldUsernamesToStartIndex = config[usernamesToStartIndexKey]
usernamesToStartIndex = oldUsernamesToStartIndex
oldIndex = config["mockIgAccToStartI"]
mockIndexToStart = oldIndex-1
isRouterReseting = False
inProgressReseting = False

def subMain(usernamesToGetInfoA, gender, tableToStore):
    global mockUsernames, mockIndexToStart, usernamesToStartIndex, oldUsernamesToStartIndex

    print("usernamesToStartIndex", usernamesToStartIndex)
    usernamesToGetInfo = usernamesToGetInfoA[usernamesToStartIndex: ]
    usernamesToStartIndex += 1
    usernameToGetInfoIndex = 0
    usernameToGetUsernameIndex = 1

    while True:
        mockIndexToStart+=1
        mockIgAccToCompleteProfile = mockUsernames[mockIndexToStart]

        # bot = getRightAcc(mockIgAccToCompleteProfile["username"], mockIgAccToCompleteProfile["password"], mockIgAccToCompleteProfile["cookies"])
        bot = getRightAcc(mockIgAccToCompleteProfile["username"], mockIgAccToCompleteProfile["password"])

        print('mockIndexToStart',mockIndexToStart)
        if bot != False:
            break

    data = downloadDataForNewIg(usernamesToGetInfo[usernameToGetInfoIndex], usernamesToGetInfo[usernameToGetUsernameIndex])
    while data == 0 or data == 1:
        if data == 0:
            usernameToGetInfoIndex+=1
            usernameToGetUsernameIndex+=1
            data = downloadDataForNewIg(usernamesToGetInfo[usernameToGetInfoIndex], usernamesToGetInfo[usernameToGetUsernameIndex])
        else:
            usernameToGetUsernameIndex += 1
            data = downloadDataForNewIg(usernamesToGetInfo[usernameToGetInfoIndex],usernamesToGetInfo[usernameToGetUsernameIndex])

    print("Downloaded successfully")

    try:
        usersData = data['usersData']
        profileAbsolutePath = data['profileAbsolutePath']
        postsAbsolutePath = data['postsAbsolutePath']
        originalUsername = usernamesToGetInfo[usernameToGetInfoIndex]
        usernameToExtractInfo = usernamesToGetInfo[usernameToGetUsernameIndex]

        replaceNewInfoInIG(bot,usersData,usernameToExtractInfo,originalUsername,profileAbsolutePath,postsAbsolutePath,gender,tableToStore)

    except Exception as e:
        print('err', e)

    db.config.find_one_and_update({"name": "completeIGProfile"}, {'$set': {"mockIgAccToStartI": mockIndexToStart+1, usernamesToStartIndexKey: usernamesToStartIndex+1}})

def reset_router():
    pass
    # global isRouterReseting, inProgressReseting
    #
    # isRouterReseting = True
    # inProgressReseting = True
    # p = 'LaertAldo'
    #
    # bot = Bot()
    # bot.open()
    # bot.driver.get('http://192.168.8.1/html/index.html')
    # time.sleep(3)
    #
    # actions = ActionChains(bot.driver)
    #
    # actions.send_keys(p)
    # actions.perform()
    #
    # login_button = bot.waitForElementWithText(text='Log In', element='div')
    # login_button.click()
    #
    # time.sleep(5)
    #
    # bot.driver.get('http://192.168.8.1/html/content.html#reboot')
    #
    # restartButton = bot.waitForId('reboot_apply_button')
    #
    # restartButton.click()
    #
    # cont_button = bot.waitForElementXPATH('//div[@class="btn_normal_short pull-left margin_left_12"]')
    # cont_button.click()
    #
    # time.sleep(15)
    # bot.close()
    #
    # inProgressReseting = False

def internet_on():
    global isRouterReseting,inProgressReseting
    if(inProgressReseting): return False
    try:
        response = requests.get("http://www.google.com", timeout=3)
        # If the request was successful, return True
        isRouterReseting = False
        return True if response.status_code == 200 else False
    except requests.ConnectionError:
        # If there was an error, return False
        return False

def wait_for_internet():
    while not internet_on():
        time.sleep(5)

def main(usernamesToGetInfo, gender, tableToStore):
    global imageNum, profileNum
    # Create a list to hold the thread objects
    threads = []

    for i in range(200):
        print('i', i)

        try:
            subMain(usernamesToGetInfo, gender, tableToStore)
        except Exception as err:
            print('err', err)

        time.sleep(60*5)

        # subMain(usernamesToGetInfo, gender, tableToStore)
        # imageNum = 0
        # profileNum = 0
        # try:
        #     os.system('rm ./data/images/*')
        # except:
        #     pass

        # thread = threading.Thread(target=subMain, args=(usernamesToGetInfo, gender, tableToStore))
        # thread.start()
        # threads.append(thread)
        # time.sleep(2)

        # if((i+1)%3==0):
        #     # Wait for all threads to finish
        #     for thread in threads:
        #         thread.join()
        #
        #     threads = []
        #
        #     imageNum = 0
        #     profileNum = 0
        #
        #     try:
        #         os.system('rm ./data/images/*')
        #     except:
        #         pass
        #
        #     reset_router()
        #     time.sleep(30)
        #     wait_for_internet()

        # if((i+1)%4==0):
        #     try:
        #         reset_router()
        #         time.sleep(30)
        #         wait_for_internet()
        #     except Exception as err:
        #         print('err', err)

rappersToGetInfo = convertFileLinesIntoArray('./data/ComigIGCreation/rappers')
boysToGetInfo = convertFileLinesIntoArray('./data/ComigIGCreation/males')
girlsToGetInfo = convertFileLinesIntoArray('./data/ComigIGCreation/females')


main(rappersToGetInfo, "rapper", db.native_ig_acc_creation_completed)
# main(girlsToGetInfo, "female", db.native_acc_creation_completed)
# main(rappersToGetInfo, "rapper", db.newlyCreatingAcc)
# main(girlsToGetInfo, "female", db.newlyCreatingAcc)
# main(rappersToGetInfo,  "fastRappersToGetInfoStartI1", "rapper", db.newlyCreatingAcc)
# main(boysToGetInfo,  "boysIgAccToStartI", "male", db.newlyCreatingAcc)
# main(girlsToGetInfo,  "girlsIgAccToStartI", "female", db.newlyCreatingAcc)
# loop.close()