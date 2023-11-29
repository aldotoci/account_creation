import time
import random
import urllib.request
import requests
import os
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.firefox.options import Options

from datetime import datetime

from reqHeaders import uploadProfilePic, commentPostHeaders, instaEditProfile, webUserProfile, web_form_data, \
    rupload_igphoto, media_configure
from utils import getExeFromUrl, getRandomUserAgent

chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
         'w', 'x', 'y', 'z']

class Bot:
    def __init__(self, username="", password="", comments=None, positive=True, cookies=None):
        if cookies is None:
            cookies = []
        if comments is None:
            comments = []
        self.username = username
        self.password = password
        self.comments = comments
        self.positive = positive
        self.cookies = cookies

    def waitForId(self, ID, time=10, parent_element: WebElement = None) -> WebElement:
        if (parent_element == None):
            parent_element = self.driver

        wait = WebDriverWait(parent_element, time)
        return wait.until(ec.visibility_of_element_located((By.ID, ID)))

    def waitForElementXPATH(self, elementAddress, time=10, parent_element: WebElement = None) -> WebElement:
        if (parent_element == None):
            parent_element = self.driver

        wait = WebDriverWait(parent_element, time)
        return wait.until(ec.visibility_of_element_located((By.XPATH, elementAddress)))

    def waitForElementsXPATH(self, elementAddress, time=10, parent_element: WebElement = None) -> list[WebElement]:
        if (parent_element == None):
            parent_element = self.driver

        wait = WebDriverWait(parent_element, time)
        return wait.until(ec.visibility_of_all_elements_located((By.XPATH, elementAddress)))

    def waitForElementCSS_Selectori(self, elementAddress, time=10, parent_element: WebElement = None) -> WebElement:
        if (parent_element == None):
            parent_element = self.driver

        wait = WebDriverWait(parent_element, time)
        return wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, elementAddress)))

    def waitForClass(self, className, time=10, parent_element: WebElement = None) -> WebElement:
        if (parent_element == None):
            parent_element = self.driver

        wait = WebDriverWait(parent_element, time)
        return wait.until(ec.visibility_of_element_located((By.CLASS_NAME, className)))

    def waitForClases(self, className, time=10, parent_element: WebElement = None) -> list[WebElement]:
        if (parent_element == None):
            parent_element = self.driver

        wait = WebDriverWait(parent_element, time)
        return wait.until(ec.visibility_of_all_elements_located((By.CLASS_NAME, className)))

    def send_text_in_browser(self, text):
        actions = ActionChains(self.driver)
        actions.send_keys(text)  # Simulate Ctrl+T command
        actions.perform()

    def waitForElementWithText(self, text, element='*', parent_element: WebElement = None, time=10) -> WebElement:
        if (parent_element == None):
            parent_element = self.driver

        return self.waitForElementXPATH(f'//{element}[text()="{text}"]', time=time, parent_element=parent_element)

    def login(self):
        """
            Logs in instagram account.
            (Webdriver needs to have been created.(Done by creating either open() or run()))
        """

        self.driver.get("https://www.instagram.com/")
        time.sleep(5)
        user_name_elem = self.waitForElementXPATH("//input[@name='username']")
        user_name_elem.clear()
        user_name_elem.send_keys(self.username)
        passwarword_elem = self.waitForElementXPATH("//input[@name='password']")
        passwarword_elem.clear()
        passwarword_elem.send_keys(self.password)
        passwarword_elem.send_keys(Keys.RETURN)
        time.sleep(10)

        self.cookies = self.getInfoForCurrentSession()

        self.notNowNotifications()

    def isAccountLoggedOut(self):
        cookies = self.getInfoForCurrentSession()

        for cookie in cookies:
            if(cookie['name'] == 'sessionid'):
                return False

        return True

    def addCookies(self):
        self.driver.get("https://www.instagram.com/")
        for cookie in self.cookies:
            self.driver.add_cookie(cookie)

    def getRandomComment(self, comments):
        randomN = random.randint(0, len(comments) - 1)
        return comments[randomN]

    def likePost(self):
        # Like post
        try:
            likeButton = self.waitForElementXPATH("//span[@class='_aamw']/button")
            time.sleep(2)
            self.waitForElementXPATH("//span[@class='_aamw']/button/div[@class='_abm0 _abl_']")
            likeButton.click()
        except:
            pass

    def isAccountIsSusspended(self):
        self.driver.get("https://www.instagram.com")
        crrUrl = self.driver.current_url
        if "challenge" in crrUrl or 'suspended' in crrUrl:
            return True
        return False

    def tagRandomPersion(self):
        try:
            self.waitForElementCSS_Selectori("textarea").clear()
            char = chars[random.randint(0, len(chars) - 1)]
            self.waitForElementCSS_Selectori("textarea").send_keys(f'@{char}{Keys.ARROW_DOWN}')
            for a in range(random.randint(1, 40)):
                self.waitForElementCSS_Selectori("textarea").send_keys(Keys.ARROW_DOWN)
                time.sleep(0.2)
        except Exception as err:
            print('instaBot : tagRandomPersion', err)

    def commentRandomEmoji(self):
        try:
            # Adding an Extra comment for positive comments
            extraComments = [
                '🔥🔥🔥🔥🔥🔥🔥',
                '🔥🔥🔥🔥🔥🔥',
                '🔥🔥🔥🔥🔥',
                '🔥🔥🔥🔥',
                '🔥🔥🔥',
                '🔥🔥',
            ]
            extraComment = self.getRandomComment(extraComments)
            self.waitForElementCSS_Selectori("textarea").clear()
            time.sleep(0.3)
            self.waitForElementCSS_Selectori("textarea").send_keys(f'{extraComment}')
            time.sleep(0.5)
            self.waitForElementCSS_Selectori("textarea").send_keys(Keys.ENTER)
        except Exception as err:
            print('instaBot : commentRandomEmoji', err)

    def commentPost(self, comment, clearComment=True):
        try:
            comment_input = self.waitForElementCSS_Selectori("textarea")
            if (clearComment):
                time.sleep(0.3)
                comment_input.clear()
            comment_input.send_keys(f'{comment}')
            time.sleep(1)
            self.waitForElementCSS_Selectori("textarea").send_keys(Keys.ENTER)
        except Exception as err:
            print('instaBot : commentNormalPost', err)
            time.sleep(3)

    def comment(self, post, comments):
        # Getting comments, if default get the bots comment if not get the personilized comments
        if (comments == 'default'):
            selectedComments = self.comments
        else:
            selectedComments = comments
        comment = self.getRandomComment(selectedComments)

        self.driver.get(post)
        time.sleep(1)
        # Checks if it is a positive, if so like, comment and comment a random person, if negative just comment
        if (self.positive):
            self.likePost()
            time.sleep(1)
            self.commentPost(comment)
            time.sleep(5)
            self.commentRandomEmoji()
        else:
            self.commentPost(comment)
        time.sleep(5)

    def massiveComments(self, postURL):
        self.driver.get(postURL)
        time.sleep(1)
        # To be changed
        for _ in range(100):
            self.commentPost('bV45')
            time.sleep(15)

    def close(self):
        self.driver.close()

    def notNowNotifications(self, time=2):
        try:
            # notNowNotification = self.waitForElementXPATH("//button[contains(text(), 'Not Now')]", time=time)
            notNowNotification = self.waitForElementWithText("Not Now", time=time)
            # _a9_1
            notNowNotification.click()
            time.sleep(2)
            print('nn worked')
        except Exception as e:
            pass

    def allowCookies(self):
        try:
            time.sleep(3)
            allowCookies = self.waitForElementXPATH("//span[contains(text(), 'Allow all cookies')]", time=3)
            allowCookies.click()
        except:
            pass

    def open(self):
        """
            Creates a new webdriver and opens a new firefox window and
            imports the cookies given from the parameters.
        """
        self.run()
        self.addCookies()
        self.home()
        self.notNowNotifications()

    def run(self):
        """
            Creates a new webdriver and opens a new firefox window.
        """
        options = Options()
        # options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        options.set_preference("general.useragent.override", getRandomUserAgent())

        self.driver = webdriver.Firefox(options=options)

    def home(self):
        self.driver.get("https://www.instagram.com/")

    def getInfoForCurrentSession(self) -> list:
        """ Returns cookies for current user. """
        self.cookies = self.driver.get_cookies()
        return self.driver.get_cookies()

    def makeAccountPrivate(self):
        time.sleep(2)
        self.driver.get('https://www.instagram.com/accounts/privacy_and_security/')
        time.sleep(2)
        try:
            switchToPrivateButt = self.waitForElementsXPATH('//input[@class="x1i10hfl x9f619 xggy1nq x1s07b3s x1ypdohk x5yr21d xdj266r x11i5rnm xat24cr x1mh8g0r x1w3u9th x1a2a7pz xexx8yu x4uap5 x18d9i69 xkhd6sd x10l6tqk x17qophe x13vifvy xh8yej3"]')[0]
            switchToPrivateButt.click()
            time.sleep(3)

            switchConfirmation = self.waitForElementWithText('Switch to private', 'button')
            switchConfirmation.click()
            time.sleep(3)
        except Exception as err:
            print('instaBot', err)

    def makeAccountPublic(self):
        time.sleep(2)
        self.driver.get('https://www.instagram.com/accounts/privacy_and_security/')
        time.sleep(2)
        try:
            switchToPrivateButt = self.waitForElementsXPATH('//input[@class="x1i10hfl x9f619 xggy1nq x1s07b3s x1ypdohk x5yr21d xdj266r x11i5rnm xat24cr x1mh8g0r x1w3u9th x1a2a7pz xexx8yu x4uap5 x18d9i69 xkhd6sd x10l6tqk x17qophe x13vifvy xh8yej3"]')[0]
            switchToPrivateButt.click()
            time.sleep(3)

            switchConfirmation = self.waitForElementWithText('Switch to public', 'button')
            switchConfirmation.click()
            time.sleep(3)
        except Exception as err:
            print('instaBot', err)

    def switchToPersonalAccount(self):
        self.driver.get('https://www.instagram.com/accounts/edit/')

        try:
            switchButton = self.waitForElementWithText('Switch to Personal Account', 'div')
            switchButton.click()
            time.sleep(2)

            switchBackButton = self.waitForElementWithText('Switch Back', 'button')
            switchBackButton.click()
            time.sleep(5)
        except Exception as err:
            print('err', err)

    def follow_user(self, username):
        self.driver.get(f'https://www.instagram.com/{username}/')
        try:
            followButton = self.waitForElementXPATH('//button[@class="_acan _acap _acas _aj1-"]')
            followButton.click()
            time.sleep(1)
            return True
        except:
            print('USR DNE || Already Followed')
            return False

    def uploadMedia(self, absolutePath: str,maxTimeToWait: int = 30):
        self.driver.get("https://www.instagram.com/")
        # self.notNowNotifications(time=5)
        time.sleep(2)
        try:
            # Click post button
            createButton = self.waitForElementXPATH('//span[text()="Create"]', time=2)
            createButton.click()
            time.sleep(3)

            try:
                # Click post button
                createButton = self.waitForElementXPATH('//span[text()="Post"]', time=2)
                createButton.click()
                time.sleep(3)
            except Exception as err:
                print('err', err)

            # Input video path
            selectButton = self.waitForElementXPATH('//div[@class="x6s0dn4 x78zum5 x5yr21d xl56j7k x1n2onr6 xh8yej3"]').find_element(By.CLASS_NAME, "_ac69")
            selectButton.send_keys(absolutePath)
            time.sleep(0.867)

            # okItIsReelInfoButton
            try:
                # self.waitForElementXPATH("//button[@class(text(), 'OK')]", time=2).click()
                # div _ag4f
                # div _ag4f
                self.waitForElementXPATH(f'//button[@class="_acan _acap _acaq _acas _acav _aj1-"]').click()
                self.waitForElementXPATH(f'//div[@class="_ag4f"]').click()
            except:
                pass

            time.sleep(1)

            def clickNext(className):
                try:
                    nextButton = self.waitForElementXPATH(f'//div[@class="{className}"]')
                    time.sleep(0.635)
                    nextButton.click()
                except:
                    pass

            clickNext("_ac7b _ac7d")
            time.sleep(2)
            clickNext("_ac7b _ac7d")
            time.sleep(2)
            clickNext("_ac7b _ac7d")
            time.sleep(2)

            self.waitForElementXPATH('//span[text()="Your post has been shared."]', time=maxTimeToWait)

            time.sleep(2)
        except Exception as e:
            print(e)
            pass

    def editProfileInfo(self, fullName=None, username=None, bio=None):
        self.driver.get('https://www.instagram.com/accounts/edit/?next=%2F')
        self.notNowNotifications(time=10)

        # Editing username
        # if(len(self.waitForId('pepEmail').get_attribute('innerText')) == 0):
        #     for char in f'{fullName.replace(" ", "").lower()}{random.randint(0, 99999)}@gmail.com':
        #         self.waitForId('pepEmail').send_keys(char)
        #         time.sleep(random.uniform(0.1, 0.3))

        if (username != None):
            self.waitForId('pepUsername').clear()
            for char in username:
                self.waitForId('pepUsername').send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
            time.sleep(1)
        # Clicking Submit
        try:
            self.waitForElementXPATH('//div[@class="_ab47"]/div[@role="button"]').click()
        except:
            pass
        time.sleep(2)

        # Editing name
        if (fullName != None):
            self.waitForId('pepName').clear()
            for char in fullName:
                self.waitForId('pepName').send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))
            time.sleep(1)
        # Editing bio
        if (bio != None):
            self.waitForId('pepBio').clear()
            for chars in bio.split('\n'):
                self.waitForId('pepBio').send_keys(chars)
            time.sleep(1)
        # Clicking Submit
        try:
            self.waitForElementXPATH('//div[@class="_ab47"]/div[@role="button"]').click()
        except:
            pass
        time.sleep(2)

    def editProfilePic(self, absolutePath):
        headers = uploadProfilePic(self.getInfoForCurrentSession())
        values = {"Content-Disposition": "form-data", "name": "profile_pic", "filename": "profilepic.jpg",
                  "Content-Type": "image/jpeg"}
        requests.post("https://www.instagram.com/api/v1/web/accounts/web_change_profile_picture/", headers=headers,
                      data=values, files={'profile_pic': open(absolutePath, 'rb')})

    def clickXInNowAccountsCenter(self) -> None:
        # Find the SVG element using aria-label
        try:
            X_SVG_El = self.waitForElementCSS_Selectori('svg[aria-label="Close"]', time=2)
            X_SVG_El.click()
        except:
            pass

    def editProfileInfoMetaWay(self, fullName: str = None, username: str = None, bio: str = None):
        # Go to edit account
        self.driver.get('https://www.instagram.com/accounts/edit/')
        time.sleep(2)

        self.clickXInNowAccountsCenter()

        # Editing bio
        if (bio != None):
            self.waitForId('pepBio').clear()
            for chars in bio.split('\n'):
                self.waitForId('pepBio').send_keys(chars)
            time.sleep(1)

            # Clicking Submit
            self.waitForElementXPATH('//div[@class="_ab47"]/div[@role="button"]').click()
            time.sleep(2)

        # Going in the account center
        self.driver.get('https://accountscenter.instagram.com/?entry_point=app_settings')
        time.sleep(1)

        # Clicking the username button
        usernameButton = self.waitForClass('xq8finb')
        usernameButton.click()
        time.sleep(2)

        currentProfileUrl = self.driver.current_url
        actions = ActionChains(self.driver)

        if (fullName != None):
            # Editing full name
            # Going in the name input
            self.driver.get(f"{currentProfileUrl}name/")

            # Getting the input name element
            nameInput = self.waitForId(':ra:', time=5)
            nameInput.clear()
            nameInput.send_keys(fullName)
            time.sleep(1)

            actions.send_keys(Keys.TAB)  # Simulate Ctrl+T command
            actions.perform()
            time.sleep(0.5)

            actions.send_keys(Keys.TAB)  # Simulate Ctrl+T command
            actions.perform()
            time.sleep(0.5)

            actions.send_keys(Keys.TAB)  # Simulate Ctrl+T command
            actions.perform()
            time.sleep(0.5)

            actions.send_keys(Keys.ENTER)  # Simulate Ctrl+T command
            actions.perform()
            time.sleep(10)

        if (username != None):
            # Editing full name
            # Going in the name input
            self.driver.get(f"{currentProfileUrl}username/?entrypoint=fb_account_center")
            time.sleep(1)

            # Getting the input name element
            usernameInput = self.waitForId(':ra:', time=5)
            usernameInput.clear()
            usernameInput.send_keys(username)
            time.sleep(3)

            actions.send_keys(Keys.TAB)  # Simulate Ctrl+T command
            actions.perform()
            time.sleep(0.5)

            actions.send_keys(Keys.TAB)  # Simulate Ctrl+T command
            actions.perform()
            time.sleep(0.5)

            actions.send_keys(Keys.ENTER)  # Simulate Ctrl+T command
            actions.perform()
            time.sleep(10)

    def postMediaFromUrl(self, mediasUrl, timeWait=1):
        """#########Posting media#########"""
        for mediaUrl in mediasUrl:
            randomName = random.randint(0, 9999)

            # Getting extection
            exTention = getExeFromUrl(mediaUrl)
            relativePath = f'./images/{randomName}.{exTention}'
            try:
                urllib.request.urlretrieve(mediaUrl, relativePath)
            except Exception as e:
                print(e)
            self.uploadMedia(f"{os.getcwd()}/{relativePath}")
            time.sleep(timeWait)

    def completeProfile(self, fullName=None, username=None, bio=None, profilePic=None, imagesPaths=None):
        if imagesPaths is None:
            imagesPaths = []
        self.allowCookies()
        self.notNowNotifications(time=5)

        if (fullName != None or username != None or bio != None):
            self.driver.get('https://www.instagram.com/accounts/edit/')
            try:
                self.waitForElementXPATH('//span[contains(text(), "See more in Accounts")]')
                self.editProfileInfoMetaWay(fullName, username, bio)
                print('first method')
            except:
                try:
                    self.waitForElementXPATH('//span[contains(text(), "See more in Accounts Centre")]')
                    self.editProfileInfoMetaWay(fullName, username, bio)
                    print('first method')
                except:
                    print('second method')
                    self.editProfileInfo(fullName, username, bio)

        if profilePic != None:
            self.editProfilePic(profilePic)

        for url in imagesPaths:
            try:
                ext = url.split('.')[len(url.split('.')) - 1]
                if (ext == "mp4"):
                    self.uploadMedia(url, maxTimeToWait=120)
                else:
                    self.uploadMedia(url, maxTimeToWait=30)
            except:
                pass
            time.sleep(5)
        return True

    def followSuggestedUsernames(self):
        self.driver.get("https://www.instagram.com/explore/people/")
        followButtons = self.waitForElementsXPATH('//button[@class="_acan _acap _acas _aj1-"]')
        time.sleep(1.34)
        for button in followButtons[: random.randint(13, 17)]:
            button.click()
            time.sleep(random.uniform(1.5, 3.0))

    def isAccCommentRestricted(self):
        try:
            if self.cookies == []:
                self.cookies = self.getInfoForCurrentSession()
            if 'sessionid' not in [cookie['name'] for cookie in self.cookies]:
                return True

            sessionid = [cookie for cookie in self.cookies if cookie['name'] == 'sessionid'][0]['value']
            headers = commentPostHeaders(sessionId=sessionid)
            canThisCommentCheck = requests.post(
                "https://www.instagram.com/api/v1/web/comments/3018538865221322305/add/", headers=headers,
                data="comment_text=asd")
            if canThisCommentCheck.status_code == 200:
                return False
        except:
            pass
        return True

    #######################

    def followUsernameLongWay(self, username):
        self.driver.get(f"https://www.instagram.com/")

        # Click the search button in the sidebar
        searchText = self.waitForElementXPATH('//div[contains(text(), "Search")]')
        searchText.click()

        # Search in the input
        serachInput = self.waitForClass('_aauy')
        serachInput.send_keys(username)

        # Get the first element in the search result
        searchList = self.waitForElementsXPATH(
            '//div[@class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh xxbr6pl xbbxn1n xwib8y2 x1y1aw1k x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"]')
        searchList[0].click()

        followButton = self.waitForElementXPATH('//button[@class="_acan _acap _acas _aj1-"]')
        followButton.click()
        time.sleep(3)

    def getUsernameData(self, username):
        userData = requests.get(
            f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}", headers=webUserProfile)
        return json.loads(userData.text)['data']['user']

    def getUserPorfileData(self):
        headers = web_form_data(self.cookies)
        res = requests.get('https://www.instagram.com/api/v1/accounts/edit/web_form_data/', headers=headers)
        jsonData = json.loads(res.text)
        return jsonData['form_data']

    ##### In development
    def editProfileRequestsMethod(self, full_name=False, email=False, username=False, phone_number=False,
                                  biography=False, external_url=False, chaining_enabled='on'):
        currentUserData = self.getUserPorfileData()

        data = {
            'first_name': currentUserData['first_name'],
            'email': currentUserData['email'],
            'username': currentUserData['username'],
            'phone_number': currentUserData['phone_number'],
            'biography': currentUserData['biography'],
            'external_url': currentUserData['external_url'],
            'chaining_enabled': 'on',
        }

        if full_name:
            data['first_name'] = full_name

        if email:
            data['email'] = email

        if username:
            data['username'] = username

        if phone_number:
            data['phone_number'] = phone_number

        if biography:
            data['biography'] = biography

        if external_url:
            data['external_url'] = external_url

        if chaining_enabled:
            data['chaining_enabled'] = chaining_enabled

        # headers = instaEditProfile(self.getInfoForCurrentSession())
        headers = instaEditProfile(self.cookies)
        res = requests.post('https://www.instagram.com/api/v1/web/accounts/edit/', headers=headers, data=data)
        print("res", res.status_code)
        return res.status_code == 200

    def uploadMediaRequests(self, filePath):
        current_unixTS = int(datetime.now().timestamp())

        # rupload_igphoto
        rupload_headers = rupload_igphoto(self.cookies)

        rupload_headers[
            'X - Instagram - Rupload - Params'] = '{"media_type": 1, "upload_id": "' + f'{current_unixTS}' '" + "upload_media_height": 1080, "upload_media_width": 1080}'
        rupload_headers['X - Entity - Name'] = f'fb_uploader_{current_unixTS}'

        photo_data = open(filePath, 'rb').read()

        res = requests.post(f'https://i.instagram.com/rupload_igphoto/fb_uploader_{current_unixTS}',
                            headers=rupload_headers, data=photo_data)
        print("res", res, res.text)

        # media_configure
        media_conf_header = media_configure(self.cookies)
        data = {
            "source_type": "library",
            "caption": "",
            "upload_id": "1681322457555",
            "disable_comments": "0",
            "like_and_view_counts_disabled": "0",
            "igtv_share_preview_to_feed": "1",
            "is_unified_video": "1",
            "video_subtitles_enabled": "0",
            "disable_oa_reuse": "false"
        }

        res = requests.post(f'https://www.instagram.com/api/v1/media/configure/', headers=media_conf_header, data=data)
        print("res", res, res.text)

    def getUsername(self):
        self.driver.get("https://www.instagram.com/")

        classNameOfUsername = "x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _aak1 _a6hd"
        usernameDiv = self.waitForElementXPATH(f'//a[@class="{classNameOfUsername}"]')
        username = usernameDiv.get_attribute('innerHTML')
        return username

    def acceptCookies(self):
        # self.driver.get("https://www.instagram.com/")
        text = "Allow all cookies"
        try:
            acceptDiv = self.waitForElementXPATH(f'//div[@aria-label="{text}"]')
            acceptDiv.click()
        except:
            pass

    def scrollThroughFeed(self):
        self.driver.get(f'https://www.instagram.com/')
        time.sleep(3)
        self.notNowNotifications()

        try:
            # _ab6k _ab6m _aggc _aatb _aatc _aate _aatf _aati
            posts = self.waitForClases("_aamw")
            post = posts[0]
            post.click()
        except Exception as err:
            print("Err: ", err)

        # Scroll down the page by pressing the END key repeatedly
        body = self.driver.find_element(By.TAG_NAME, "body")
        for i in range(3):  # scroll down three times
            self.driver.execute_script("window.scrollTo(0, window.scrollY + 500);")
            time.sleep(2)  # wait for 2 seconds to load the content

        # self.driver.execute_script("arguments[0].scrollIntoView();", post)
        body.send_keys(Keys.ARROW_DOWN)

        self.driver.get('https://www.instagram.com/')
        time.sleep(3)

        # Click in the first stories and watches a cople of those
        try:
            stories = self.waitForElementsXPATH(
                '//button[@role="menuitem"]',
                time=10)

            stories[0].click()

            # Click the next button
            for _ in range(random.randint(3, 8)):
                try:
                    nextArrowButton = self.waitForClass('_ac0d')
                    nextArrowButton.click()
                    time.sleep(random.uniform(1, 3))
                except Exception as err:
                    print("Error", err)

        except Exception as err:
            print("Err: ", err)

        # Go back into feed
        self.driver.get('https://www.instagram.com/')
        time.sleep(3)

    def scrollThroughReels(self):
        self.driver.get(f'https://www.instagram.com/reels/')
        time.sleep(3)
        self.notNowNotifications()

        actions = ActionChains(self.driver)

        for i in range(random.randint(15,35)):  # scroll down three times
            actions.send_keys(Keys.ARROW_DOWN)
            actions.perform()
            time.sleep(random.randint(5,15))  # wait for 2 seconds to load the content


    def likeOrReplyToComment(self, postUrl, usernameComment, toLike=False, toComment=False):
        self.driver.get(postUrl)
        time.sleep(5)

        # Click plus button to get more comments
        def clickPlusCommentButton():
            # Scroll down
            # listContainer = self.waitForElementXPATH('//div[@class="x10l6tqk xexx8yu x1pi30zi x1l90r2v x1swvt13 xh8yej3 x9f619 x5yr21d"]').find_element("xpath", '//div[@class="x5yr21d"]')

            plusButton = self.waitForElementXPATH(
                '//div[@class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh xdj266r xat24cr x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh xl56j7k"]').find_element(
                "xpath", 'button[@class="_abl-"]')

            plusButton.click()

        # Check if comment is in the current list
        def findComment(lengthToStart=0):
            usernamesInComment = self.waitForElementsXPATH(
                '//a[@class="x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x1i0vuye xwhw2v2 xl56j7k x17ydfre x1f6kntn x2b8uid xlyipyv x87ps6o x14atkfc x1d5wrs8 x972fbf xcfux6l x1qhh985 xm0m39n xm3z3ea x1x8b98j x131883w x16mih1h xt0psk2 xt7dq6l xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 xjbqb8w x1n5bzlp xqnirrm xj34u2y x568u83"]')
            commentsList = self.waitForElementsXPATH('//li[@class="_a9zj _a9zl"]')

            commentsLen = len(usernamesInComment)
            print("usernamesInComment len", commentsLen, len(commentsList))

            for i, list in enumerate(usernamesInComment):
                if (usernameComment == list.get_attribute("innerHTML")):
                    print("Found: ", list.get_attribute("innerHTML"))
                    return commentsList[i - 1]
            try:
                clickPlusCommentButton()
            except:
                return False

            time.sleep(2)
            return findComment()

        isCommentFound = findComment()
        if isCommentFound != False:
            # Liking the comment
            if (toLike == True):
                heartButton = isCommentFound.find_element("xpath", './/button[@class="_abl- _abm2"]')
                heartButton.click()

            # Replying
            if (toComment == True):
                actionButtonsContainer = isCommentFound.find_element("xpath",
                                                                     './/div[@class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1xmf6yo x12nagc x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"]')
                actionButtons = actionButtonsContainer.find_elements("xpath", './/button[@class="_a9ze"]')
                if (len(actionButtons) == 0):
                    replyButton = actionButtons[0]
                else:
                    replyButton = actionButtons[1]

                replyButton.click()
                self.commentPost('damn', clearComment=False)

    def likeStory(self):
        pass

    def watchStoryOfUser(self, username):
        self.driver.get(f'https://www.instagram.com/{username}/')

        # class that is used to verify if a user has story
        classOfStory = '_aarg'

        try:
            doesUserHasStory = self.waitForClass(classOfStory, time=3)
        except:
            doesUserHasStory = False

        if(doesUserHasStory != False):
            doesUserHasStory.click()
        else:
            return False

        numberOfStories = len(self.waitForClases('_ac3o', time=3))
        numberOfLikes = 3

        if(numberOfStories < numberOfLikes):
            numberOfLikes = numberOfStories

        numberOfLikes = random.randint(1,numberOfLikes)

        storiesToLike = [0]

        for _ in range(numberOfLikes-1):
            randomN = random.randint(1, numberOfStories-1)
            toLoop = randomN in storiesToLike
            while toLoop:
                randomN = random.randint(1, numberOfStories-1)
                toLoop = randomN in storiesToLike
            storiesToLike.append(randomN)

        def next():
            try:
                nextButton = self.waitForClass('_9zm2', time=3)
                nextButton.click()
                return True
            except:
                return False

        def like():
            try:
                likeButton = self.waitForClass('_abx4', time=3)
                likeButton.click()
                return True
            except:
                return False

        print('storiesToLike',storiesToLike, numberOfLikes)

        for i in range(numberOfStories+1):
            if(i in storiesToLike):
                like()
                time.sleep(1)

            next()
            time.sleep(2)

    def likeNnumberOfPostsFromUser(self, username):
        self.driver.get(f'https://www.instagram.com/{username}/')

        postClass = '_al3l'

        posts = self.waitForClases(postClass, time=10)
        randomPostLikeLength = random.randint(1,3)

        random_numbers = random.sample(range(0, len(posts)-1), randomPostLikeLength)

        print('posts', len(posts), random_numbers, randomPostLikeLength)

        def likePost():
            try:
                likeButton = self.waitForClass('_aamw')
                likeButton.click()
            except Exception as err: print('err',err)


        for i in random_numbers:
            post = posts[i]

            post.click()
            time.sleep(2)
            likePost()
            time.sleep(1)

            self.driver.back()
            time.sleep(2)

    def message_username(self, username, message):
        self.driver.get(f'https://www.instagram.com/{username}/')

        time.sleep(4)

        self.waitForElementWithText('Message').click()

        time.sleep(10)

        # self.waitForElementWithText('Message...').click()

        self.send_text_in_browser(message)

        self.send_text_in_browser(Keys.ENTER)
        time.sleep(3)