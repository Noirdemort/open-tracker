from flask import Blueprint, request, jsonify
from model import User, Device
#from .utils import *

usr_api_blueprint = Blueprint("User", __name__)

# public key + nonce -> id
# Message Received
# signed with server's public key -> signed with your private key -> verified with your public key -> verified with server's private key
# Message sent
# signed with your public key -> signed with server's private key -> verified with server public key -> verified with your private key

# MARK: User
@usr_api_blueprint.route("/user", methods=["POST"])
@usr_api_blueprint.route("/user/<id>", methods=["DELETE", "PUT"])
def account(id=None):
    data = request.json if request.json else {}
    
    # create account
    if request.method == "POST":
        # - send your public key signed with server's public key and nonce
#        nonce = data.get("nonce", "")
#        usr_key = data.get("public_key", None)
#        verified = verify_key_validity(usr_key, nonce)
#        if not verified:
#            return jsonify({"message": "The key is invalid"}), 400

        status = User.create(data)
        if isinstance(status, User):
            return jsonify({"user_id": status.id}), 201
        
        return jsonify({"message": "User Creation unsuccessful!"}), 406
    
    user = User.read(id)
    if not user:
        return jsonify({"message": "User not found"}), 400
    
#    if not verify_full_chain(user["public_key"], user["token"]):
#        return jsonify({"message": "Unauthorized access"}), 403
    
    # delete account
    if request.method == "DELETE":
        count = User.delete(id)
        return jsonify({"user_deleted": count }), 202
        # - all related devices are deleted
        # - account is deleted
    
    # update account
    if request.method == "PUT":
        update_count = User.update(id, data)
        return jsonify({"user_updated": count }), 200


# MARK:- Device
@usr_api_blueprint.route("/device", methods=["POST"])
@usr_api_blueprint.route("/device/<id>", methods=["DELETE", "PUT"])
def manage_device(id=None):
    data = request.json if request.json else {}
    # author-id
    # author_sign
    user_id = data.get("user_id", None)
#    user_sign = data.get("author_sign", None)
    user = User.read(user_id)
    if not user:
        return jsonify({"message": "User not found!"}), 403
        
#    if not verify_full_chain(user["public_key"], user_sign):
#        return jsonify({"message": "message tempered!"}), 403

    # add device
    # - send device data signed with your private key
    # - parse devices and make sure ip-address with user's private key and signed with it as well
    
    if request.method == "POST":
        status = Device.create(data)
        if isinstance(status, Device):
            return jsonify({"device_id": status.id}), 200
        
        return jsonify({"message": "Device creation unsuccessful"}), 406

    if not id:
        return jsonify({"message": "Device ID not found"}), 400
    
    # delete device
    # - device id signed with private key
    if request.method == "DELETE":
        count = Device.delete(id)
        return jsonify({"deleted_count": count}), 202
    
    # update device - use this to log device as well
    # - new data signed with private key is updated
    if request.method == "PUT":
        count = Device.update(id, data)
        return jsonify({"updated_count": count}), 200
    

@usr_api_blueprint.route("/device/<id>", methods=["GET"])
@usr_api_blueprint.route("/devices/<id>", methods=["GET"])
def search_device(id):
    data = dict(request.args)
    
    # return all devices for the user
    if "/devices/" in request.url:
        return jsonify({ "devices": Device.read(id, all=True) })
    
    return jsonify({ "device": Device.read(id) })

#@usr_api_blueprint.route("/token", methods=["GET"])
#def get_nonce():
#    # request a nonce encrypted and signed by server's private key
#    nonce = generate_nonce()
##    nonce = prepare_payload(nonce)
#    return jsonify({"nonce": nonce}), 200
    
