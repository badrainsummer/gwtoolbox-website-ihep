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

import os
import cgi
import sys
import json
import astropy.cosmology
import pandas as pd
from collections import namedtuple
from pprint import pprint
import numpy as np
from astropy import units as u
from io import StringIO
if __name__=='__main__':
    # the path to the main codes
    gwtoolbox_path = os.getenv("PATH_GWTOOLBOX", sys.executable)
    sys.path.insert(0, gwtoolbox_path)

    # import the gwtoolbox code
    from gwtoolbox.tools_earth import Tools
    from gwtoolbox.HE_detectors import *
    from gwtoolbox.HE_models import *
    #from gwtoolbox import parameters
    #from gwtoolbox import plotshtml as gwplots
    from gwtoolbox import constants

    # Get the fields from the form 
    form = cgi.FieldStorage()
    #print("form:", file=sys.stderr)
    #print(form, file=sys.stderr)

    def format_response(response):
        """ Prints the content-type header and formts the data as json"""
        sys.__stdout__.write('Content-type: text/json\r\n\r\n')  # 原始 stdout
        json.dump(response, sys.__stdout__)  # 保证输出到真正 stdout
        quit()

    def error_response(msg):
        format_response({'msg': msg, 'success': False})


    def get_parameters():
        """ Gets the requires fields from the html form, sanitizes input and checks that it's all there and in range"""

        # create a named tuple to contain everything needed
        config = {
            'time': None,
            'snr': None,
            'cosmology': None,
            'detector_type': None,
            'setup_ligo': None,
            'setup_et': None,
            'event_type': None,
            'new_theta': None,
            'population': None,
            'HE_detector_type':None, ########################
            'signal_type':None,     #########################
            'grb_model':None,
            'with_events': None,
            'with_dtp':None,
            'with_errors': None,
            'max_events': None }
        

        # time
        try:
            config['time'] = 24. * 60. * float(form.getvalue('time'))
        except Exception as e:
            print(e, file=sys.stderr)
            error_response('Shuxu: Could not parse time value')
        else:
            if config['time'] <= 0.0:
                error_response('Time must be positive')

        # snr
        try:
            config['snr'] = float(form.getvalue('snr'))
        except:
            error_response('Could not parse snr value')
        else:
            if config['snr'] <= 0.0:
                error_response('SNR must be positive')

        # cosmology
        try:
            cosmology = getattr(astropy.cosmology, form.getvalue('cosmology'))
            if isinstance(cosmology, astropy.cosmology.core.Cosmology):
                config['cosmology'] = cosmology
            elif issubclass(cosmology, astropy.cosmology.core.Cosmology):
                H0=float(form.getvalue('H0'))
                Om0=float(form.getvalue('omega'))
                Tcmb0=float(form.getvalue('Tcmb'))
                config['cosmology'] = cosmology(H0=H0, Om0=Om0, Tcmb0=Tcmb0)
            else:
                raise ValueError('Unrecognised cosmology')
        except:
            error_response('cosmology is not valid')

        # detector type
        config['detector_type'] = form.getvalue('detector_type')

        # arm_length and laser power
        if 'ligo-like' in config['detector_type']:
            config['setup_ligo'] = {}
            try:
                config['setup_ligo']['LARM_VALUE'] = float(form.getvalue('arm_length_ligo'))
            except:
                error_response('Arm length has an invalid value')
            else:
                if config['setup_ligo']['LARM_VALUE'] <= 0.0:
                    error_response('Arm length must be positive')
            # laser_power
            try:
                config['setup_ligo']['PIN_VALUE'] = float(form.getvalue('laser_power_ligo'))
            except:
                error_response('Laser power has an invalid value')
            else:
                if config['setup_ligo']['PIN_VALUE'] <= 0.0:
                    error_response('Laser power must be positive')
            # cavity_mirror_transmission
            try:
                config['setup_ligo']['ITMT_VALUE'] = float(form.getvalue('cavity_mirror_transmission_ligo'))
            except:
                error_response('Cavity mirror transmission coefficient has an invalid value')
            else:
                if config['setup_ligo']['ITMT_VALUE'] <= 0.0:
                    error_response('Cavity mirror transmission coefficient must be positive')
                if config['setup_ligo']['ITMT_VALUE'] >= 1.0:
                    error_response('Cavity mirror transmission coefficient must be less than 1')
            # signal_recycling_transmission
            try:
                config['setup_ligo']['SRMT_VALUE'] = float(form.getvalue('signal_recycling_transmission_ligo'))
            except:
                error_response('Signal recycling mirror transmission coefficient has an invalid value')
            else:
                if config['setup_ligo']['SRMT_VALUE'] <= 0.0:
                    error_response('Signal recycling mirror transmission coefficient must be positive')
                if config['setup_ligo']['SRMT_VALUE'] >= 1.0:
                    error_response('Signal recycling mirror transmission coefficient must be less than 1')
            # power_recycling_transmission
            try:
                config['setup_ligo']['SRMT_VALUE'] = float(form.getvalue('power_recycling_transmission_ligo'))
            except:
                error_response('Power recycling mirror transmission coefficient has an invalid value')
            else:
                if config['setup_ligo']['SRMT_VALUE'] <= 0.0:
                    error_response('Power recycling mirror transmission coefficient must be positive')
                if config['setup_ligo']['SRMT_VALUE'] >= 1.0:
                    error_response('Power recycling mirror transmission coefficient must be less than 1')
            # mirror_mass
            try:
                config['setup_ligo']['MTM_VALUE'] = float(form.getvalue('mirror_mass_ligo'))
            except:
                error_response('Mirror mass has an invalid value')
            else:
                if config['setup_ligo']['MTM_VALUE'] <= 0.0:
                    error_response('Mirror mass must be positive')
            # signal_recycling_phase
            try:
                config['setup_ligo']['SRMPHI_VALUE'] = float(form.getvalue('signal_recycling_phase_ligo'))
            except:
                error_response('Signal recycling phase has an invalid value')
            # power_recycling_length
            try:
                config['setup_ligo']['LPRC_VALUE'] = float(form.getvalue('power_recycling_length_ligo'))
            except:
                error_response('Power recycling cavity length has an invalid value')
            else:
                if config['setup_ligo']['LPRC_VALUE'] <= 0.0:
                    error_response('Power recycling cavity length must be positive')
            # signal_recycling_length
            try:
                config['setup_ligo']['LSRC_VALUE'] = float(form.getvalue('signal_recycling_length_ligo'))
            except:
                error_response('Signal recycling cavity length has an invalid value')
            else:
                if config['setup_ligo']['LSRC_VALUE'] <= 0.0:
                    error_response('Signal recycling cavity length must be positive')

        if 'et-like' in config['detector_type']:
            config['setup_ligo'] = {}
            try:
                config['setup_ligo']['LARM_VALUE'] = float(form.getvalue('arm_length_et'))
            except:
                error_response('Arm length has an invalid value')
            else:
                if config['setup_ligo']['LARM_VALUE'] <= 0.0:
                    error_response('Arm length must be positive')
            # laser_power
            try:
                config['setup_ligo']['PIN_VALUE'] = float(form.getvalue('laser_power_et'))
            except:
                error_response('Laser power has an invalid value')
            else:
                if config['setup_ligo']['PIN_VALUE'] <= 0.0:
                    error_response('Laser power must be positive')
            # cavity_mirror_transmission
            try:
                config['setup_ligo']['ITMT_VALUE'] = float(form.getvalue('cavity_mirror_transmission_et'))
            except:
                error_response('Cavity mirror transmission coefficient has an invalid value')
            else:
                if config['setup_ligo']['ITMT_VALUE'] <= 0.0:
                    error_response('Cavity mirror transmission coefficient must be positive')
                if config['setup_ligo']['ITMT_VALUE'] >= 1.0:
                    error_response('Cavity mirror transmission coefficient must be less than 1')
            # signal_recycling_transmission
            try:
                config['setup_ligo']['SRMT_VALUE'] = float(form.getvalue('signal_recycling_transmission_et'))
            except:
                error_response('Signal recycling mirror transmission coefficient has an invalid value')
            else:
                if config['setup_ligo']['SRMT_VALUE'] <= 0.0:
                    error_response('Signal recycling mirror transmission coefficient must be positive')
                if config['setup_ligo']['SRMT_VALUE'] >= 1.0:
                    error_response('Signal recycling mirror transmission coefficient must be less than 1')
            # power_recycling_transmission
            try:
                config['setup_ligo']['SRMT_VALUE'] = float(form.getvalue('power_recycling_transmission_et'))
            except:
                error_response('Power recycling mirror transmission coefficient has an invalid value')
            else:
                if config['setup_ligo']['SRMT_VALUE'] <= 0.0:
                    error_response('Power recycling mirror transmission coefficient must be positive')
                if config['setup_ligo']['SRMT_VALUE'] >= 1.0:
                    error_response('Power recycling mirror transmission coefficient must be less than 1')
            # mirror_mass
            try:
                config['setup_ligo']['MTM_VALUE'] = float(form.getvalue('mirror_mass_et'))
            except:
                error_response('Mirror mass has an invalid value')
            else:
                if config['setup_ligo']['MTM_VALUE'] <= 0.0:
                    error_response('Mirror mass must be positive')
            # signal_recycling_phase
            try:
                config['setup_ligo']['SRMPHI_VALUE'] = float(form.getvalue('signal_recycling_phase_et'))
            except:
                error_response('Signal recycling phase has an invalid value')
            # power_recycling_length
            try:
                config['setup_ligo']['LPRC_VALUE'] = float(form.getvalue('power_recycling_length_et'))
            except:
                error_response('Power recycling cavity length has an invalid value')
            else:
                if config['setup_ligo']['LPRC_VALUE'] <= 0.0:
                    error_response('Power recycling cavity length must be positive')
            # signal_recycling_length
            try:
                config['setup_ligo']['LSRC_VALUE'] = float(form.getvalue('signal_recycling_length_et'))
            except:
                error_response('Signal recycling cavity length has an invalid value')
            else:
                if config['setup_ligo']['LSRC_VALUE'] <= 0.0:
                    error_response('Signal recycling cavity length must be positive')

        # event_type and population
        config['event_type'] = form.getvalue('event_type')   
        if config['event_type'] == 'bhns':
            config['population'] = form.getvalue('bhns_population')
            if config['population'] not in ['I','IS','II','IIS']:
                error_response('Invalid population')
            if config['population']=='IS':
                config['new_theta'] = {}
                config['new_theta']['R0']=float(form.getvalue('Rn_BHNS_IS'))
                config['new_theta']['tau']=float(form.getvalue('tau_BHNS_IS'))
                config['new_theta']['m_mean']=float(form.getvalue('mmean_BHNS_IS'))
                config['new_theta']['m_scale']=float(form.getvalue('mscale_BHNS_IS'))
                config['new_theta']['m_low']=float(form.getvalue('mlow_BHNS_IS'))
                config['new_theta']['m_high']=float(form.getvalue('mhigh_BHNS_IS'))
                config['new_theta']['mu']=float(form.getvalue('mu_BHNS_IS'))
                config['new_theta']['c']=float(form.getvalue('c_BHNS_IS'))
                config['new_theta']['gamma']=float(form.getvalue('gamma_BHNS_IS'))
                config['new_theta']['mcut']=float(form.getvalue('mcut_BHNS_IS'))     
                config['new_theta']['chi_sigma']=float(form.getvalue('sigx_BHNS_IS'))           
                config['population']='I'
            elif config['population']=='IIS':
                config['new_theta'] = {}
                config['new_theta']['R0']=float(form.getvalue('Rn_BHNS_IIS'))
                config['new_theta']['tau']=float(form.getvalue('tau_BHNS_IIS'))
                config['new_theta']['m_mean']=float(form.getvalue('mmean_BHNS_IIS'))
                config['new_theta']['m_scale']=float(form.getvalue('mscale_BHNS_IIS'))
                config['new_theta']['m_low']=float(form.getvalue('mlow_BHNS_IIS'))
                config['new_theta']['m_high']=float(form.getvalue('mhigh_BHNS_IIS'))
                config['new_theta']['mu']=float(form.getvalue('mu_BHNS_IIS'))
                config['new_theta']['c']=float(form.getvalue('c_BHNS_IIS'))
                config['new_theta']['gamma']=float(form.getvalue('gamma_BHNS_IIS'))
                config['new_theta']['mcut']=float(form.getvalue('mcut_BHNS_IIS'))   
                config['new_theta']['m_peak']=float(form.getvalue('mpeak_BHNS_IIS'))
                config['new_theta']['m_peak_scale']=float(form.getvalue('mpeakscale_BHNS_IIS'))
                config['new_theta']['m_peak_sig']=float(form.getvalue('mpeaksig_BHNS_IIS'))
                config['new_theta']['chi_sigma']=float(form.getvalue('sigx_BHNS_IIS'))           
                config['population']='II'                
        elif config['event_type'] == 'nsns':
            config['population'] = form.getvalue('nsns_population')
            if config['population'] not in ['I','IS']:
                error_response('Invalid population')
            if config['population']=='IS':
                config['new_theta'] = {}
                config['new_theta']['R0']=float(form.getvalue('Rn_DNS_IS'))
                config['new_theta']['tau']=float(form.getvalue('tau_DNS_IS'))
                config['new_theta']['m_mean']=float(form.getvalue('mmean_DNS_IS'))
                config['new_theta']['m_scale']=float(form.getvalue('mscale_DNS_IS'))
                config['new_theta']['m_low']=float(form.getvalue('mlow_DNS_IS'))
                config['new_theta']['m_high']=float(form.getvalue('mhigh_DNS_IS'))
                config['new_theta']['chi_sigma']=float(form.getvalue('sigx_DNS_IS')) 
                config['population']='I'
        else:
            error_response('Invalid event type')

        # with_events
        config['with_events'] = form.getvalue('with_events')
        config['with_errors'] = form.getvalue('with_errors')
        config['with_dtp']=form.getvalue('with_dtp')

        try:
            config['max_events'] = int(form.getvalue('max_events'))
        except Exception as e:
            print(e, file=sys.stderr)
            error_response('Could not parse max_events value')
        else:
            if config['max_events'] <= 0:
                error_response('max_events must be positive')

#####################################################################
        # HE detector type
        config['HE_detector_type'] = form.getvalue('HE_detector_type')
        if config['HE_detector_type'] not in ['Fermi_GBM', 'insight_HE', 'GECAM_GRM', 'Swift_BAT', 'Konus']:
            print("Unrecognised detector type: {}".format(config['HE_detector_type']), file=sys.stderr)
            error_response('Unrecognised HE detector type')

        #signal_type
        config['signal_type'] = form.getvalue('signal_type')
        #grb model para
        model_para=None
        config['grb_model'] = form.getvalue('grb_model')
        if config['grb_model']:
            if config['signal_type'] == 'sGRB_p':
                pi=3.1415926
                half_open_mean=float(form.getvalue('half_open_mean'))*pi/180.
                half_open_std=float(form.getvalue('half_open_std'))*pi/180.
                lg_r_grb_mean=float(form.getvalue('lg_r_grb_mean'))
                lg_r_grb_std=float(form.getvalue('lg_r_grb_std'))
                lgEgrb_mean=float(form.getvalue('lgEgrb_mean'))
                lgEgrb_std=float(form.getvalue('lgEgrb_std'))
                nup0_mean=float(form.getvalue('nup0_mean'))
                nup0_std=float(form.getvalue('nup0_std'))
                jet_Gamma_mean=float(form.getvalue('jet_Gamma_mean'))
                jet_Gamma_std=float(form.getvalue('jet_Gamma_std'))
                # Band_alpha=float(form.getvalue('Band_alpha'))
                # Band_beta=float(form.getvalue('Band_beta'))
                # Band_s=float(form.getvalue('Band_s'))
                # t_d_sigma=float(form.getvalue('t_d_sigma'))
                model_para=[half_open_mean,half_open_std, lg_r_grb_mean, lg_r_grb_std,lgEgrb_mean, lgEgrb_std,nup0_mean, nup0_std, jet_Gamma_mean, jet_Gamma_std]
            elif config['signal_type'] == 'sGRB_d':
                L_star=float(form.getvalue('L_star'))
                theta_mean=float(form.getvalue('theta_mean'))*np.pi/180.
                theta_std=float(form.getvalue('theta_std'))*np.pi/180.
                model_para={"L_star": L_star, "theta_mean": theta_mean, "theta_std": theta_std}

###########################################################################
        return [config, model_para]

    config,model_para = get_parameters()
        
    # create the tool for this detector
    tool = Tools(config['detector_type'],
                    config['event_type'],
                    config['population'])
    tool.cosmos = config['cosmology']
    ET_tool = Tools('et',
                    config['event_type'],
                    config['population'])
    ET_tool.cosmos = config['cosmology']
    det_setup = []
    if config['setup_ligo'] is not None:
        det_setup.append(config['setup_ligo'])
    if config['setup_et'] is not None:
        det_setup.append(config['setup_et'])
    if det_setup:
        tool.update_detector(det_setup=det_setup)
    if config['new_theta']:
        tool.new_theta = config['new_theta']
################################################################


    if config['signal_type'] == 'sGRB_p':
        # do the calculations
        total = tool.total_number(time_obs = config['time'], rho_cri = config['snr'])
        total_poisson=np.random.poisson(lam=total) 
        numevents = min(total_poisson, config['max_events'])
        events = tool.list_params(config['time'], config['snr'], numevents,dtp=True, witherrors=config['with_errors'])
        tool.list_with_iota(events)

        ##############################   
        from gwtoolbox.tools_EMC import *
        from gwtoolbox.EM_HE import *
        from gwtoolbox.HE_models import *
        
        if model_para==None:
            model_para=[half_open_mean_,half_open_std_, lg_r_grb_mean_, lg_r_grb_std_,lgEgrb_mean_, lgEgrb_std_,nup0_mean_, nup0_std_, jet_Gamma_mean_, jet_Gamma_std_]

        # Search for GRB
        # model_para=[half_open_mean,half_open_std, lg_r_grb_mean, lg_r_grb_std,lgEgrb_mean, lgEgrb_std,nup0_mean, nup0_std, jet_Gamma_mean, jet_Gamma_std]
        HEtools=High_Energy(event_type=config['event_type'], signal_type=config['signal_type'], detector=config['HE_detector_type'],model_para=model_para,cosmos=config['cosmology'])

        # #df1
        # temp=events[(events['inc']<=40.*pi/180.)&(events['z']<2.5)].copy()
        # events=HEtools.Search_EMC(temp, full=True, verbose=True)
        events=events[events['z']<2.5]
        events=HEtools.Search_EMC(events, full=True, verbose=False)

        #select source that t90<2s
        # events=events[events['T90']<2.]  #when bhns ,there may do not T90 value
        # events.loc[events['detected'] == False, ['T90', 'F_max', 't_max', 'Epeak','fluence']] = np.nan
        events=events.iloc[:,[0,1,2,3,4,5,6,12]]
        #select source that detected and t90<2s
        # events_HE_det=events[(events['detected']==True)&(events['T90']<2)]
        if config['max_events'] < total_poisson:
            total_true=len(events[events['detected']==True])*total_poisson/config['max_events']
        else:
            total_true=len(events[events['detected']==True])

        #all sGRB data by ET , set snr=0
        # ET_tools=Tools(detector_type='et', event_type=config['event_type'], population=config['population'],cosmos=config['cosmology'], new_theta=new_theta)
        tot_all=ET_tool.total_number(time_obs=config['time'], rho_cri=0.)    #rho_cri? SNR? 
        tot_poisson=np.random.poisson(lam=tot_all)

        size=100000  #here we define the size 
        ################################################################  

        #read the sample file,the len=100000
        type=config['event_type']
        cosmos=config['cosmology'].name

        if (config['new_theta'] == None or np.abs(config['new_theta']['tau']-3.)<1e-8) and cosmos in ['WMAP5','WMAP7','WMAP9','Planck13','Planck15','Planck18'] :
            
            with open(f'sample/{type}_params_df_10w_{cosmos}.json', 'r') as f:
                json_str = json.load(f)
            eventall = pd.read_json(StringIO(json_str))
            if tot_poisson < 100000 :
                eventall=eventall.sample(n=tot_poisson, random_state=None)

        else:
            size=50000
            numevents2 = min(tot_poisson, size)    
            eventall = ET_tool.list_params(time_obs=config['time'],rho_cri=0., size=numevents2,dtp=True)
            ET_tool.list_with_iota(eventall)


        #df2
        # temp=eventall[(eventall['inc']<=40.*pi/180.)&(eventall['z']<2)].copy()
        # eventall=HEtools.Search_EMC(temp, full=True, verbose=True);
        # eventall=eventall[eventall['z']<2.5]
        eventall=HEtools.Search_EMC(eventall, full=True, verbose=False)

        #select source that detected,or/and select event that sgrb
        eventall=eventall[eventall['detected']==True]
        # eventall=eventall[(eventall['detected']==True)&(eventall['T90']<2.)]
        eventall=eventall.iloc[:,[0,7,8,9,10,13,14,15,16,17]]
        
        if size < tot_poisson:
            tot_all=len(eventall)*tot_poisson/size
        else:
            tot_all=len(eventall)
        ##################################

    elif config['signal_type'] == 'sGRB_d':
        Erange=HE_detectors[config['HE_detector_type']]['Erange']
        sens=HE_detectors[config['HE_detector_type']]['sens']
        flux_unit=HE_detectors[config['HE_detector_type']]['flux_unit']
        window=HE_detectors[config['HE_detector_type']]['window']
        bkg=HE_detectors[config['HE_detector_type']]['bkg']
        FoV=HE_detectors[config['HE_detector_type']]['FoV']
        correction=HE_detectors[config['HE_detector_type']]['corr']
        E_min, E_max = Erange
        E_avg = np.log(E_max / E_min) / (1 / E_min - 1 / E_max)
        E_avg_erg = E_avg * 1e6 * u.eV.to(u.erg)
        flim = sens * E_avg_erg  # erg/cm^2/s
        lam = FoV * correction

        total = tool.total_number(time_obs = config['time'], rho_cri = config['snr'])
        total_poisson=np.random.poisson(lam=total) 

        tool.create_BNScatalog(T=config['time'], N=config['max_events'])
        events = tool.create_GWcatalog(rho_cri=config['snr'])
        part = max(1, total_poisson / len(events))
        if model_para==None:
            eventall = tool.create_sgrbcatalog(HE_detector=config['HE_detector_type'])
        else:
            eventall = tool.create_sgrbcatalog(HE_detector=config['HE_detector_type'], GRB_parameter=model_para)
        tot_all = len(eventall) * part
        tool.BNScatalog = events
        if model_para==None:
            event_detected = tool.create_sgrbcatalog(HE_detector=config['HE_detector_type'])
        else:
            event_detected = tool.create_sgrbcatalog(HE_detector=config['HE_detector_type'], GRB_parameter=model_para)
        total_true = len(event_detected) * part
    
    # d1=events.copy()
    # with open('events_off.json', 'w') as f:
    #     json.dump(d1.to_json(orient='records'), f)
    
    

    # format a response
    response = {}
    response['success'] = True
    response['msg'] = "Success"
    config['cosmology'] = config['cosmology'].name # To make it serializeable
    response['config'] = config
    response['total'] = total
    response['total_true'] = total_true
    response['tot_all'] = tot_all ######
    # response['sensitivity'] = [sensitivity[0].tolist(), sensitivity[1].tolist()]
    # if default_sensitivity is not None:
    #     response['default_sensitivity'] = [default_sensitivity[0].tolist(),default_sensitivity[1].tolist()]
    # if config['with_events']:
    #     # TODO: find a better orientation where the headers are sent even if there are 0 records
    #     response['events'] = json.loads(events.to_json(orient='records'))
    #     response['eventall'] = json.loads(eventall.to_json(orient='records'))
    # else:
    #     response['events'] = []
    #     response['eventall'] = []

    response['events'] = json.loads(events.to_json(orient='records'))
    response['eventall'] = json.loads(eventall.to_json(orient='records'))

    res=response.copy()
    with open('/home/websiteadmin/response_earth_joint.json','w') as f:
        json.dump(response,f)

    format_response(response)
    

