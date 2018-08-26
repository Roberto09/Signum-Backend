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

    for key, name in friendsToSend.items():
        msg = Message("test")
        friends = client.searchForUsers(name)
        print(msg, " ", name)
        sent = client.send(msg, friends[0].uid)
        if sent:
            return True
        else:
            return False
