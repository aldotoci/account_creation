import os
import random
import time

import uiautomator2 as u2

# import EC
from config import db
# from outlook__browser_bot import Outlook_bot

letters = ['e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
class IG_Bot:
    def __init__(self, device_serial: str = None, username: str = None, password: str = None, minWatchStory=6,
                 maxWatchStory=10, minScrollThroughFeed=10, maxScrollThroughFeed=15,
                 package_ext='android'):
        self.username = username
        self.password = password
        self.d = u2.connect(addr=device_serial)  # The android device address to connect to
        self.screen_width, self.screen_height = self.d.window_size()
        self.minWatchStory = minWatchStory
        self.maxWatchStory = maxWatchStory
        self.minScrollThroughFeed = minScrollThroughFeed
        self.maxScrollThroughFeed = maxScrollThroughFeed
        self.package_ext = package_ext

    def getNodeByResourceIdTextInclude(self, text):
        # Use XPath to find the node with a description that includes the target string
        xpath_expression = f'*//*[contains(@resource-id, "{text}")]'

        # Find the first matching element
        return self.d.xpath(xpath_expression)

    def openInstagram(self, relative_name='Instagram'):
        IGIcon = self.d.xpath(f'//android.widget.TextView[@text="{relative_name}"]')

        try:
            IGIcon = IGIcon.get_last_match()
        except:
            pass

        IGIcon.click()
        time.sleep(2)

        # Click ok button
        isOkButton = self.d.xpath(f'//*[contains(@text, "OK")]').wait(1)
        if (isOkButton):
            self.d.xpath(f'//*[contains(@text, "OK")]').click()


    def login(self, u=None, p=None) -> None:
        """Loging into instagram using username and password given from the (parameters | instructor)"""

        if u == None: u = self.username
        if p == None: p = self.password

        # Getting username, password input and login button
        usernameIn = self.d(className="android.widget.EditText")[0]
        passwordIn = self.d(className="android.widget.EditText")[1]

        # Entring username password
        usernameIn.set_text(u)
        passwordIn.set_text(p)

        self.d.click(100, 100)
        time.sleep(2)

        logInButt = self.d(text="Log in")
        # Clicking login button
        logInButt.click()

        # #Clicking not now button
        self.clickNotNowLogin()

        # Clicking Don't Allow Access
        self.dontAllowAccessToContact()

    def getXmlHierchy(self):
        with open('hierarchy.xml', 'w', encoding='utf-8') as f:
            # Write the hierarchy string to the file
            text = self.d.dump_hierarchy()
            f.write(text)

    def clickAndHoldProfileButton(self):
        """Click and hold the profile tab"""

        profile_tab = self.getNodeByResourceIdTextInclude(":id/profile_tab")

        # Click and hold the progile button
        self.d.swipe(profile_tab.center()[0], profile_tab.center()[1], profile_tab.center()[0], profile_tab.center()[1],
                     1)
        time.sleep(0.5)



    """
        Used when the fist account is logged in and you want to add another account
        @:param username:str of the user
        @:param password:str of the user
    """

    def addAccount(self, username: str, password: str) -> None:
        # self.clickAndHoldProfileButton()


        # Swipe till add account
        for i in range(2):
            self.d.swipe(500, 1000, 500, 500, 0.1)

        # Find the element by text and class
        AddAccountButton = self.d(text="Add account")
        AddAccountButton.click()
        time.sleep(2)

        # Clicking log into existing account
        logIntoExistingButton = self.d(text="Log into existing account")
        logIntoExistingButton.click()
        time.sleep(2)

        # Clicking into Switch Accounts button
        switchAccountButton = self.d(text="Switch Accounts")
        switchAccountButton.click()
        time.sleep(2)

        self.login(username, password)

    def swtichAccount(self, userNumber=None):
        self.clickAndHoldProfileButton()


        # Swipe till add account
        for i in range(2):
            self.d.swipe(500, 1000, 500, 500, 0.1)

        # Find the parent node
        listOfUsers = self.getNodeByResourceIdTextInclude(":id/row_user_textview")

        if (userNumber == None):
            userInList = listOfUsers[len(listOfUsers) - 2]
        else:
            userInList = listOfUsers[userNumber]

        userInList.click()

        # Click ok button
        isOkButton = self.d.xpath(f'//*[contains(@text, "OK")]').wait(1)
        if (isOkButton):
            self.d.xpath(f'//*[contains(@text, "OK")]').click()

    def openEditProfile(self):
        self.goToProfile()
        time.sleep(1)

        # Clicks the "Edit Profile" button
        self.d(resourceId=f"com.instagram.{self.package_ext}:id/button_text", text='Edit profile').wait(3)

        editProfileButt = self.d(resourceId=f"com.instagram.{self.package_ext}:id/button_text", text='Edit profile')
        editProfileButt.click()

    def editProfile(self, bio: str = None, external_url: str = None, external_title: str = None):
        self.openEditProfile()

        # Click not now
        self.clickNotNowAvatar()

        if bio != None:
            bioButton = self.d(text="Bio", resourceId=f"com.instagram.{self.package_ext}:id/form_field_label_inline")
            bioButton.click()

            # Edit text
            bioEditText = self.d(resourceId=f"com.instagram.{self.package_ext}:id/caption_edit_text")
            bioEditText.set_text(bio)
            time.sleep(2)

            # Edit Clicking okay icon
            okeyButton = self.d(resourceId=f"com.instagram.{self.package_ext}:id/action_bar_button_action")
            okeyButton.click()
            time.sleep(1)

        if external_url != None and external_title != None:
            # Clicks add link
            addLinkButton = self.d(text="Add link",
                                   resourceId=f"com.instagram.{self.package_ext}:id/igds_textcell_title")
            addLinkButton.click()

            # Add external link
            addExternalLinkBut = self.d(text="Add external link",
                                        resourceId=f"com.instagram.{self.package_ext}:id/link_option_text")
            addExternalLinkBut.click()

            # Gets url and title input
            urlIn = self.d(className="android.widget.EditText")[0]
            titleIn = self.d(className="android.widget.EditText")[1]

            # Edit url and Title
            urlIn.set_text(external_url)
            titleIn.set_text(external_title)

            # Edit Clicking okay icon
            okeyButton = self.d(resourceId=f"com.instagram.{self.package_ext}:id/action_bar_button_action")
            okeyButton.click()

        time.sleep(3)
        self.goBackButton()
        time.sleep(3)
        self.goBackButton()

    def goToSearchTab(self):
        self.getNodeByResourceIdTextInclude(':id/search_tab').click()

    def refreshSearchTab(self):
        self.goToSearchTab()
        time.sleep(0.05)
        self.goToSearchTab()

    def goToHomeTab(self):
        self.getNodeByResourceIdTextInclude(':id/feed_tab').click()

    def refreshHomeTab(self):
        self.goToHomeTab()
        time.sleep(0.05)
        self.goToHomeTab()

    def goToProfile(self):
        self.d(resourceId='com.instagram.androie:id/profile_tab').click()

    def goThroughExplorer(self):
        self.refreshSearchTab()
        time.sleep(2)

        postsList = self.getNodeByResourceIdTextInclude(':id/image_button')

        selectedPost = postsList[random.randint(3, 6)]

        selectedPost.click()

        # Scroll through posts
        self.goThroughFeed(goHome=False)

    def followUser(self, username):
        # Clicking the search button tab
        self.goToSearchTab()

        # Getting the search input
        searchInput = self.d(className="android.widget.EditText")

        # Click the searhc input
        searchInput.click()

        # Search
        searchInput.set_text(username)

        # Getting all the search results
        usernamesLabels = self.getNodeByResourceIdTextInclude(':id/row_search_user_username')

        # Clicking in the first username
        firstUsername = usernamesLabels[0]
        firstUsername.click()

        try:
            # Clicking the follow button
            isButton = self.d(text="Follow", className="android.widget.Button").click(timeout=2)

            time.sleep(1)
            if (isButton):
                followButton = self.d(text="Follow", className="android.widget.Button")
                followButton.click()
        except:
            print("User is porpably already followed")
            pass

    def clickTheFirstStory(self):
        # Clicking the first story
        firstStoryIcon = self.getNodeByResourceIdTextInclude(':id/avatar_image_view')[1]
        firstStoryIcon.click()

    def goThroughStory(self):
        self.refreshHomeTab()
        time.sleep(2)
        try:
            self.clickTheFirstStory()

            time.sleep(2)

            self.clickOkButton()

            time.sleep(1)

            # Calculate the coordinates for the right center side
            x = self.screen_width - 1  # Subtract 1 to avoid potential out-of-bounds errors
            y = self.screen_height // 2

            # Clicking at right center side of the screen
            for a in range(random.randint(self.minWatchStory, self.maxWatchStory)):
                time.sleep(random.uniform(0.5, 1.5))
                self.d.click(x, y)

            self.goBackButton()
            self.goBackButton()
        except:
            pass

    def goThroughFeed(self, goHome=True):
        if (goHome):
            self.refreshHomeTab()

        # Perform a swipe to scroll
        start_x = 500
        start_y = 1000
        end_x = 500
        end_y = 500
        duration = 0.1

        constMultiplier = 4
        postsToScroll = random.randint(self.minScrollThroughFeed, self.maxScrollThroughFeed)

        nPostsToLike = random.randint(2, 3)

        for i in range(constMultiplier * postsToScroll):
            self.d.swipe(start_x, start_y, end_x, end_y, duration)

            if (nPostsToLike > 0 and i % random.randint(3, 5) == 0):
                if (self.isThereALikeButton()):
                    self.likePost()
                    nPostsToLike -= 1

    def isThereALikeButton(self):
        try:
            likeButton = self.d(description="Like")
            return likeButton.exists
        except:
            return False

    def likePost(self):
        try:
            likeButton = self.d(description="Like")
            likeButton.click()
        except:
            pass

    def goBackButton(self):
        # Press the back button
        self.d.press("back")

    def clickOkButton(self, call_back=None):
        try:
            okButtton = self.d(text="OK").wait(timeout=2)
            if (okButtton):
                self.d(text="OK").click()
                if(call_back != None):
                    call_back()
        except:
            pass

    def clickokButton(self, call_back=None):
        try:
            okButtton = self.d(text="ok").wait(timeout=2)
            if (okButtton):
                self.d(text="ok").click()
                if(call_back != None):
                    call_back()
        except:
            pass


    def clickNotNowAvatar(self):
        try:
            exists = self.d(text="Not now").wait(0.5)
            print('exists', exists)
            if (exists):
                notNowButton = self.d(text="Not now")
                notNowButton.click()
        except Exception as err:
            print('Error: ', err)

    def clickNotNowLogin(self):
        try:
            notNowButton = self.d(className="android.widget.Button", description="Not now")
            notNowButton.click()
        except Exception as err:
            print("Err: ", err)

    def dontAllowAccessToContact(self):
        try:
            switchAccountButton = self.d(text="Don't Allow Access")
            switchAccountButton.click()
        except Exception as err:
            print("Err: ", err)

    def downloadIGCache(self):
        os.system("adb pull /data/data/com.instagram.android/cache instacache")

    def deleteIGCache(self):
        os.system("adb shell pm clear com.instagram.android")

    def uploadIGCache(self, chacheFilePath):
        # adb push <path_to_cache_file> /sdcard/Android/data/com.instagram.android/cache/
        pass

    def changeImei(self):
        #
        pass

    def removeOpenedApps(self):
        # Open the recent apps screen
        self.d.press("recent")

        time.sleep(2)

        try:
            butt = self.d(text="Close all").wait(1)
            if (butt):
                self.d(text="Close all").click()
        except:
            pass

        # Press the home button again to return to the home screen
        self.d.press("home")

    def isAccountSuspended(self):
        isSus = self.d.xpath(f'//*[contains(@text, "We suspended your account,")]').wait(1)
        if (isSus != None):
            print(isSus.info['text'])

        return isSus != None

    def removeSuspendedAccount(self):
        options = self.d(className="android.view.View", index='1')
        options.click()

        time.sleep(1)

        logOutButton = self.d.xpath(f'//*[contains(@text, "Log out")]').wait(1)
        logOutButton.click()

        time.sleep(1)

        logOutButton2 = self.d.xpath(f'//*[contains(@text, "Log Out")]').wait(1)
        logOutButton2.click()

        time.sleep(2)

        # Click ok button
        isOkButton = self.d.xpath(f'//*[contains(@text, "OK")]').wait(1)
        if (isOkButton):
            self.d.xpath(f'//*[contains(@text, "OK")]').click()

    def swipe_number_picker(self, el, num_swipe, direction, steps=10):
        info = el.info
        bounds = info.get('visibleBounds') or info.get("bounds")
        lx, ly, rx, ry = bounds['left'], bounds['top'], bounds['right'], bounds['bottom']  # yapf: disable
        cx, cy = (lx + rx) // 2, (ly + ry) // 2

        assert direction in ("left", "right", "up", "down")

        if direction == 'up':
            self.d.swipe(cx, cy, cx, (ly * (1 + (num_swipe / 10))), steps=steps)
        elif direction == 'down':
            self.d.swipe(cx, cy, cx, (ry * (1 + (num_swipe / 10) + 0.1)) + 1, steps=10)
        elif direction == 'left':
            self.d.swipe(cx, cy, lx, cy, steps=steps)
        elif direction == 'right':
            self.d.swipe(cx, cy, rx - 1, cy, steps=steps)

    def skip(self) -> None:
        skip_button = self.d(text="Skip")
        skip_button.click()

    def createAccount(self, fullname, password, day, month, year, username, email) -> None:
        if (self.isUserLoggedIn()):
            # self.clickAndHoldProfileButton()

            self.goToProfile()

            drop_down_icon = self.d(resourceId='com.instagram.androie:id/action_bar_little_icon_container')
            drop_down_icon.click()

            # Swipe till add account
            for i in range(2):
                self.d.swipe(500, 1000, 500, 500, 0.1)

            # Find the element by text and class
            AddAccountButton = self.d(text="Add account")
            AddAccountButton.click()
            time.sleep(2)

            # Clicking log into existing account
            logIntoExistingButton = self.d(text="Create new account")
            logIntoExistingButton.click()
            time.sleep(2)

            # Setting Username
            username_input = self.d(className='android.widget.EditText')
            username_input.clear_text()
            username_input.send_keys(username)

            time.sleep(4)

            # Clicking Next
            next_button = self.d.xpath(f'//*[contains(@text, "Next")]')
            next_button.click()

            time.sleep(4)

            # Adding password
            full_name_input = self.d(className='android.widget.EditText')
            full_name_input.send_keys(password)

            full_name_input = self.d.xpath(f'//*[contains(@text, "Create a password")]')
            full_name_input.click()
            full_name_input = self.d.xpath(f'//*[contains(@text, "Create a password")]')
            full_name_input.click()

            time.sleep(2)

            # Clicking Next
            next_button = self.d.xpath(f'//*[contains(@text, "Next")]')
            next_button.click()

            time.sleep(3)

            # Adding Email
            add_new_email_or_phone = self.d.xpath(f'//*[contains(@text, "Add new phone or email")]')
            add_new_email_or_phone.click()

            time.sleep(3)

            EMAIL_option = self.d.xpath(f'//*[contains(@text, "EMAIL")]')
            EMAIL_option.click()

            time.sleep(3)

            # Setting Email
            email_input = self.d(className='android.widget.EditText')
            email_input.send_keys(email)

            next_button = self.d(text="Add phone or email")
            next_button.click()

            time.sleep(1)

            # Clicking Next
            next_button = self.d(text='Next')
            next_button.click()

            time.sleep(5)

            code = EC.wait_until_verification_code_from_email(email)
            print('code', code)

            # Setting Email
            email_confirm_input = self.d(className='android.widget.EditText')
            email_confirm_input.send_keys(code)

            time.sleep(1)

            # Clicking Next
            next_button = self.d.xpath(f'//*[contains(@text, "Next")]')
            next_button.click()

            time.sleep(30)

        else:
            # Clicking the click new button
            create_new_button = self.d.xpath(f'//*[contains(@text, "Create new account")]')
            create_new_button.click()

            # Click none of the above if instagram ask if you want to use previous crededentils
            try:
                none_of_the_above = self.d.xpath(f'//*[contains(@text, "NONE OF THE ABOVE")]')
                none_of_the_above.click()
            except Exception as err:
                print('err, none of the above did not exist.')

            # Adding fullname
            full_name_input = self.d(className='android.widget.EditText')
            full_name_input.send_keys(fullname)

            # Clicking Next
            next_button = self.d.xpath(f'//*[contains(@text, "Next")]')
            next_button.click()

            time.sleep(3)

            # Adding password
            full_name_input = self.d(className='android.widget.EditText')
            full_name_input.send_keys(password)

            full_name_input = self.d.xpath(f'//*[contains(@text, "Create a password")]')
            full_name_input.click()

            time.sleep(2)

            # Clicking Next
            next_button = self.d.xpath(f'//*[contains(@text, "Next")]')
            next_button.click()

            time.sleep(1)

            try:
                # Cling Not now
                not_now_button = self.d.xpath(f'//*[contains(@text, "Not now")]').wait(2)
                if (not_now_button): not_now_button = self.d.xpath(f'//*[contains(@text, "Not now")]')
                not_now_button.click()
            except Exception as err:
                print('Not now err')

            time.sleep(3)

            # Setting date
            number_pickers = self.d(className='android.widget.NumberPicker')

            month_picker = number_pickers[0]
            day_picker = number_pickers[1]
            year_picker = number_pickers[2]

            # Selecting day
            current_day = self.d(resourceId=f"android:id/numberpicker_input")[1].info['text']
            day_sub = int(current_day) - int(day)
            day_sub = day_sub if day_sub > 0 else 30 + day_sub

            print('day_sub', day_sub)
            self.swipe_number_picker(day_picker, day_sub, 'down')

            # Selecting month
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            time.sleep(1)
            month_text = self.d(resourceId=f"android:id/numberpicker_input")[0]

            current_month = int(months.index(month_text.info['text']) + 1)
            month_sub = current_month - int(month)
            month_sub = month_sub if month_sub > 0 else 12 + month_sub

            print('month_sub', month_sub)
            self.swipe_number_picker(month_picker, month_sub, 'down')
            #
            # # Selecting Year
            current_year = self.d(resourceId=f"android:id/numberpicker_input")[2].info['text']
            year_sub = int(current_year) - int(year)
            year_sub = year_sub if year_sub > 0 else 30 + year_sub

            print('year_sub', year_sub)
            self.swipe_number_picker(year_picker, year_sub + 2, 'down')

            time.sleep(1)

            # Clicking Set
            set_button = self.d.xpath(f'//*[contains(@text, "SET")]')
            set_button.click()

            # Clicking Next
            next_button = self.d.xpath(f'//*[contains(@text, "Next")]')
            next_button.click()

            time.sleep(1)

            # Setting Username
            username_input = self.d(className='android.widget.EditText')
            username_input.clear_text()
            username_input.send_keys(username)

            time.sleep(4)

            # Clicking Next
            next_button = self.d.xpath(f'//*[contains(@text, "Next")]')
            next_button.click()

            # Sign up with email
            set_button = self.d.xpath(f'//*[contains(@text, "Sign up with email")]')
            set_button.click()

            # Setting Email
            email_input = self.d(className='android.widget.EditText')
            email_input.send_keys(email)

            next_button = self.d.xpath(f'//*[contains(@text, "What\'s your email?")]')
            next_button.click()

            time.sleep(1)

            # Clicking Next
            next_button = self.d.xpath(f'//*[contains(@text, "Next")]')
            next_button.click()

            time.sleep(1)

            code = EC.wait_until_verification_code_from_email(email)
            print('code', code)

            # Setting Email
            email_confirm_input = self.d(className='android.widget.EditText')
            email_confirm_input.send_keys(code)

            time.sleep(1)

            # Clicking Next
            next_button = self.d.xpath(f'//*[contains(@text, "Next")]')
            next_button.click()

            # Agreeing to terms of privacy
            agreeing_button = self.d(className="android.widget.Button", description="I agree")
            agreeing_button.click()


    def createAccount_v1(self, fullname, password, day, month, year, username, email, email_password) -> None:
        if (self.isUserLoggedIn()):
            # self.clickAndHoldProfileButton()

            self.goToProfile()

            time.sleep(3)

            drop_down_icon = self.d(resourceId='com.instagram.androie:id/action_bar_little_icon_container')
            drop_down_icon.click()

            # Swipe till add account
            for i in range(2):
                self.d.swipe(500, 1000, 500, 500, 0.1)

            # Find the element by text and class
            AddAccountButton = self.d(text="Add account")
            AddAccountButton.click()
            time.sleep(2)

            # Clicking log into existing account
            logIntoExistingButton = self.d(text="Create new account")
            logIntoExistingButton.click()
            time.sleep(2)

            # Setting Username
            username_input = self.d(className='android.widget.EditText')
            username_input.clear_text()
            username_input.send_keys(username)

            time.sleep(4)

            # Clicking Next
            next_button = self.d.xpath(f'//*[contains(@text, "Next")]')
            next_button.click()

            time.sleep(4)

            # Adding password
            full_name_input = self.d(className='android.widget.EditText')
            full_name_input.send_keys(password)

            full_name_input = self.d.xpath(f'//*[contains(@text, "Create a password")]')
            full_name_input.click()
            full_name_input = self.d.xpath(f'//*[contains(@text, "Create a password")]')
            full_name_input.click()

            time.sleep(2)

            # Clicking Next
            next_button = self.d.xpath(f'//*[contains(@text, "Next")]')
            next_button.click()

            time.sleep(3)

            # Adding Email
            add_new_email_or_phone = self.d.xpath(f'//*[contains(@text, "Add new phone or email")]')
            add_new_email_or_phone.click()

            time.sleep(3)

            EMAIL_option = self.d.xpath(f'//*[contains(@text, "EMAIL")]')
            EMAIL_option.click()

            time.sleep(3)

            # Setting Email
            email_input = self.d(className='android.widget.EditText')
            email_input.send_keys(email)

            next_button = self.d(text="Add phone or email")
            next_button.click()

            time.sleep(1)

            # Clicking Next
            next_button = self.d(text='Next')
            next_button.click()

            time.sleep(5)

            outlook_bot = Outlook_bot(email, email_password)
            code = outlook_bot.get_insta_verif_code()

            if(code == False):
                return False

            outlook_bot.close()

            print('code', code)

            # Setting Email
            email_confirm_input = self.d(className='android.widget.EditText')
            email_confirm_input.send_keys(code)

            time.sleep(1)

            # Clicking Next
            next_button = self.d.xpath(f'//*[contains(@text, "Next")]')
            next_button.click()

            time.sleep(30)

        else:
            # Clicking the click new button
            create_new_button = self.d.xpath(f'//*[contains(@text, "Create new account")]')
            create_new_button.click()

            # Click none of the above if instagram ask if you want to use previous crededentils
            try:
                none_of_the_above = self.d.xpath(f'//*[contains(@text, "NONE OF THE ABOVE")]')
                none_of_the_above.click()
            except Exception as err:
                print('err, none of the above did not exist.')

            # Adding fullname
            full_name_input = self.d(className='android.widget.EditText')
            full_name_input.send_keys(fullname)

            # Clicking Next
            next_button = self.d.xpath(f'//*[contains(@text, "Next")]')
            next_button.click()

            time.sleep(3)

            # Adding password
            full_name_input = self.d(className='android.widget.EditText')
            full_name_input.send_keys(password)

            full_name_input = self.d.xpath(f'//*[contains(@text, "Create a password")]')
            full_name_input.click()

            time.sleep(2)

            # Clicking Next
            next_button = self.d.xpath(f'//*[contains(@text, "Next")]')
            next_button.click()

            time.sleep(1)

            try:
                # Cling Not now
                not_now_button = self.d.xpath(f'//*[contains(@text, "Not now")]').wait(2)
                if (not_now_button): not_now_button = self.d.xpath(f'//*[contains(@text, "Not now")]')
                not_now_button.click()
            except Exception as err:
                print('Not now err')

            time.sleep(3)

            # Setting date
            number_pickers = self.d(className='android.widget.NumberPicker')

            month_picker = number_pickers[0]
            day_picker = number_pickers[1]
            year_picker = number_pickers[2]

            # Selecting day
            current_day = self.d(resourceId=f"android:id/numberpicker_input")[1].info['text']
            day_sub = int(current_day) - int(day)
            day_sub = day_sub if day_sub > 0 else 30 + day_sub

            print('day_sub', day_sub)
            self.swipe_number_picker(day_picker, day_sub, 'down')

            # Selecting month
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            time.sleep(1)
            month_text = self.d(resourceId=f"android:id/numberpicker_input")[0]

            current_month = int(months.index(month_text.info['text']) + 1)
            month_sub = current_month - int(month)
            month_sub = month_sub if month_sub > 0 else 12 + month_sub

            print('month_sub', month_sub)
            self.swipe_number_picker(month_picker, month_sub, 'down')
            #
            # # Selecting Year
            current_year = self.d(resourceId=f"android:id/numberpicker_input")[2].info['text']
            year_sub = int(current_year) - int(year)
            year_sub = year_sub if year_sub > 0 else 30 + year_sub

            print('year_sub', year_sub)
            self.swipe_number_picker(year_picker, year_sub + 2, 'down')

            time.sleep(1)

            # Clicking Set
            set_button = self.d.xpath(f'//*[contains(@text, "SET")]')
            set_button.click()

            # Clicking Next
            next_button = self.d.xpath(f'//*[contains(@text, "Next")]')
            next_button.click()

            time.sleep(1)

            # Setting Username
            username_input = self.d(className='android.widget.EditText')
            username_input.clear_text()
            username_input.send_keys(username)

            time.sleep(4)

            # Clicking Next
            next_button = self.d.xpath(f'//*[contains(@text, "Next")]')
            next_button.click()

            # Sign up with email
            set_button = self.d.xpath(f'//*[contains(@text, "Sign up with email")]')
            set_button.click()

            # Setting Email
            email_input = self.d(className='android.widget.EditText')
            email_input.send_keys(email)

            next_button = self.d.xpath(f'//*[contains(@text, "What\'s your email?")]')
            next_button.click()

            time.sleep(1)

            # Clicking Next
            next_button = self.d.xpath(f'//*[contains(@text, "Next")]')
            next_button.click()

            time.sleep(1)

            outlook_bot = Outlook_bot(email, email_password)
            code = outlook_bot.get_insta_verif_code()

            # Setting Email
            email_confirm_input = self.d(className='android.widget.EditText')
            email_confirm_input.send_keys(code)

            time.sleep(1)

            # Clicking Next
            next_button = self.d.xpath(f'//*[contains(@text, "Next")]')
            next_button.click()

            # Agreeing to terms of privacy
            agreeing_button = self.d(className="android.widget.Button", description="I agree")
            agreeing_button.click()


    def isUserLoggedIn(self) -> bool:
        log_in_button = self.d.xpath(f'//*[contains(@text, "Create new account")]').wait(2)

        if (log_in_button):
            return False
        return True

    def goToDiscoverPeople(self) -> None:
        self.goToSearchTab()

        time.sleep(1)

        discover_people = self.d(description="Discover people")
        discover_people.click()

        time.sleep(2)

    def swipe_up(self, number_swipe=400) -> None:
        # Define the start and end coordinates for the swipe
        start_x = 500  # X-coordinate in the middle of the screen
        start_y = 1000  # Starting from the bottom of the screen
        end_x = 500  # X-coordinate in the middle of the screen (no horizontal movement)
        end_y = number_swipe  # Ending closer to the top of the screen

        # Perform the swipe up action
        self.d.swipe(start_x, start_y, end_x, end_y)

    def swipe_down(self, number_swipe=400, duration=0.1, start_y=10, start_x=500 ) -> None:
        # Define the start and end coordinates for the swipe
        end_x = number_swipe  # X-coordinate in the middle of the screen
        end_y = 1000  # Starting from the bottom of the screen

        # Perform the swipe up action
        self.d.swipe(start_x, start_y, end_x, end_y, duration)

    def follow_suggested_accounts(self, number=50):
        self.goToDiscoverPeople()

        try:
            dontAllow = self.d(text="Don't allow access").wait(2)
            if (dontAllow):
                self.d(text="Don't allow access").click()
        except:
            pass

        discover_people = self.d.xpath(f'//*[contains(@text, "Discover people")]')
        discover_people.click()

        follow_count = 0

        while follow_count <= number:
            try:
                follow_buttons = [*self.d(text="Follow")][0]
                follow_buttons.click()
            except Exception as err:
                print('err', err)

            time.sleep(random.uniform(0.5, 1))

            follow_count += 1
            if (follow_count > number):
                return

            if (follow_count % 5 == 0):
                self.swipe_up(number_swipe=250)
                time.sleep(1)

    def go_android_home(self):
        self.d.keyevent("KEYCODE_HOME")

    def reset_ip(self):
        self.swipe_down()
        time.sleep(0.5)

        plane_icon = self.d(resourceId='android:id/icon')[4]
        plane_icon.click()

        time.sleep(3)

        plane_icon = self.d(resourceId='android:id/icon')[4]
        plane_icon.click()

        self.go_android_home()

    def uninstall_app(package_name):
        os.system(f'adb shell pm uninstall {package_name}')

    def create_new_clone(self):
        self.removeOpenedApps()

        self.swipe_up(50)

        cloner = self.d.xpath(f'//android.widget.TextView[@text="App Cloner"]')
        cloner.click()

        time.sleep(10)

        ig = self.d(text='Instagram')
        ig.click()

        ##########################3
        clone_number_button = self.d(text="Clone number")
        clone_number_button.click()

        time.sleep(1)

        current_app_number = self.d(className="android.widget.EditText").info['text']
        print('current_app_number', current_app_number)

        self.package_ext = f'androi{letters[int(current_app_number)]}'
        print('bot.package_ext', self.package_ext)

        # Increase number
        self.d(description="Plus").click()

        # Clicking OK
        self.d(text='OK').click()

        ##############

        time.sleep(2)
        clone_button = self.d(description="Clone app")
        clone_button.click()

        try:
            update_button = self.d(text="UPDATE").wait(2)
            if update_button: self.d(text="UPDATE").click()
        except:
            pass

        time.sleep(60 * 2.5)

    def open_clone(self, instance_name):
        self.go_android_home()
        time.sleep(1)
        self.swipe_up(50)
        time.sleep(1)
        self.swipe_up(100)
        time.sleep(1)

        self.openInstagram(relative_name=instance_name)
        time.sleep(10)

    def create_and_warm_account(self, instance_name, fullname, username, password, day, month, year, email):
        self.createAccount(fullname, password=password, day=day, month=month, year=year, username=username, email=email)

        user = {
            'username': username,
            'password': password,
            'email': email,
            'email_username': email,
            'cookies': []
        }
        db.native_android_ig_acc.insert_one(user)

        time.sleep(20)

        self.removeOpenedApps()

        time.sleep(2)

        self.open_clone(instance_name)

        time.sleep(10)

        self.d.click(100, 100)
        time.sleep(2)

        # Check if the user is loged in
        if (not self.isUserLoggedIn()):
            self.login(username, password)

            time.sleep(10)

            def call_back():
                self.login(username, password)

            self.clickOkButton(call_back)
            self.clickokButton(call_back)

        self.removeOpenedApps()

        # self.open_clone(instance_name)
        #
        # self.removeOpenedApps()
        #
        # time.sleep(2)
        #
        # self.open_clone(instance_name)
        #
        # time.sleep(10)
        #
        # try:
        #     self.follow_suggested_accounts(50)
        # except Exception as err:
        #     print('err', err)
        #
        # try:
        #     self.goBackButton()
        # except Exception as err:
        #     print('err', err)
        #
        # try:
        #     self.goThroughFeed()
        # except Exception as err:
        #     print('err', err)
        #
        # try:
        #     self.goThroughStory()
        # except Exception as err:
        #     print('err', err)


    def create_and_warm_account_v1(self, instance_name, fullname, username, password, day, month, year, email, email_password):
        r = self.createAccount_v1(fullname, password=password, day=day, month=month, year=year, username=username, email=email, email_password=email_password)

        if(r == False):
            return False

        user = {
            'username': username,
            'password': password,
            'email': email,
            'email_username': email,
            'cookies': []
        }
        db.native_android_ig_acc.insert_one(user)

        time.sleep(20)

        self.removeOpenedApps()

        time.sleep(2)

        self.open_clone(instance_name)

        time.sleep(10)

        self.d.click(100, 100)
        time.sleep(2)

        # Check if the user is loged in
        if (not self.isUserLoggedIn()):
            self.login(username, password)

            time.sleep(10)

            def call_back():
                self.login(username, password)

            self.clickOkButton(call_back)
            self.clickokButton(call_back)

        self.removeOpenedApps()

        # self.open_clone(instance_name)
        #
        # self.removeOpenedApps()
        #
        # time.sleep(2)
        #
        # self.open_clone(instance_name)
        #
        # time.sleep(10)
        #
        # try:
        #     self.follow_suggested_accounts(50)
        # except Exception as err:
        #     print('err', err)
        #
        # try:
        #     self.goBackButton()
        # except Exception as err:
        #     print('err', err)
        #
        # try:
        #     self.goThroughFeed()
        # except Exception as err:
        #     print('err', err)
        #
        # try:
        #     self.goThroughStory()
        # except Exception as err:
        #     print('err', err)



    def create_new_identity(self):
        self.removeOpenedApps()

        self.swipe_up(50)

        cloner = self.d.xpath(f'//android.widget.TextView[@text="App Cloner"]')
        cloner.click()

        time.sleep(10)

        app_cloner_nav_butts = self.d(className="android.view.View")
        app_cloner_nav_butts[1].click()

        time.sleep(1)

        gmail_butt = self.d.xpath("//*[contains(@text, 'Instagram')]")
        gmail_butt.click()

        time.sleep(1)

        new_identity = self.d(text='New identity')
        new_identity.click()

        time.sleep(2)

        delete_app_data = self.d(text='Delete app data')
        delete_app_data.click()

        time.sleep(2)
        delete_app_data = self.d(text='OK')
        delete_app_data.click()

        time.sleep(10)








