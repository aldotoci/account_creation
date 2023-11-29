from data.shallowIGAccs import mockUsernames
from utils_acc_c import isAccUsable, downloadDataForNewIg, replaceNewInfoInIG,\
    generateSimilarIGUsername
from utils import convertFileLinesIntoArray
from config import db
from ANDROID_IG_AC_BOT import IG_Bot

ig_bot = IG_Bot

def main(shallow_ig_acc_data: list[dict], real_usernames: list ,gender: str, tableToStore: str):
    for i, user in enumerate(shallow_ig_acc_data):
        print('i', i)
        username, password = user['username'], user['password']

        bot = isAccUsable(username, password)
        if bot == False: return False

        username_to_profile_info = real_usernames[i]
        username_to_get_images = real_usernames[i+1]

        data_to_use = downloadDataForNewIg(username_to_get_images, username_to_profile_info, 1)
        while data_to_use == 0 or data_to_use == 1:
            if data_to_use == 0:
                u_to_remove = username_to_get_images
            else:
                u_to_remove = username_to_profile_info

            print(u_to_remove, 'sth with this account')
            real_usernames.pop(real_usernames.index(u_to_remove))

            username_to_profile_info = real_usernames[i]
            username_to_get_images = real_usernames[i + 1]
            data_to_use = downloadDataForNewIg(username_to_get_images, username_to_profile_info, 1)

        usernameToReplace = generateSimilarIGUsername(username_to_profile_info)

        cookies = replaceNewInfoInIG(bot, data_to_use, usernameToReplace)

        tableToStore.insert_one({"username": usernameToReplace, "usernameToExtractInfo": username_to_get_images,
                                 "originalUsername": username_to_profile_info, "mockUsername": bot.username,
                                 "password": bot.password, "cookies": cookies, "gender": gender, "usedQuantity": 0,
                                 "currentDate": 0})

        ig_bot.reset_ip()

rappersToGetInfo = convertFileLinesIntoArray('./data/ComigIGCreation/rappers')
boysToGetInfo = convertFileLinesIntoArray('./data/ComigIGCreation/males')
girlsToGetInfo = convertFileLinesIntoArray('./data/ComigIGCreation/females')

# usernamesToStartIndexKey = "fastRappersToGetInfoStartI"
config = db.config.find_one({"name": "completeIGProfile"})
gender = 'rapper'
usernamesToStartIndex = config["fastRappersToGetInfoStartI"]
oldIndex = config["mockIgAccToStartI"]
mockIndexToStart = oldIndex-1
isRouterReseting = False
inProgressReseting = False

shallow_ig_acc_data = mockUsernames[mockIndexToStart]

main(shallow_ig_acc_data, rappersToGetInfo[usernamesToStartIndex], gender, db.newlyCreatingAcc)