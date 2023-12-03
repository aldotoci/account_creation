import time, os

from data.shallowIGAccs import mockUsernames
from utils_acc_c import isAccUsable, downloadDataForNewIg, replaceNewInfoInIG,\
    generateSimilarIGUsername
from utils import convertFileLinesIntoArray, suspendedUsernames
from config import db
from ANDROID_IG_AC_BOT import IG_Bot
from instabot import Bot

ig_bot = IG_Bot()

def main(shallow_ig_acc_data: list[dict], real_usernames: list ,gender: str, tableToStore: str):
    print('shallow_ig_acc_data', len(shallow_ig_acc_data))
    rui = 0
    for i, user in enumerate(shallow_ig_acc_data):
        print('i', i)

        try:
            os.system('rm ./data/images/*')
        except Exception as err:
            print('err', err)

        username, password = user['username'], user['password']

        username_to_profile_info = real_usernames[rui+i]
        username_to_get_images = real_usernames[rui+i+1]

        data_to_use = downloadDataForNewIg(username_to_get_images, username_to_profile_info, 1)
        while data_to_use == 0 or data_to_use == 1:
            if data_to_use == 0:
                u_to_remove = username_to_get_images
            else:
                u_to_remove = username_to_profile_info
            rui+=1

            print(u_to_remove, 'sth with this account')
            real_usernames.pop(real_usernames.index(u_to_remove))

            username_to_profile_info = real_usernames[rui+i]
            username_to_get_images = real_usernames[rui+i + 1]
            data_to_use = downloadDataForNewIg(username_to_get_images, username_to_profile_info, 1)


        bot = isAccUsable(username, password)
        if bot == False: continue

        usernameToReplace = generateSimilarIGUsername(username_to_profile_info)

        cookies = replaceNewInfoInIG(bot, data_to_use, usernameToReplace)

        tableToStore.insert_one({"username": usernameToReplace, "usernameToExtractInfo": username_to_get_images,
                                 "originalUsername": username_to_profile_info, "mockUsername": bot.username,
                                 "password": bot.password, "cookies": cookies, "gender": gender, "usedQuantity": 0,
                                 "currentDate": 0})
        # db.config.find_one_and_update({"name": "completeIGProfile"}, {'$inc': {"mockIgAccToStartI": 1}})

        time.sleep(5)

        ig_bot.reset_ip()
        time.sleep(10)

rappersToGetInfo = convertFileLinesIntoArray('./data/ComigIGCreation/rappers')
boysToGetInfo = convertFileLinesIntoArray('./data/ComigIGCreation/males')
girlsToGetInfo = convertFileLinesIntoArray('./data/ComigIGCreation/females')

# usernamesToStartIndexKey = "fastRappersToGetInfoStartI"
config = db.config.find_one({"name": "completeIGProfile"})
gender = 'rapper'
usernamesToStartIndex = config["fastRappersToGetInfoStartI"]
shallow_ig_acc_data = mockUsernames[config["mockIgAccToStartI"]:]

main(shallow_ig_acc_data, rappersToGetInfo[usernamesToStartIndex:], gender, db.newlyCreatingAcc)

# fU = suspendedUsernames([u['username'] for u in shallow_ig_acc_data], Not=True)
# fU = [u for u in shallow_ig_acc_data if u['username'] in fU]
# open('./data/userpassF.txt', 'a').write('\n'.join([f'{u["username"]}:{u["password"]}:' for u in fU]))

# user = shallow_ig_acc_data[0]
# bot = Bot(username=user['username'], password=user['password'])
#
# bot.open()
# bot.login()
# time.sleep(2)

# bot.completeProfile(imagesPaths=[f'{os.getcwd()}/data/images/profile0.png'])
