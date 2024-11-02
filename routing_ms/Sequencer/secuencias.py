
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2




   
def sub_model(ENR1,into_route,id_org,cp_start,returns=False):
  ENR1['VH']=into_route
  CP_start=[]
  for n in (ENR1.groupby('VH').sum()).index:
    if n in CP_start:
      ENR1.loc[ENR1.id==id_org,'VH']=n+1
    else:
      ENR1.loc[ENR1.id==id_org,'VH']=n
    Data=(ENR1.loc[ENR1.VH==n,]).reset_index(drop= True)
    A=np.array(Data.iloc[:,[1,2]])
    B=np.array(Data.iloc[:,[1,2]])
    dist=cdist(A,B,metric='euclidean')
    distancias=dist*100000
    if returns==False:
      distancias[:,0]=0
    distancias=distancias.astype(int)
    def create_subdata_model():
      data = {}
      data['distance_matrix'] = distancias
      data['num_vehicles'] = 1
      if n in CP_start:
        data['depot'] = int(Data[Data.clicoh_pts.notnull()].index[0])
      else:
        data['depot'] = 0
      return data
    def get_routes(solution, routing, manager):
      routes = []
      for route_nbr in range(routing.vehicles()):
        index = routing.Start(route_nbr)
        route = [manager.IndexToNode(index)]
        while not routing.IsEnd(index):
          index = solution.Value(routing.NextVar(index))
          route.append(manager.IndexToNode(index))
        routes.append(route)
      return routes  
    def sub_main():
        data = create_subdata_model()
        manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),data['num_vehicles'], data['depot'])
        routing = pywrapcp.RoutingModel(manager)
        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data['distance_matrix'][from_node][to_node]
        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
        solution = routing.SolveWithParameters(search_parameters)
        if solution:
          routes = get_routes(solution, routing, manager)
          for j in range(0,len(routes[0])-1):
            in_sec=1 if n in CP_start else 0
            Data.loc[routes[0][j],'sec']=j+in_sec
            ENR1.loc[ENR1.VH==n,'sec']=list(Data['sec'])
    sub_main()
