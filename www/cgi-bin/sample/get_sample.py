from multiprocessing import freeze_support
# import recaptcha
import time
import os
import signal
import cgi
import sys
#import signal
import functools
import json
sys.path.append('/home/raojh')
import astropy.cosmology
import pandas as pd
from collections import namedtuple
from pprint import pprint
import numpy as np

config={}
event_type='bhns'
population='I'
T=24.*60.*365*20
config['time']=T
new_theta=None

cosmology_list=['WMAP5','WMAP7','WMAP9','Planck13','Planck15','Planck18']

for cosmos in cosmology_list:
    

    cosmology = getattr(astropy.cosmology, cosmos)
    if isinstance(cosmology, astropy.cosmology.core.Cosmology):
        config['cosmology'] = cosmology
    elif issubclass(cosmology, astropy.cosmology.core.Cosmology):
        H0=float(form.getvalue('H0'))
        Om0=float(form.getvalue('omega'))
        Tcmb0=float(form.getvalue('Tcmb'))
        config['cosmology'] = cosmology(H0=H0, Om0=Om0, Tcmb0=Tcmb0)
    else:
        raise ValueError('Unrecognised cosmology')



    if __name__=='__main__':
        # the path is the server
        #os.environ["FINESSE_DIR"] = os.getenv("FINESSE_DIR") or  "/home/raojh/miniconda3/envs/tes/bin/"
        #os.environ["KATINI"] = os.getenv("KATINI") or "/home/raojh/miniconda3/envs/tes/bin/"

        t=time.time()
        # the path to the main codes
        sys.path.insert(0, '../../../gwtoolbox')

        # import the gwtoolbox code
        from gwtoolbox.tools_earth import Tools
        #from gwtoolbox import parameters
        #from gwtoolbox import plotshtml as gwplots
        from gwtoolbox import constants

        ET_tool = Tools('et',
                        event_type,
                        'I',
                        config['cosmology'],
                        #det_setup=setup,
                        new_theta=new_theta)

        tot_all=ET_tool.total_number(time_obs=config['time'], rho_cri=0.)    #rho_cri? SNR? 
        tot_poisson=np.random.poisson(lam=tot_all)
        print(f'tot_poisson{cosmos}:',tot_poisson)

        size=100000  #here we define the size 
        numevents2 = min(tot_poisson, size)################################################################      
        eventall = ET_tool.list_params_df(time_obs=config['time'],rho_cri=0., size=numevents2,dtp=True)
        ET_tool.list_with_iota(eventall)


        df=eventall.copy()
        with open(f'{event_type}_params_df_10w_{cosmos}.json', 'w') as f:
            json.dump(df.to_json(orient='records'), f)

        print(time.time()-t)
