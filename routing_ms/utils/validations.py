import logging
import re

logging.basicConfig(filename='logysto_router.log', filemode='a', format='%(asctime)s %(levelname)s => %(message)s')
logging.root.setLevel(logging.INFO)

def validacion_param(request_data,cmps):            
            f = 0
            for c in range(0,len(cmps)):
                exs = request_data.get(cmps[c])
                if exs is None:  
                    f=f+1
                else:
                    if cmps[c]=='source':
                        if type(request_data.get(cmps[c])) is not dict or len(request_data.get(cmps[c]))!=2:                            
                            f=f+1
                            logging.warning("Parametros incompletos 408a - Source Invalido")
                        org = request_data.get(cmps[c])
                        if org.get('lat') is None or org.get('lon') is None:
                            f=f+1
                            logging.warning("Parametros incompletos 408b - Coordenada Invalido")
                        else:
                            if type(request_data.get(cmps[c])['lat']) is not float or type(request_data.get(cmps[c])['lon']) is not float:
                                f=f+1
                                logging.warning("Parametros incompletos 408c - Valor Coordenada Source Invalido")                       
                    elif cmps[c]=='veh_mot' or cmps[c]=='veh_aut' or cmps[c]=='veh_carry' or cmps[c]=='veh_nh' or cmps[c]=='veh_cam':
                         if type(request_data.get(cmps[c])) is not int:
                            f=f+1
                            logging.warning("Parametros incompletos 408d - Valor de Vehiculos Invalido")     

            return f

def validacion_srv(request_data,flds):
            ent_vrf=[]  
            ent_error=[]   
            for s in request_data.get('services'):                           
                k = 0
                for c in range(0,len(flds)):
                    patttime = re.compile(r'([0-1][0-9]|[2][0-3]):([0-5][0-9]):([0-5][0-9])')
                    exs = s.get(flds[c])                    
                    if exs is not None:                         
                        if flds[c]=='id' and len(str(exs))>0:
                            k = k +1                            
                        elif ((flds[c]=='lat' or flds[c]=='lon') and type(exs) is float) and ((flds[c]=='lat' and exs>-90 and exs<90) or (flds[c]=='lon' and exs>-180 and exs<180)):
                            k = k +1                            
                        elif flds[c]=='size' and exs>=0 and exs<5:
                            k = k +1                            
                        elif flds[c]=='t_start' and len(exs)==8 and patttime.search(exs) is not None:                            
                            k = k +1                            
                        elif flds[c]=='t_end' and len(exs)==8 and patttime.search(exs) is not None:                            
                            k = k +1                            
                        elif (flds[c]=='l' or flds[c]=='h' or flds[c]=='w') and exs>0 and exs<100:
                            k = k +1
                        elif flds[c]=='origen':
                            scoo = s.get("origen")                                                         
                            ltsrc = scoo.get("lat")                    
                            lnsrc = scoo.get("lon")             
                            if (type(ltsrc) is float and type(lnsrc) is float and ltsrc>-90 and ltsrc<90 and lnsrc>-180 and lnsrc<180):                                                                   
                                k = k +1                           
                        elif flds[c]=='destino':
                            dcoo = s.get("destino")                                                         
                            ltdst = dcoo.get("lat")                    
                            lndst = dcoo.get("lon")             
                            if (type(ltdst) is float and type(lndst) is float and ltdst>-90 and ltdst<90 and lndst>-180 and lndst<180):                                                                   
                                k = k +1                                           

                if k == len(flds):
                    ent_vrf.append(s)
                else:
                    if s.get('id') is not None:                    
                        ent_error.append(s.get('id'))
                    else:
                        ent_error.append("ID")                                                          

            request_data['invalid'] = ent_error
            return len(ent_vrf)