#library used for simple queries
import base64
from firebase import firebase
from flask import jsonify
import FacebookFunctions
systemKey = b"SUPERSECRETKEYXD"
fb = firebase.FirebaseApplication('https://emergencyapp-1e7d0.firebaseio.com', None)

def getFirebaseInfo(uid):
    userInfoJson = fb.get("/Users/" + uid, None)
    encryptedPassword = userInfoJson["mypassenc"]
    contacts = userInfoJson["FacebookInfo"]["Contacts"]
    messages = userInfoJson["Messages"]
    nonce = userInfoJson["Nonce"]
    tag = userInfoJson["Tag"]
    return {"idUserFacebook" : uid, "encryptedPassword" : encryptedPassword, "contacts" : contacts, "messages" : messages, "nonce" : nonce, "tag" : tag}

def registerAccount(uid, password):
    dict =  FacebookFunctions.UserPasswordEncrypt(systemKey, password)
    strpass = dict["Pass"].decode("utf8")
    strtag = dict["Tag"].decode("utf8")
    strnonce = dict["Nonce"].decode("utf8")
    #fb.post('/Users', "uid:", jsonify({"mypassenc": strpass, "Tag" : strtag, "Nonce" : strnonce}),  params={'print': 'silent'}, headers={'X_FANCY_HEADER': 'VERY FANCY'})
    fb.put('/Users/'+uid, "mypassenc", strpass, params={'print': 'silent'}, headers={'X_FANCY_HEADER': 'VERY FANCY'})
    fb.put('/Users/'+uid, "Tag", strtag, params={'print': 'silent'}, headers={'X_FANCY_HEADER': 'VERY FANCY'})
    fb.put('/Users/'+uid, "Nonce", strnonce, params={'print': 'silent'}, headers={'X_FANCY_HEADER': 'VERY FANCY'})
    fb.put('/Users/'+uid+"/Messages/", 0, "Hola, me encuentro bien actualmente, me pondre en contacto contigo pronto.", params={'print': 'silent'}, headers={'X_FANCY_HEADER': 'VERY FANCY'})
    fb.put('/Users/'+uid+"/Messages/", 1, "Hola, me encuentro mal, ayuda.", params={'print': 'silent'}, headers={'X_FANCY_HEADER': 'VERY FANCY'})