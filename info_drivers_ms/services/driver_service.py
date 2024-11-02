from repositories.driver_repository import DriverRepository

class DriverService:
    
    @staticmethod
    def create_driver_service(data):

        name = data['name']
        email = data['email']
        tp_veh = data['tp_veh']
        capacity = data['capacity']
        client_id = data['client_id']

        return DriverRepository.create_driver_repository(name, email, tp_veh, capacity, client_id)