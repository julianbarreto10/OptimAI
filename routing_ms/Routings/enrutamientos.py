import config
import pandas as pd
import numpy as np
import math
from flask import jsonify
import Sequencer.secuencias as lgtsec
import logging
from scipy.spatial.distance import cdist
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
from datetime import datetime
import json
import warnings
warnings.filterwarnings('ignore')
import traceback


logging.basicConfig(filename='logysto_router.log', filemode='a', format='%(asctime)s %(levelname)s => %(message)s')
logging.root.setLevel(logging.INFO)

def router_unif(rqst,token,tp,tokenrequest,router_type):
    try:  
        if router_type=='rtstatic_vh':
            try:
                logging.info("1"+str(token))
                cliente=rqst['client_id']
                data=rqst
                fecha=str(datetime.now())
                # Crear lista para almacenar los datos
                trng = []
                logging.info("1"+str(token))

                # Agregar la primera fila (origen) con cont = 0
                origen = data['services'][0]['origen']
                trng.append([0, origen['lat'], origen['lon'], 0, 0])

                # Agregar las filas de destino para cada servicio con cont = 1
                for i, service in enumerate(data['services'], start=1):
                    destino = service['destino']
                    trng.append([i, destino['lat'], destino['lon'], service['size'], 1])

                # Convertir a DataFrame y renombrar columnas
                ENR = pd.DataFrame(trng, columns=['id', 'lat', 'lon', 'vol', 'cont'])
                ENR['sec']=0
                A=np.array(ENR.iloc[:,[1,2]])
                B=np.array(ENR.iloc[:,[1,2]])
                dist=cdist(A,B,metric='euclidean')
                distancias=dist*100000
                distancias=distancias.astype(int)
                logging.info("2"+str(token))
                distancias[:,0]=0
                
                n_motos=int(rqst['veh_mot'])
                n_carro=int(rqst['veh_aut'])
                n_carry=int(rqst['veh_carry'])
                n_nh=int(rqst['veh_nh'])
                n_cam=int(rqst['veh_cam'])
                no_ort=0
                if n_motos+n_carro+n_carry+n_nh+n_cam ==0:
                  logging.warning("Numero de vehiculos invalido - "+str(token))
                  return jsonify(success="false", message="Numero de vehiculos invalido",error_code="420",data="", invalid="")
                if n_motos+n_carro+n_carry+n_nh+n_cam ==1:
                  ENR['Ruta']=1
                  lgtsec.sub_model(ENR,list(ENR['Ruta']),0,False)
                  no_ort=1
                if (int(config.max_vol_cam)*n_cam+int(config.max_vol_nh)*n_nh+int(config.max_vol_carry)*n_carry+int(config.max_vol_carro)*n_carro+int(config.max_vol_moto)*n_motos)<sum(ENR['vol'])*config.vol_pkt_pequeño:
                  logging.warning("Volumen de enrutamiento superior a la capacidad de los vehiculos 1 - "+str(token))
                  return jsonify(success="false", message="Volumen de enrutamiento superior a la capacidad de los vehiculos",error_code="417",data="", invalid="")
                A=[] #.
                logging.info("3"+str(token))
                if (len(ENR)-1)/(n_carry+n_carro+n_nh+n_cam+n_motos) <=config.max_pktbase_moto:
                  max_c=math.ceil((len(ENR)-1)/(n_carry+n_carro+n_nh+n_cam+n_motos))
                  max_m=max_c
                else:
                  max_m=config.max_pktbase_moto
                  if n_carry+n_carro+n_nh+n_cam!=0:
                    max_c=math.ceil((len(ENR)-1-(config.max_pktbase_moto*n_motos))/(n_carry+n_carro+n_nh+n_cam))
                  else:
                    max_c=0
                if max_c>60: max_c=60
                if (max_c*n_cam+max_c*n_nh+max_c*n_carry+max_c*n_carro+max_m*n_motos)<len(ENR)-1:
                  logging.warning("Volumen de enrutamiento superior a la capacidad de los vehiculos 1 - "+str(token))
                  return jsonify(success="false", message="Volumen de enrutamiento superior a la capacidad de los vehiculos",error_code="417",data="", invalid="")
                def create_data_model():
                  data = {}
                  data['distance_matrix'] = distancias
                  data['demands'] = [x*3500 for x in list(ENR['vol'])]
                  data['vehicle_capacities'] =list([int(config.max_vol_cam)]*n_cam+[int(config.max_vol_nh)]*n_nh+[int(config.max_vol_carry)]*n_carry+[int(config.max_vol_carro)]*n_carro+[int(config.max_vol_moto)]*n_motos)
                  data['cont']=ENR['cont']
                  data['vehicle_cont']=[int(max_c)]*(n_carry+n_carro+n_nh+n_cam)+[int(max_m)]*n_motos
                  data['num_vehicles'] = n_carry+n_carro+n_nh+n_cam+n_motos
                  data['depot'] = 0
                  return data
                def print_solution(data, manager, routing, solution):
                    total_distance = 0
                    total_load = 0
                    for vehicle_id in range(data['num_vehicles']):
                        index = routing.Start(vehicle_id)
                        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
                        C=[] #.
                        route_distance = 0
                        route_load =0
                        while not routing.IsEnd(index):
                            node_index = manager.IndexToNode(index)
                            route_load += data['demands'][node_index]
                            '''route_nivel += data['nivel'][node_index]'''
                            plan_output += ' {0} Load({1})-> '.format(node_index, route_load)
                            '''plan_output += ' {0} Load({1}) ({2}) -> '.format(node_index, route_load,route_nivel )'''
                            C.append(node_index) #.
                            previous_index = index
                            index = solution.Value(routing.NextVar(index))
                            route_distance += routing.GetArcCostForVehicle(
                                previous_index, index, vehicle_id)
                        plan_output += ' {0} Load({1})\n'.format(manager.IndexToNode(index),
                                                                route_load)
                        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
                        plan_output += 'Load of the route: {}\n'.format(route_load)
                        A.append(C)
                        total_distance += route_distance
                        total_load += route_load
                        '''total_nivel += route_nivel'''
                    return A
                def ortools2():
                    data = create_data_model()
                    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                                          data['num_vehicles'], data['depot']) 
                    routing = pywrapcp.RoutingModel(manager)
                    def distance_callback(from_index, to_index):
                        from_node = manager.IndexToNode(from_index)
                        to_node = manager.IndexToNode(to_index)
                        return data['distance_matrix'][from_node][to_node]
                    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
                    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
                    
                    def demand_callback(from_index):
                        from_node = manager.IndexToNode(from_index)
                        return data['demands'][from_node]
                    demand_callback_index = routing.RegisterUnaryTransitCallback(
                        demand_callback)
                    routing.AddDimensionWithVehicleCapacity(
                        demand_callback_index,
                        0,  # null capacity slack
                        data['vehicle_capacities'],  # vehicle maximum capacities
                        True,  # start cumul to zero
                        'Capacity')
                    def cont_callback(from_index):
                      from_node = manager.IndexToNode(from_index)
                      return data['cont'][from_node]
                    cont_callback_index = routing.RegisterUnaryTransitCallback(
                        cont_callback)
                    routing.AddDimensionWithVehicleCapacity(
                        cont_callback_index,
                        0,  # null capacity slack
                        data['vehicle_cont'],  # vehicle maximum capacities
                        True,  # start cumul to zero
                        'Cuenta')
                    

                    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
                    search_parameters.first_solution_strategy = (
                        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
                    search_parameters.local_search_metaheuristic = (
                        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
                    search_parameters.time_limit.FromSeconds(360)
                    if int(0.9*len(ENR))< 450 :
                      search_parameters.solution_limit = int(0.9*len(ENR))
                    else:
                      search_parameters.solution_limit = int(0.9*len(ENR))
                    solution = routing.SolveWithParameters(search_parameters)
                    if solution:
                      print_solution(data, manager, routing, solution)   
                if no_ort==0:
                  ortools2()
                  if len(A)==0:
                    logging.warning("Volumen de enrutamiento superior a la capacidad de los vehiculos 2 - "+str(token))
                    return jsonify(success="false", message="Volumen de enrutamiento superior a la capacidad de los vehiculos",error_code="417",data="", invalid="")
                if no_ort==1:
                  L=(ENR.loc[ENR.Ruta==1,]).sort_values( by= 'sec')
                  A.append(list(L.index))
                x, y, J, P=[1],[0],[0],[]
                for i in range(0,len(A)):
                  for j in range(1,len(A[i])):
                    J.append(A[i][j])
                J=sorted(J)
                J.append(len(ENR))

                def missing_elements(L,start,end,missing_num):
                    complete_list = range(start,end+1)
                    count = 0
                    input_index = 0
                    for item  in  complete_list:
                        if item != L[input_index]:
                            P.append(item)
                            count += 1
                        else :
                            input_index += 1
                        if count > missing_num:
                            break
                L = J
                missing_elements(L,0,len(ENR),100000)


                if len(P)> 0:
                  A.append(P)
                for i in range(1,len(ENR)):
                  for j in range(0,len(A)):
                    if i in A[j]:
                      x.append(j+1)
                      if j < n_cam:
                        y.append('camion')
                      elif j < n_nh+n_cam:
                          y.append('nh')
                      elif j <n_nh+n_cam+n_carry:
                          y.append('carry')
                      elif j < n_carry+n_carro+n_nh+n_cam:
                          y.append('carro')
                      elif j < n_motos+ n_carro+n_carry+n_nh+n_cam: 
                          y.append('moto')
                      elif j == n_carry+n_carro+n_nh+n_cam:
                          y.append('sin ruta')
                for i in range(0,len(A)):
                  for j in range(1,len(A[i])):
                    ENR.loc[A[i][j],'sec']=j

                
                ENR['Ruta']=x
                ENR['type']=y
                ENR['costo']=0
                ENR['Tiempo']=300
                ENR['Distancia']=0
                ENR['costo']=1000
                logging.info("4"+str(token))

                   
                for i,j in enumerate(np.sort(ENR['Ruta'].unique()),1):
                  ENR.loc[ENR.Ruta==j,'Ruta']=i
                
                print(ENR)
                logging.info("5"+str(ENR))
                logging.info("5"+str(ENR))
                #lgtsec.sub_model(ENR,list(ENR['Ruta']),0,False)
                logging.info("5"+str(token))
                H_ruta=ENR.loc[1:,['id','lat','lon','vol','sec','Ruta','type','costo','Tiempo','Distancia']]
                logging.info("5"+str(token))
                         
                ent_excl_0= list(rqst['invalid'])

                ex_df= pd.DataFrame({
                    'id': ent_excl_0,})
                # Convertir H_ruta a lista de diccionarios por cada fila
                rutas = H_ruta.to_dict(orient='records')
                logging.info("6"+str(token))

                # Construir el documento JSON
                documento_json = {
                    "cliente": cliente,
                    "fecha": fecha,
                    "token": token,
                    "rutas": rutas,
                    "invalidos": list(rqst["invalid"])
                }

                # Convertir a JSON
                documento_json_str = documento_json

                      
                logging.info("Termina Enrutamiento - "+str(token))
                return jsonify(success="true", message="Enrutamiento Completo",error_code="",data=documento_json_str)            

            except Exception as e:
                logging.error("Exception 459 - "+str(e))        
                return jsonify(success="false", message="Error General",error_code="419",data="", invalid="")
    
    except Exception as e:
        logging.error("Exception 479 - "+str(e))    
        logging.error("Exception 479 - "+str(traceback.print_exc()))      
        return jsonify(success="false", message="Error General",error_code="479",data="", invalid="")