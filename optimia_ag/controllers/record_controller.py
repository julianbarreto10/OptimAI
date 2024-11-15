from flask import Blueprint, request, jsonify
from services.record_service import RecordService

record_api = Blueprint('record_api', __name__)

@record_api.route('/api/record', methods=['POST'])
def create_record_controller():

    data = request.get_json()

    response,message = RecordService.create_record_service(data)

    if response == True:
        return jsonify(message), 201

    return jsonify("Error"), 400