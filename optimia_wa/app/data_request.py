from app.record_consumer import create_record


def driver_request(data):
    dt={"ms-drivers": 1,
    "ms-drivers-info": [data],
    "ms-routing": 0,
    "ms-routing-info": [],
    "ms-bi": 0,
    "ms-bi-info": []}
    message=create_record(dt)
    return message

def router_request(data):
    dt={"ms-drivers": 0,
    "ms-drivers-info": [],
    "ms-routing": 1,
    "ms-routing-info": [data],
    "ms-bi": 0,
    "ms-bi-info": []}
    message=create_record(dt)
    return message

def bi_request(data):
    dt={"ms-drivers": 0,
    "ms-drivers-info": [],
    "ms-routing": 0,
    "ms-routing-info": [],
    "ms-bi": 1,
    "ms-bi-info": [data]}
    message=create_record(dt)
    return message