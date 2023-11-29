# from utils import convertDicCookiesIntoRow

def convertDicCookiesIntoRow(cookies):
    row = ""
    for cookie in cookies:
        row += f"{cookie['name']}={cookie['value']};"
    return row
def tranRowIntoDictHeaders(filePath):
    listHeaders = open(filePath).readlines()
    dictHeaders = {}

    for i, header in enumerate(listHeaders):
        if(i+1 != len(listHeaders)):
            header = header[:-1]
        name = ''
        value = ''
        c = 0
        for char in header:
            if char == ':':
                c += 1
                if c == 1:
                    continue
            if c == 0:
                name += char
            else:
                value += char

        dictHeaders[name.strip()] = value.strip()
    return dictHeaders

webUserProfile = {
    # GET /api/v1/users/web_profile_info/?username=shkendije_mujaj_ HTTP/2
    'Host': 'i.instagram.com',
    'Cookie': 'sessionid=;',
    # 'Cookie': 'sessionid=61706700869%3AsTNWvDuKfbKE0S%3A10%3AAYfjpfCrn17eGUyaOqb4FP-47qEeyWrZRV5J9oG8gQ;',
    'Content-Length': '0',
    'Sec-Ch-Ua': '"Chromium";v="95", ";Not A Brand";v="99"',
    'X-Ig-App-Id': '936619743392459',
    'X-Ig-Www-Claim': 'hmac.AR3jZQ0css2KCe5zGzPBscz1cL0odSz9nCg7QxCAlZz2VjUz',
    'Sec-Ch-Ua-Mobile': '?0',
    # 'X-Instagram-Ajax': '1006123492',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'X-Asbd-Id': '198387',
    'X-Csrftoken': '',
    'Sec-Ch-Ua-Platform': '"Linux"',
    'Origin': 'https://www.instagram.com',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.instagram.com/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
}

def defaultHeaders(cookiesRow="''", crsfToken="''"):
    return {
        'Host': 'www.instagram.com',
        'Cookie': cookiesRow,
        "Content-Length": "59",
        'Sec-Ch-Ua': '"Chromium";v="95", ";Not A Brand";v="99"',
        'X-Ig-App-Id': '936619743392459',
        'X-Ig-Www-Claim': 'hmac.AR2pEE_QD2mwCPtc8X9HU3WcNx4jUcKxHibd3CJX6DNsgMlN',
        'Sec-Ch-Ua-Mobile': '?0',
        'X-Instagram-Ajax': '1006638455',
        'Viewport-Width': '1366',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'X-Csrftoken': crsfToken,
        'X-Requested-With': 'XMLHttpRequest',
        'X-Asbd-Id': '198387',
        'Sec-Ch-Prefers-Color-Scheme': 'light',
        'Sec-Ch-Ua-Platform': '"Linux"',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.instagram.com/whosnext.tv/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
    }

def owner_media():
    return {
        # GET /api/v1/feed/user/223049889/?count=12&max_id=2990993799884314286_223049889 HTTP/2
        "Host": "www.instagram.com",
        "Cookie": "ds_user_id=''; sessionid='60055211827%3As3FzDyLWKjk0sJ%3A4%3AAYfQM4dgs7ac3UYK8kjvLgk51w-HD-To7dqtX2R1hA';",
        "Sec-Ch-Ua": '"Chromium";v="95", ";Not A Brand";v="99"',
        "X-Ig-App-Id": "936619743392459",
        "X-Ig-Www-Claim": "hmac.AR2pEE_QD2mwCPtc8X9HU3WcNx4jUcKxHibd3CJX6DNsgBLn",
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
        "Viewport-Width": "1366",
        "Accept": "*/*",
        "X-Csrftoken": '',
        "X-Requested-With": "XMLHttpRequest",
        "X-Asbd-Id": "198387",
        "Sec-Ch-Prefers-Color-Scheme": "light",
        "Sec-Ch-Ua-Platform": '"Linux"',
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.instagram.com/blackjaguarwhitetiger/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
    }

def uploadProfilePic(cookieObjs):
    crsfToken = next((cookie for cookie in cookieObjs if cookie["name"] == "csrftoken"), {})
    defaultH = defaultHeaders(convertDicCookiesIntoRow(cookieObjs), crsfToken['value'])
    return {
        **defaultH,
        # "Content-Disposition": "form-data"; name="profile_pic"; 
    }
resetPassHeaders = {
    # POST /api/v1/web/accounts/web_create_ajax/attempt/ HTTP/2
    "Host": "www.instagram.com",
    "Cookie": "''",
    "Content-Length": "59",
    "Sec-Ch-Ua": '"Chromium";v="95", ";Not A Brand";v="99"',
    "X-Ig-App-Id": "936619743392459",
    "X-Ig-Www-Claim": "hmac.AR2pEE_QD2mwCPtc8X9HU3WcNx4jUcKxHibd3CJX6DNsgKXI",
    "X-Requested-With": "XMLHttpRequest",
    "Sec-Ch-Ua-Mobile": "?0",
    "X-Instagram-Ajax": "1006628428",
    "Viewport-Width": "1366",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "*/*",
    "X-Csrftoken": "''",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
    "X-Asbd-Id": "198387",
    "Sec-Ch-Prefers-Color-Scheme": "light",
    "Sec-Ch-Ua-Platform": "Linux",
    "Origin": "https://www.instagram.com",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://www.instagram.com/accounts/emailsignup/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
    # email=aldotoci&username=&first_name=&opt_into_one_tap=false
}

def commentPostHeaders(sessionId: str):
    return {
        # POST /api/v1/web/comments/3013319255906815223/add/ HTTP/2
        # comment_text=asd
        'Host': 'www.instagram.com',
        'Cookie': f'sessionid={sessionId};',
        'Content-Length': "16",
        'Sec-Ch-Ua': '"Chromium";v="105", "Not)A;Brand";v="8"',
        'X-Ig-App-Id': "936619743392459",
        'X-Ig-Www-Claim': 'hmac.AR3WlVqqF2mw7cTVf2QXVAN8HeOdLCZUKPdo2ruF0UUAk8cJ',
        'X-Requested-With': 'XMLHttpRequest',
        'Sec-Ch-Ua-Mobile': '?0',
        'X-Instagram-Ajax': '1006893658',
        'Viewport-Width': '945',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'X-Csrftoken': '""',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36',
        'X-Asbd-Id': '198387',
        'Sec-Ch-Prefers-Color-Scheme': 'light',
        'Sec-Ch-Ua-Platform': '"Linux"',
        'Origin': '"https://www.instagram.com"',
        'Sec-Fetch-Site': '"same-origin"',
        'Sec-Fetch-Mode': '"cors"',
        'Sec-Fetch-Dest': '"empty"',
        "Referer":"https://www.instagram.com/p/CnkARriOkZB/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
    }

def commentPostHeaders(sessionId: str):
    return {
        # POST /api/v1/web/comments/3013319255906815223/add/ HTTP/2
        # comment_text=asd
        'Host': 'www.instagram.com',
        'Cookie': f'sessionid={sessionId};',
        'Content-Length': "16",
        'Sec-Ch-Ua': '"Chromium";v="105", "Not)A;Brand";v="8"',
        'X-Ig-App-Id': "936619743392459",
        'X-Ig-Www-Claim': 'hmac.AR3WlVqqF2mw7cTVf2QXVAN8HeOdLCZUKPdo2ruF0UUAk8cJ',
        'X-Requested-With': 'XMLHttpRequest',
        'Sec-Ch-Ua-Mobile': '?0',
        'X-Instagram-Ajax': '1006893658',
        'Viewport-Width': '945',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'X-Csrftoken': '""',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36',
        'X-Asbd-Id': '198387',
        'Sec-Ch-Prefers-Color-Scheme': 'light',
        'Sec-Ch-Ua-Platform': '"Linux"',
        'Origin': '"https://www.instagram.com"',
        'Sec-Fetch-Site': '"same-origin"',
        'Sec-Fetch-Mode': '"cors"',
        'Sec-Fetch-Dest': '"empty"',
        "Referer":"https://www.instagram.com/p/CnkARriOkZB/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
    }

#POST /api/v1/web/accounts/edit/ HTTP/2
def instaEditProfile(cookiesDict):
    headersDict = tranRowIntoDictHeaders('./data/rowHeaders/editProfile')
    headersDict['Cookie'] = convertDicCookiesIntoRow(cookiesDict)
    for cookie in cookiesDict:
        if cookie['name'] == 'csrftoken':
            headersDict['X-Csrftoken'] = cookie['value']
            break
    return headersDict

#GET /api/v1/accounts/edit/web_form_data/ HTTP/2
def web_form_data(cookiesDict):
    headersDict = tranRowIntoDictHeaders('./data/rowHeaders/web_form_data')
    headersDict['Cookie'] = convertDicCookiesIntoRow(cookiesDict)
    for cookie in cookiesDict:
        if cookie['name'] == 'csrftoken':
            headersDict['X-Csrftoken'] = cookie['value']
            break
    return headersDict

"""
    https://i.instagram.com/rupload_igphoto/fb_uploader_1681322457455
    POST /rupload_igphoto/fb_uploader_1681322457555 HTTP/2
    
    
    Custom Headers_To_Add:
        X-Instagram-Rupload-Params: {"media_type":1,"upload_id":"1681322457555","upload_media_height":1080,"upload_media_width":1080}
        X-Entity-Name: fb_uploader_1681322457555
"""
def rupload_igphoto(cookiesDict):
    headersDict = tranRowIntoDictHeaders('./data/rowHeaders/rupload_igphoto')
    headersDict['Cookie'] = convertDicCookiesIntoRow(cookiesDict)
    return headersDict

"""
    POST /api/v1/media/configure/ HTTP/2

    data 
        source_type=library,
        caption=,
        upload_id=1681322457555,
        disable_comments=0,
        like_and_view_counts_disabled=0,
        igtv_share_preview_to_feed=1,
        is_unified_video=1,
        video_subtitles_enabled=0,
        disable_oa_reuse=false
"""
def media_configure(cookiesDict):
    headersDict = tranRowIntoDictHeaders('./data/rowHeaders/media_configure')
    headersDict['Cookie'] = convertDicCookiesIntoRow(cookiesDict)
    for cookie in cookiesDict:
        if cookie['name'] == 'csrftoken':
            headersDict['X-Csrftoken'] = cookie['value']
            break
    return headersDict

def instaPostLikers(sessionIdCookie):
    headersDict = tranRowIntoDictHeaders('./data/rowHeaders/instaPostLikers')
    headersDict['Cookie'] += f'ds_user_id=; sessionid={sessionIdCookie};'
    return headersDict