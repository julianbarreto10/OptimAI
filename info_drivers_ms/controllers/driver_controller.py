from flask import Blueprint, request, jsonify
from services.driver_service import DriverService

driver_api = Blueprint('driver_api', __name__)

@driver_api.route('/api/driver', methods=['POST'])
def create_driver_controller():

    data = request.get_json()
    DriverService.create_driver_service(data)

    return jsonify("Driver has been successfully created."), 201