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
        time.sleep(60*10)

rappersToGetInfo = convertFileLinesIntoArray('./data/ComigIGCreation/rappers')
boysToGetInfo = convertFileLinesIntoArray('./data/ComigIGCreation/males')
girlsToGetInfo = convertFileLinesIntoArray('./data/ComigIGCreation/females')

# usernamesToStartIndexKey = "fastRappersToGetInfoStartI"
config = db.config.find_one({"name": "completeIGProfile"})
gender = 'rapper'
usernamesToStartIndex = config["fastRappersToGetInfoStartI"]
# shallow_ig_acc_data = mockUsernames[config["mockIgAccToStartI"]:]

# main(shallow_ig_acc_data, rappersToGetInfo[usernamesToStartIndex:], gender, db.newfastigs)

# fU = suspendedUsernames([u['username'] for u in mockUsernames], Not=True)
fU = ['chrisinntatiehg35', 'gaatok8', 'studfinnpetasani37', 'depsushitsuducfx2023', 'uncondeoloy5k17', 'lapakates1', 'earatkoriso563', 'berhotsfushidriv7x45', 'zhioyu2', 'chrisinntatiehg35','iztreattakureowp71','didismizumbolux','proninpunex8o653','erpaupitsuminsbo72','dyspwormbojies847','menscoatsuviatg3','burrmopijicaebl54','tuifibakudianq8','maoshmineh2','sitiradabes7d43','paokamteaz7','haitrifgishimil574','sorebashibaij484','nighgingheielre5','lenohdaan32','siseno596','buddezeibrem3y4','peuswirmuchivi23','exonkukiole7','receldorisleevz79','lyidepdelb49','outalseruriasm8','meilazzokurand15','provcompiighetd35','terspopenlock8489','greatenburecon6d','moadayurp8','igsinosubreakd23','shaguz54','faucitaetran6m25','naatsezrl46','klastiominidis6w61','raibetnaiglugwy1','towetttsuoscor4z2023','sourrefourplocbi','holvaimakukiddpd1','chensbrokiripat252023','nuposthundfudrent3','ashleyisglucria74','tgegadwariqui203','neaukowneyagroww72023','alolwokarer29','kaohopansh22','lgenanmekuworkf796','perccernanipromg2','miapaniosp2023','gestyeruunvp2','alyjnyaspirhk46','adgefpakube4h24','gadowoyaglazfv88','rosatchiyapo8y7']

fU = [u for u in mockUsernames if u['username'] not in fU]
open('./data/userpassF.txt', 'a').write('\n'.join([f'{u["username"]}:{u["password"]}:' for u in fU]))

# user = shallow_ig_acc_data[0]
# bot = Bot(username=user['username'], password=user['password'])
#
# bot.open()
# bot.login()
# time.sleep(2)