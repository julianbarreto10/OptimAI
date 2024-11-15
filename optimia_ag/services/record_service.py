from consumers.drivers_ms.driver_consumer import *
from consumers.routing_ms.routing_consumer import *
from consumers.bi_ms.bi_consumer import *

class RecordService:

    @staticmethod
    def create_record_service(data):

        if data["ms-drivers"] == 1:
            driver_data = data['ms-drivers-info'][0]
            try:
                driver = create_driver(driver_data)
                return True, "Drivers successfully created"
            except:
                return False
        
        elif data["ms-routing"] == 1:
            routing_data = data["ms-routing-info"][0]
            try:
                routing = create_routing(routing_data)
                return True, str(routing.json())
            except:
                return False


        elif data["ms-bi"] == 1:
            cliente = data['ms-bi-info'][0]['client_id']
            try:
                data_bi = get_bi_info(cliente)
                return True, str(data_bi.json())
            except:
                return False
        else:
            return False