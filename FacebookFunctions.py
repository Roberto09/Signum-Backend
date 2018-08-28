import base64
from Crypto.Cipher import AES
import FirebaseFunctions
import fbchat
from fbchat.models import Message
systemKey = b"SUPERSECRETKEYXD"


def UserPasswordDecrypt(udd):
    cipher = AES.new(udd["Key"], AES.MODE_EAX, base64.b64decode(udd["Nonce"]))
    depass = cipher.decrypt_and_verify(base64.b64decode(udd["Pass"]), base64.b64decode(udd["Tag"]))
    passw = depass.decode('utf-8')
    print(passw)
    return passw


def UserPasswordEncrypt(key, password):
    encoded = password.encode("utf8")
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(encoded)
    userdatadict = {
        "Pass": base64.b64encode(ciphertext),
        "Key": key,
        "Tag": base64.b64encode(tag),
        "Nonce": base64.b64encode(cipher.nonce)
    }
    return userdatadict

def sendMessage(senderId, messageId):
    #obtiene datos de firebase
    username = senderId
    username = username.replace("_", ".")
    userInfo = FirebaseFunctions.getFirebaseInfo(senderId)
    friendsToSend = userInfo["contacts"]
    messageToSend = userInfo["messages"][int(messageId)]
    userEncryptedPassword = userInfo["encryptedPassword"]
    userTagPassword = userInfo["tag"]
    userNonce = userInfo["nonce"]

    userdatadict = {
        "Pass": userEncryptedPassword,
        "Key": systemKey,
        "Tag": userTagPassword,
        "Nonce": userNonce
    }

    #desenctipta contraseña
    userDectyptedPassword = UserPasswordDecrypt(userdatadict)

    print(username)
    print(userDectyptedPassword)

    client = fbchat.Client(username, userDectyptedPassword)

    print(friendsToSend.items)
    for key, name in friendsToSend.items():
        print (name)
        msg = Message(messageToSend)
        print(msg, " ", name)
        sent = client.send(msg, name)
        if sent:
            return True
        else:
            return False

def sendFriends(senderId):
    username = senderId
    username = username.replace("_", ".")
    userInfo = FirebaseFunctions.getFirebaseInfo(senderId)
    userEncryptedPassword = userInfo["encryptedPassword"]
    userTagPassword = userInfo["tag"]
    userNonce = userInfo["nonce"]

    userdatadict = {
        "Pass": userEncryptedPassword,
        "Key": systemKey,
        "Tag": userTagPassword,
        "Nonce": userNonce
    }
    #desenctipta contraseña
    userDectyptedPassword = UserPasswordDecrypt(userdatadict)
    client = fbchat.Client(username, userDectyptedPassword)
    friends = client.fetchAllUsers()

    jsonArray = []

    print(type(friends))
    print (friends)
    for user in friends:
        jsonUser = {}
        jsonUser[str(user.name)] = str(user.uid)
        jsonArray.append(jsonUser)
    return jsonArray