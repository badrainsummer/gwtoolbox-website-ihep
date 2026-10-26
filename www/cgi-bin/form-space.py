#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

class DevNull:
    def write(self, _): pass
    def flush(self): pass
sys.stdout = DevNull()

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
python_exec = os.getenv("PY_EXEC_GW", sys.executable)
conda_dir = os.getenv("CONDA_PATH", "")
home_dir = os.getenv("HOME_PATH", "")
terminal = os.getenv("TERMINAL", "")

if os.path.realpath(sys.executable) != os.path.realpath(python_exec) or os.environ.get("CONDA_DEFAULT_ENV") != "gwtoolbox":
    cmd = f'''
    source {conda_dir}/etc/profile.d/conda.sh > /dev/null 2>&1
    conda activate gwtoolbox > /dev/null 2>&1
    exec {python_exec} {" ".join(sys.argv)}
    '''
    os.execve(terminal, [terminal, "-c", cmd], os.environ)
os.environ["HOME"] = home_dir

from multiprocessing import freeze_support
import recaptcha
import time
tick=time.time()
import numpy as np
import pandas as pd
import os
import json
if __name__=='__main__':
    freeze_support();
    import cgi
    gwtoolbox_path = os.getenv("PATH_GWTOOLBOX", sys.executable)
    sys.path.insert(0, gwtoolbox_path)

    from astropy.constants import c
    from gwtoolbox.tools_space import Tools, set_cosmology
    from gwtoolbox import parameters
    from gwtoolbox import plotshtml as gwplots
    from gwtoolbox.sources_mHz import *

    def format_response(response):
        """ Prints the content-type header and formts the data as json"""
        sys.__stdout__.write('Content-type: text/json\r\n\r\n')
        json.dump(response, sys.__stdout__)
        quit()

    def error_response(msg):
        format_response({'msg': msg, 'success': False})

    form = cgi.FieldStorage()

    tock=time.time()
    time_initialize=tock-tick
    if not recaptcha.verify(form.getvalue('recaptcha')):
        error_response("You're requests are deemed too robot-like. Aborting.")
    _cosmology = form.getvalue('cosmo_model') # string
    _obs_time = form.getvalue('obs_time') # float, read in days, convert to minutes
    _detector_id  = form.getvalue('detector_name') # 0 1 -1 2 -2
    _snr = form.getvalue('signal_to_noise') # float
    _det_arm = form.getvalue('det_arm') # float
    _det_laser_power = form.getvalue('det_laser_power') # float
    _det_dia = form.getvalue('det_dia') # float
    if form.getvalue('Sacc0')!=None:
        _det_sacc0=float(form.getvalue('Sacc0')) # float
    #_det_sacc0=1e-4
    else:
        _det_sacc0=form.getvalue('Sacc0') # float
    if form.getvalue('Sops')!=None:
        _det_sops0=float(form.getvalue('Sops')) # float
    else:
        _det_sops0=form.getvalue('Sopo0')
    if form.getvalue('Sopo0'):
        _det_sopo0=float(form.getvalue('Sopo0')) # float
    else:
        _det_sopo0=form.getvalue('Sopo0')
    #_mbhb = form.getvalue('mbhb') # 1
    _sourcetype_mHz=form.getvalue('sourcetype_mHz')
    _mbhb_pop = form.getvalue('mbhb_pop') # 0 1
    #_gb = form.getvalue('gb') # 1
    _gwd_pop = form.getvalue('gwd_pop') # 0 1
    #_emri = form.getvalue('emri') # 1
    _emri_pop = form.getvalue('emri_pop') # 0 1

    if _sourcetype_mHz == '1' and _mbhb_pop == '0':
        _M1 = form.getvalue('mbhb_M1')
        if not _M1:
            _M1 = 1000000
        else :
            _M1 = float(_M1)
        _M2 = form.getvalue('mbhb_M2')
        if not _M2:
            _M2 = 100000
        else :
            _M2 = float(_M2)
        _z = form.getvalue('mbhb_z')
        _D = form.getvalue('mbhb_d')
        if _D:
            _D = float(_D)
        elif _z:
            _z = float(_z)
        else:
           _D = 4400
        _s1 = form.getvalue('mbhb_s1')
        if not _s1:
            _s1 = 0.5
        else :
            _s1 = float(_s1)
        _s2 = form.getvalue('mbhb_s2')
        if not _s2:
            _s2 = 0.3
        else :
            _s2 = float(_s2)
        _ra = form.getvalue('mbhb_ra')
        if not _ra:
            _ra = 2
        else :
            _ra = float(_ra)
        _dec = form.getvalue('mbhb_dec')
        if not _dec:
            _dec = 0.5
        else :
            _dec = float(_dec)

    if _sourcetype_mHz == '2' and _gwd_pop == '0':
        _M1 = form.getvalue('gwd_M1')
        if not _M1:
            _M1 = 1000000
        else :
            _M1 = float(_M1)
        _M2 = form.getvalue('gwd_M2')
        if not _M2:
            _M2 = 100000
        else :
            _M2 = float(_M2)
        _z = form.getvalue('gwd_z')
        _D = form.getvalue('gwd_d')
        if _D:
            _D = float(_D)
        elif _z:
            _z = float(_z)
        else:
           _D = 4400
        _f = form.getvalue('gwd_f')
        if not _f:
            _f = 0.5
        else :
            _f = float(_f)
        _fdot = form.getvalue('gwd_fdot')
        if not _fdot:
            _fdot = 0.3
        else :
            _fdot = float(_fdot)
        _ra = form.getvalue('gwd_ra')
        if not _ra:
            _ra = 2
        else :
            _ra = float(_ra)
        _dec = form.getvalue('gwd_dec')
        if not _dec:
            _dec = 0.5
        else :
            _dec = float(_dec)
          
    if _sourcetype_mHz == '3' and _emri_pop == '0':
        _mu = form.getvalue('emri_mu')
        if not _mu:
            _mu = 27
        else :
            _mu = float(_mu)
        _M = form.getvalue('emri_M')
        if not _M:
            _M = 1e6
        else :
            _M = float(_M)
        _s = form.getvalue('emri_s')
        if not _s:
            _s = 0.99
        else :
            _s = float(_s)
        _e = form.getvalue('emri_e')
        if not _e:
            _e = 0.047
        else :
            _e = float(_e)
        _iota = form.getvalue('emri_iota')
        if not _iota:
            _iota = 0.9
        else :
            _iota = float(_iota)
        _gamma = form.getvalue('emri_gamma')
        if not _gamma:
            _gamma = 3.6
        else :
            _gamma = float(_gamma)
        _phi = form.getvalue('emri_phi')
        if not _phi:
            _phi = 2.1
        else :
            _phi = float(_phi)
        _alpha = form.getvalue('emri_alpha')
        if not _alpha:
            _alpha = 5.1
        else :
            _alpha = float(_alpha)
        _thetas = form.getvalue('emri_thetas')
        if not _thetas:
            _thetas = 2.1
        else :
            _thetas = float(_thetas)
        _phis = form.getvalue('emri_phis')
        if not _phis:
            _phis = 3.4
        else :
            _phis = float(_phis)
        _thetak = form.getvalue('emri_thetak')
        if not _thetak:
            _thetak = 0.41
        else :
            _thetak = float(_thetak)
        _phik = form.getvalue('emri_phik')
        if not _phik:
            _phik = 5.2
        else :
            _phik = float(_phik)
        _D = form.getvalue('emri_d')
        if not _D:
            _D = 13
        else :
            _D = float(_D)

    _output = form.getvalue('output') # string
    if _output == "table":
        _sample_size =  form.getvalue('output_size_table')
    elif _output == "table2":
        _sample_size =  form.getvalue('output_size_table2')
    #elif _output == "plot_vs":
    #    _sample_size =  form.getvalue('output_size_plot')
    #

    if '_cosmology' in locals():
       if _cosmology in ['FlatLambdaCDM','WMAP5','WMAP7','WMAP9','Planck13','Planck15']:
         cosmology = _cosmology
       else:
         quit()

    if '_obs_time' in locals():
     if _obs_time != None: 
      try:
        obs_time = float(_obs_time)*0.00273790926 # read in days, convert into years
      except:
        quit()
     else:
        obs_time = parameters.TIME_OBS_EARTH

        
    if '_snr' in locals():
     if _snr != None:
      try:
        snr = float(_snr)
      except:
        quit()
     else:
        snr = parameters.RHO_CRIT_EARTH

    if '_detector_id' in locals():
      try:
        detector_id = int(_detector_id)
        if detector_id not in [-1, 0]:
          quit() 
      except:
        error_response("Please choose a detector")


    if '_det_arm' in locals():
     if _det_arm != None:
      try:
        det_arm = float(_det_arm)
      except:
        quit()

    if '_det_laser_power' in locals():
     if _det_laser_power != None:
      try:
        det_laser_power = float(_det_laser_power)
      except:
        quit()

    if '_det_dia' in locals():
        if _det_dia != None:
            try:
                det_dia = float(_det_dia)
            except:
                quit()
    if '_det_sacc0' in locals():
        if _det_sacc0 != None:
            try:
                det_sacc0 = float(_det_sacc0)
            except:
                quit()

    if '_det_sops0' in locals():
        if _det_sops0 != None:
            try:
                det_sops0 = _det_sops0
            except:
                quit()

    if '_det_sopo0' in locals():
        if _det_sopo0 != None:
            try:
                det_sopo0 = _det_sopo0
            except:
                quit()


    if _sourcetype_mHz=='1':
        if _mbhb_pop=='1':
            populations=0.1
        elif _mbhb_pop=='2':
            populations=0.2
        elif _mbhb_pop=='3':
            populations=0.3
        #populations=0.+float(_mbhb_pop)*0.1
    elif _sourcetype_mHz=='2':
        populations=1.+float(_gwd_pop)*0.1
    elif _sourcetype_mHz=='3':
        populations=2.+float(_emri_pop)*0.01
    else : pass
    #if '_mbhb' in locals() and _mbhb != None:
    #  if int(_mbhb) == 1:
    #      populations.append(float('0.'+_mbhb_model))
    #if '_gb' in locals() and _gb != None:
    #  if int(_gb) == 1:
    #    populations.append(float('1.'+_gb_model))
    #if '_emri' in locals() and _emri != None:
    #  if int(_emri) == 1:
    #    populations.append(float('2.'+_emri_model))

    #population model not specified yet

    output_table = output_table2 = output_ind =  False
    if '_output' in locals():
    #  if _output == 'sensfun':
         #output_sensfun = True     
        if _output == 'table':
            output_table = True
        elif _output == 'table2':
            output_table2= True
        #elif _output == 'plot_vs':
        #   output_plot_vs = True
        else:
            error_response("Please choose an output type")
    else:
        quit()
    if (_sourcetype_mHz == '1' and _mbhb_pop=='0') or (_sourcetype_mHz == '2' and _gwd_pop=='0') or (_sourcetype_mHz == '3' and _emri_pop=='0'):
        output_ind = True

    tick=time.time()
    time_readinform=tick-tock

    if output_table or output_table2:
        if '_sample_size' in locals():
            try:
                sample_size = int(_sample_size)
            except:
                sample_size = parameters.SAMPLE_SIZE

    # set cosmology
    if cosmology in ['WMAP5','WMAP7','WMAP9','Planck13','Planck15']:
        cosmos=set_cosmology(cosmology)
    elif cosmology=='FlatLambdaCDM':
        H0=float(form.getvalue('H0'))
        Om0=float(form.getvalue('omega'))
        Tcmb=float(form.getvalue('Tcmb'))
        cosmos=set_cosmology(cosmoID=cosmology,H0=H0,Om0=Om0,Tcmb=Tcmb)
    tock=time.time()
    time_setoutput_cosmos=tock-tick

    from numpy import sqrt
    from gwtoolbox.detectors_space import LisaLike
    if detector_id == 0:
            # 0 is virgo, 1 is ligo, 4 is kagra
        new_det = LisaLike(Tobs=obs_time)
    else:
        new_det = LisaLike(lisaLT=det_arm/c.value, lisaD=det_dia, lisaP=det_laser_power, Sacc0=det_sacc0, Sopo0=det_sopo0, Sops0=det_sops0, Tobs=obs_time)
    frequencies=np.logspace(-5,0,500)
        #x=np.linspace(1e-5,1,500)
    noises = new_det.S_michaelson(frequencies)
    noises_sqrt=np.sqrt(noises)
    response= {} # respose in a json
    response['success'] = True
    response['sensitivity'] = [frequencies.tolist(), noises_sqrt.tolist()]
    # print total number of detected sources

    if output_ind:
        if _sourcetype_mHz == '1':
            from gwtoolbox.sources_mHz import SMBHB
            from gwtoolbox.functions_space import redshift_from_luminosity_distance
            from gwtoolbox.parameters import MBHBunits
            if not _D:
                _D = cosmos.luminosity_distance(_z).to(u.Gpc).value
            elif not _z:
                _z = redshift_from_luminosity_distance(_D*u.Gpc,cosmos=cosmos)
            source = SMBHB(pop_model=None,cosmos=cosmos)
            pars = {}
            par_list = [_ra,_dec,0,0,0,0,_s1,_s2,_M1,_M2,0,0,np.pi/3,np.pi/2,None,0,_z,_D,(obs_time*u.yr).to(u.s).value,'text']
            for key, val in zip(MBHBunits.keys(),par_list):
                pars[key]=val
            p=ParsUnits(pars_i=pars, units_i=MBHBunits)
            snr_GB = source.SNR(p,new_det)
            # err_GB = source.errors(p,new_det,0.1)
            snr = "{:.2f}".format(snr_GB)
        elif _sourcetype_mHz == '2':
            from gwtoolbox.sources_mHz import GB
            from gwtoolbox.functions_space import intriamp,redshift_from_luminosity_distance
            if not _D:
                _D = cosmos.luminosity_distance(_z).to(u.kpc).value
            source = GB(pop_model=None,cosmos=cosmos)
            amp = intriamp(_M1,_M2,_D,_f*1e3)
            inc = np.pi
            pars = np.array([_f,_fdot,_dec,_ra,amp,inc,1,1,1,_M1,_M2,_D])
            snr_GB = source.SNR_speed(pars,obs_time,0.1,det=new_det)
            # err_GB = source.errors(pars,det=new_det,Tobs=obs_time,dt=0.1)
            snr = "{:.2f}".format(snr_GB)
        elif _sourcetype_mHz == '3':
            from gwtoolbox.sources_mHz import EMRI
            source=EMRI(pop_model=None,cosmos=cosmos)
            # pars=[10000000,np.log(_mu),np.log(_M),_e,0.01,_gamma,_phi,np.cos(_thetas),_phis,_iota,_alpha,_s,np.cos(_thetak),_phik,_D]
            pars=[10000000,np.log(_mu)-12.22096,np.log(_M)-12.22096,_e,0.01,_gamma,_phi,np.cos(_thetas),_phis,_iota,_alpha,_s,np.cos(_thetak),_phik,_mu*4.7869e-23/_D]
            snr_emri = source.SNR(pars, new_det, obs_time)
            snr = "{:.2f}".format(snr_emri)
            # snr = 1000
        response['snr'] = snr

    # print table with parameters
    elif output_table:
        tick=time.time()
        Tyears = obs_time 
        if Tyears < 0.1 or Tyears >= 10:
            error_response("Please set observing time between 0.1 and 10 years.")
        if (detector_id < 0):
            det_setup=[det_arm / c.value, det_laser_power, det_dia, det_sacc0, det_sopo0, det_sops0]
        else:
            det_setup=[8.3391, 2., 0.3]
        t=Tools(Tobs=Tyears, popID=populations, cosmos=cosmos, det_setup=det_setup)
        df, tot_num = t.dataframe(rho_cri=snr ,size=sample_size)
        sample_size_u=min(sample_size,int(tot_num))
        response['events']=json.loads(df.to_json(orient='records'))
        response['total']=tot_num
    elif output_table2:
        tick=time.time()
        Tyears = obs_time
        if Tyears < 0.1 or Tyears > 10:
            error_response("Please set observing time between 0.1 and 10 years.")
        if (detector_id < 0):
            det_setup=[det_arm / c.value, det_laser_power, det_dia, det_sacc0, det_sopo0, det_sops0]
        else:
            det_setup=[8.3391, 2., 0.3]
        t=Tools(Tobs=Tyears, popID=populations, cosmos=cosmos, det_setup=det_setup)
        df, tot_num=t.errordataframe(rho_cri=snr, size=sample_size)
        tock=time.time()
        time_totalnum=tock-tick
        sample_size_u=min(sample_size,int(tot_num))

        response['events']=json.loads(df.to_json(orient='records'))
        response['total']=tot_num
    else:
        quit()
    res=response.copy()

    format_response(response)
