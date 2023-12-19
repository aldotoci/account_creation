# from config import db
# mockUsernames = [*db.native_acc_creation.find()]
# mockUsernames = [*db.native_android_ig_acc.find()]


mockUsernames = []
rowData = open('./data/userspass1.txt').readlines()
rowData[-1] += "\n"
currentDT = 0

def stringToDict(input_string):
    # Split the input string by semicolon to get individual key-value pairs
    key_value_pairs = input_string.split(";")

    # Create an empty dictionary to store the key-value pairs
    result_dict = {}

    # Iterate through the key-value pairs and add them to the dictionary
    for pair in key_value_pairs:
        # Split each pair by '=' to separate the key and value
        key, value = pair.split("=")

        # Add the key-value pair to the dictionary
        result_dict[key] = value

    # Print the resulting dictionary
    return result_dict

def dictToList(input_dict):
    # Convert the dictionary into the desired list format
    output_list = [{
        'name': key,
        'value': value,
        # 'path': "/",
        # 'domain': ".instagram.com",
        # 'secure': True,
        # 'httpOnly': True,
        # 'expiry': 1726203880,
        # 'sameSite': "None",
    } for key, value in input_dict.items()]

    return output_list

for acc in rowData:
    username = ""
    password = ""
    cookies = ""
    for char in acc[0:-2]:
        if(char == ":" and currentDT != 2):
            currentDT+=1
        else:
            if(currentDT == 0):
                username += char
            elif(currentDT == 1):
                password += char
            elif(currentDT == 2):
                cookies += char
            else:
                pass

    mockUsernames.append({
        "username": username,
        "password": password,
        # "cookies": dictToList(stringToDict(cookies))
    })
    currentDT = 0

