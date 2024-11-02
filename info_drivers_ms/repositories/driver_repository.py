from models.driver import Driver, db

class DriverRepository:

    @staticmethod
    def create_driver_repository(name, email, tp_veh, capacity, client_id):

        driver = Driver(name=name, email=email, tp_veh=tp_veh, capacity=capacity, client_id=client_id)
        
        db.session.add(driver)
        db.session.commit()

        return driver