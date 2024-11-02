from datetime import datetime
import Routings.enrutamientos as lgtenrt
from utils.validations import validacion_param, validacion_srv
from flask import Flask, jsonify, request
import hashlib
import config
import logging


logging.basicConfig(filename='logysto_router.log', filemode='a', format='%(asctime)s %(levelname)s => %(message)s')
logging.root.setLevel(logging.INFO)

app = Flask(__name__)

@app.route('/logysto_router', methods=['POST'])
def logysto_router():    
    try:
        request_data = request.get_json()        
        if request_data is None:
            logging.warning("Parametros incompletos 402")
            return jsonify(success="false", message="Parametros incompletos",error_code="402",data="")
                 
        
        tipo = request_data.get('type')
        if tipo is None:
            logging.warning("Parametros incompletos 405")
            return jsonify(success="false", message="Parametros incompletos",error_code="405",data="")        
                    
        else:

            if request_data.get('services') is None or type(request_data.get('services')) is not list:
                logging.warning("Parametros incompletos 404")
                return jsonify(success="false", message="Parametros incompletos",error_code="404",data="")

            now = datetime.now()
            token = hashlib.sha1( str(now.strftime("%Y%m%d%H%M%S%f")).encode('utf-8') ).hexdigest()               
            ent_vrf = []
            ent_error = []            

            if len(request_data.get('services')) < 2:  
                logging.warning("Cantidad minima excedida 414 - "+str(token))
                return jsonify(success="false", message="Cantidad minima excedida",error_code="414",data="") 
        
            

            if tipo=='routing_static_vh':            
                if len(request_data.get('services')) > config.maximo_srv_vh:  
                    logging.warning("Cantidad maxima excedida 413 - "+str(token))
                    return jsonify(success="false", message="Cantidad excedida",error_code="413",data="")            
                if validacion_param(request_data,['services','veh_mot', 'veh_carry', 'veh_aut','veh_nh','veh_cam'])>0:
                    logging.warning("Parametros incompletos 408 - "+str(token))
                    return jsonify(success="false", message="Parametros incompletos",error_code="408",data="")                
                if validacion_param(request_data,['services'])>0:
                    logging.warning("Parametros incompletos 408 - "+str(token))
                    return jsonify(success="false", message="Parametros incompletos",error_code="408",data="")                
                if validacion_srv(request_data,['id','size','origen','destino'])<1 and (request_data.get('request_id') is None or request_data.get('request_id')==''):                    
                    logging.warning("Cantidad minima excedida 415 - "+str(token))
                    return jsonify(success="false", message="Cantidad minima verificada excedida",error_code="415",data="")
                else:
                    request_data['ent_vrf'] = ent_vrf
                    logging.info("Request '"+tipo+"' aceptado - Servicios vrf="+str(len(request_data['ent_vrf']) )+", invalid="+str(len(request_data['invalid']) )+" - "+str(token))
                    return lgtenrt.router_unif(request_data,token,0,request_data.get('token'),'rtstatic_vh')         
            else:
                logging.error("Metodo Invalido 411 - "+str(token))
                return jsonify(success="false", message="Metodo Invalido",error_code="411",data="")


    except Exception as e:
        logging.error("Exception 400 - "+str(e))
        return jsonify(success="false", message="Error General",error_code="400",data="")
        
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
