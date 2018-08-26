from flask import Flask, jsonify, request
import FacebookFunctions
import FirebaseFunctions

app = Flask(__name__)

@app.route('/', methods=['GET'])
def test():
    return jsonify({"status" : "ok"})

@app.route('/sendMessage/<string:fbUserID>/<string:messageId>', methods=['GET'])
def sendTheMessage(fbUserID, messageId):
    if FacebookFunctions.sendMessage(fbUserID, messageId):
        return jsonify({"status" : "ok"})
    else:
        return jsonify({"status" : "not ok"})

@app.route('/createUser/<string:uid>/<string:password>', methods=['GET'])
def registerUser(uid, password):
    FirebaseFunctions.registerAccount(uid, password)
    return jsonify({"status" : "ok"})

@app.route('/getUserFriends/<string:uid>', methods=['GET'])
def getUserFriends(uid):
    return jsonify(FacebookFunctions.sendFriends(uid))

if __name__ == '__main__':
    app.run()
