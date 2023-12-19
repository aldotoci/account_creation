import time, os
from data.shallowIGAccs import mockUsernames
from utils_acc_c import isAccUsable, downloadDataForNewIg, replaceNewInfoInIG,\
    generateSimilarIGUsername, replaceNewInfoInIG_android, replace_usernames_android, \
    upload_images_usernames_android, make_users_private
from utils import convertFileLinesIntoArray, suspendedUsernames, checkIfUsernameIsSuspended, checkIfUsernamePrivate
from config import db
from ANDROID_IG_AC_BOT import IG_Bot

ig_bot = IG_Bot()

def sub_main(i, rui, real_usernames, user, gender, tableToStore):
    print('i', i)

    try:
        os.system('rm ./data/images/*')
    except Exception as err:
        print('err', err)

    try:
        os.system('del /Q .\data\images\*')
    except Exception as err:
        print('err', err)

    # Removing instagram data
    os.system('adb shell pm clear com.instagram.android')

    username, password = user['username'], user['password']

    username_to_profile_info = real_usernames[rui + i]
    username_to_get_images = real_usernames[rui + i + 1]

    data_to_use = downloadDataForNewIg(username_to_get_images, username_to_profile_info, 1)
    while data_to_use == 0 or data_to_use == 1:
        if data_to_use == 0:
            u_to_remove = username_to_get_images
        else:
            u_to_remove = username_to_profile_info
        rui += 1

        print(u_to_remove, 'sth with this account')
        real_usernames.pop(real_usernames.index(u_to_remove))

        username_to_profile_info = real_usernames[rui + i]
        username_to_get_images = real_usernames[rui + i + 1]
        data_to_use = downloadDataForNewIg(username_to_get_images, username_to_profile_info, 1)

    usernameToReplace = generateSimilarIGUsername(username_to_profile_info)

    print('usernameToReplace', usernameToReplace)

    cookies = replaceNewInfoInIG_android(username, password, ig_bot, data_to_use, usernameToReplace)

    tableToStore.insert_one({"username": usernameToReplace, "usernameToExtractInfo": username_to_get_images,
                             "originalUsername": username_to_profile_info, "mockUsername": username,
                             "password": password, "cookies": cookies, "gender": gender, "usedQuantity": 0,
                             "currentDate": 0})
    # db.config.find_one_and_update({"name": "completeIGProfile"}, {'$inc': {"mockIgAccToStartI": 1}})

rappersToGetInfo = convertFileLinesIntoArray('./data/ComigIGCreation/rappers')
boysToGetInfo = convertFileLinesIntoArray('./data/ComigIGCreation/males')
girlsToGetInfo = convertFileLinesIntoArray('./data/ComigIGCreation/females')

# usernamesToStartIndexKey = "fastRappersToGetInfoStartI"
config = db.config.find_one({"name": "completeIGProfile"})
gender = 'rapper'
usernamesToStartIndex = config["fastRappersToGetInfoStartI"]
shallow_ig_acc_data = mockUsernames[config["mockIgAccToStartI"]:]

def main():
    global usernamesToStartIndex
    for i, user in enumerate(mockUsernames):
        print('i', i)
        try:
            sub_main(0, 0, rappersToGetInfo[usernamesToStartIndex:], user, gender, db.newfastigs)
            usernamesToStartIndex+=1
            print('usernamesToStartIndex', usernamesToStartIndex)
        except Exception as err:
            print('Error in for user in mockUsernames: ', err)

def main_test_1():
    users = db.newfastigs.find()
    usernamesToF = ['gismonditennant', 'lavonneanderton', 'aureadelce', 'tyneraline', 'yukocerasi', 'odelia.zin', 'carmeliamender', 'krah.aretha', 'tomekamierzwa', 'melainepentaris', 'sharicesibille', 's ynthiayeakle', 'valentinebekius', 'kourtneydulemba', 'oniemermelstein', 'jacklinbeverley', 'edrisdecourt', 'senaidamccardell', 'langrameres', 'twilagrams', 'majkaella', 'margheritadorr', 'leanaplassmeyer', 'linnemanncecille', 'gaykolassa', 'sha.footer', 'cheriselucey', 'nievesmency', 'celinebrummitt', 'audracafferty']
    users = [user for user in users if user['mockUsername'] in usernamesToF]
    for i, user in enumerate(users):
        print('i', i)
        try:
            usernameToReplace = generateSimilarIGUsername(user['originalUsername'])
            print('usernameToReplace', usernameToReplace)
            data_to_use = downloadDataForNewIg(user['usernameToExtractInfo'], user['originalUsername'], 1)
            replace_usernames_android(user, ig_bot, usernameToReplace, data_to_use['usersData']['fullname'], data_to_use['usersData']['bio'])
            db.newfastigs.find_one_and_update({'username': user['username']}, {'$set': {'username':  usernameToReplace}})
        except Exception as err:
            print('Error in main_test_1: ', err)

def main_test_2():
    users = [*db.newfastigs.find().skip(44).limit(64)]
    # usernamesToF = ['gismonditennant', 'lavonneanderton', 'aureadelce', 'tyneraline', 'yukocerasi', 'odelia.zin', 'carmeliamender', 'krah.aretha', 'tomekamierzwa', 'melainepentaris', 'sharicesibille', 's ynthiayeakle', 'valentinebekius', 'kourtneydulemba', 'oniemermelstein', 'jacklinbeverley', 'edrisdecourt', 'senaidamccardell', 'langrameres', 'twilagrams', 'majkaella', 'margheritadorr', 'leanaplassmeyer', 'linnemanncecille', 'gaykolassa', 'sha.footer', 'cheriselucey', 'nievesmency', 'celinebrummitt', 'audracafferty']
    # users = [user for user in users if user['mockUsername'] in usernamesToF]
    for i, user in enumerate(users):
        try: os.system('rm ./data/images/*')
        except Exception as err: print('err', err)
        try: os.system('del /Q .\data\images\*')
        except Exception as err:print('err', err)
        print('i', i)
        try:
            data_to_use = downloadDataForNewIg(user['usernameToExtractInfo'], user['originalUsername'], 1)
            upload_images_usernames_android(user, ig_bot, data_to_use['profileAbsolutePath'], data_to_use['postsAbsolutePath'])
        except Exception as err: print('Error in main_test_1: ', err)

def main_test_3():
    users = mockUsernames[382:]
    sus = suspendedUsernames(['chrisinntatiehg35', 'gaatok8', 'studfinnpetasani37', 'depsushitsuducfx2023', 'uncondeoloy5k17', 'lapakates1', 'earatkoriso563', 'berhotsfushidriv7x45', 'zhioyu2', 'chrisinntatiehg35','iztreattakureowp71','didismizumbolux','proninpunex8o653','erpaupitsuminsbo72','dyspwormbojies847','menscoatsuviatg3','burrmopijicaebl54','tuifibakudianq8','maoshmineh2','sitiradabes7d43','paokamteaz7','haitrifgishimil574','sorebashibaij484','nighgingheielre5','lenohdaan32','siseno596','buddezeibrem3y4','peuswirmuchivi23','exonkukiole7','receldorisleevz79','lyidepdelb49','outalseruriasm8','meilazzokurand15','provcompiighetd35','terspopenlock8489','greatenburecon6d','moadayurp8','igsinosubreakd23','shaguz54','faucitaetran6m25','naatsezrl46','klastiominidis6w61','raibetnaiglugwy1','towetttsuoscor4z2023','sourrefourplocbi','holvaimakukiddpd1','chensbrokiripat252023','nuposthundfudrent3','ashleyisglucria74','tgegadwariqui203','neaukowneyagroww72023','alolwokarer29','kaohopansh22','lgenanmekuworkf796','perccernanipromg2','miapaniosp2023','gestyeruunvp2','alyjnyaspirhk46','adgefpakube4h24','gadowoyaglazfv88','rosatchiyapo8y7'])
    print(sus)

def main_test_4():
    # for i, user in enumerate([*db.newfastigs.find().skip(44)]):
    #     print(i)
    #     isUS = checkIfUsernamePrivate(user['username'])
    #     print(user['username'], isUS)
    print([*db.newfastigs.find().skip(44)][0]['username'])

def main_test_5():
    for user in [*db.newfastigs.find().limit(40)]:
        make_users_private(user, ig_bot)

main_test_2()

# main_test_2()

# ig_bot.getXmlHierchy()

# ig_bot.open_and_share_img()

# for i, user in enumerate(shallow_ig_acc_data):
#     print('i',i)
#     if not checkIfUsernameIsSuspended(user["username"]):
#         open('./data/userpassF.txt', 'a').write(f'{user["username"]}:{user["password"]}:\n')

