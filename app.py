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

@app.route('/createUser', methods=['POST'])
def registerUser():
    print(request.json["uid"], " ", request.json["pass"])
    FirebaseFunctions.registerAccount(request.json["uid"], request.json["pass"])
    return "todo bien"


if __name__ == '__main__':
    app.run()
