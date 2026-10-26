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

import cgi
import astropy.cosmology
from collections import namedtuple
from pprint import pprint
import numpy as np
import json
if __name__=='__main__':
    # the path to the main codes
    gwtoolbox_path = os.getenv("PATH_GWTOOLBOX", sys.executable)
    sys.path.insert(0, gwtoolbox_path)
    # import the gwtoolbox code
    from gwtoolbox.tools_earth import Tools
    #from gwtoolbox import parameters
    #from gwtoolbox import plotshtml as gwplots
    from gwtoolbox import constants

    # Get the fields from the form 
    form = cgi.FieldStorage()
    #print("form:", file=sys.stderr)
    #print(form, file=sys.stderr)

    def format_response(response):
        """ Prints the content-type header and formts the data as json"""
        sys.__stdout__.write('Content-type: text/json\r\n\r\n')
        json.dump(response, sys.__stdout__)
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
            'individual_params': None,
            'population': None,
            'with_events': None,
            'with_dtp':None,
            'with_errors': None,
            'with_angles': None,
            'max_events': None,
            'cal_snr': False,}
        

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
        if config['event_type'] == 'bhbh':
            config['population'] = form.getvalue('bhbh_population')
            if config['population'] not in ['I', 'II','IS','IIS']:
                error_response('Invalid population')
            if config['population']=='IS':
                config['new_theta'] = {}
                config['new_theta']['R0']=float(form.getvalue('Rn_BBH_IS'))
                config['new_theta']['tau']=float(form.getvalue('tau_BBH_IS'))
                config['new_theta']['mu']=float(form.getvalue('mu_BBH_IS'))
                config['new_theta']['c']=float(form.getvalue('c_BBH_IS'))
                config['new_theta']['gamma']=float(form.getvalue('gamma_BBH_IS'))
                config['new_theta']['mcut']=float(form.getvalue('mcut_BBH_IS'))
                config['new_theta']['ql']=float(form.getvalue('ql_BBH_IS'))
                config['new_theta']['sigx']=float(form.getvalue('sigx_BBH_IS'))
                config['population']='I'
            elif config['population']=='IIS':
                config['new_theta'] = {}
                config['new_theta']['R0']=float(form.getvalue('Rn_BBH_IIS'))
                config['new_theta']['tau']=float(form.getvalue('tau_BBH_IIS'))
                config['new_theta']['mu']=float(form.getvalue('mu_BBH_IIS'))
                config['new_theta']['c']=float(form.getvalue('c_BBH_IIS'))
                config['new_theta']['gamma']=float(form.getvalue('gamma_BBH_IIS'))
                config['new_theta']['mcut']=float(form.getvalue('mcut_BBH_IIS'))
                config['new_theta']['m_peak']=float(form.getvalue('mpeak_BBH_IIS'))
                config['new_theta']['m_peak_scale']=float(form.getvalue('mpeakscale_BBH_IIS'))
                config['new_theta']['m_peak_sig']=float(form.getvalue('mpeaksig_BBH_IIS'))
                config['new_theta']['ql']=float(form.getvalue('ql_BBH_IIS'))
                config['new_theta']['sig_x']=float(form.getvalue('sigx_BBH_IIS'))     
                config['population']='II'      
        elif config['event_type'] == 'bhns':
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
        elif config['event_type'] == 'inds':
            config['population'] = 'I'
            config['individual_params'] = {}
            try:
                config['individual_params']['m1'] = float(form.getvalue('m1_individual'))
            except:
                error_response('Could not parse m1 value for individual event')
            else:
                if config['individual_params']['m1'] <= 0.0:
                    error_response('m1 must be positive for individual event')
            try:
                config['individual_params']['m2'] = float(form.getvalue('m2_individual'))
            except:
                error_response('Could not parse m2 value for individual event')
            else:
                if config['individual_params']['m2'] <= 0.0:
                    error_response('m2 must be positive for individual event')
            try:
                config['individual_params']['chi'] = float(form.getvalue('chi_individual'))
            except:
                error_response('Could not parse chi value for individual event')
            else:
                if abs(config['individual_params']['chi']) > 1.0:
                    error_response('Absolute value of chi must be less than or equal to 1 for individual event')
            try:
                config['individual_params']['z'] = float(form.getvalue('z_individual'))
            except:
                if form.getvalue('z_individual') is None:
                    config['individual_params']['z'] = None
                    try:
                        config['individual_params']['D'] = float(form.getvalue('D_individual'))
                    except:
                        if form.getvalue('D_individual') is None:
                            error_response('z or D must be provided for individual event')
                        else:
                            error_response('Could not parse D value for individual event')
                    else:
                        if config['individual_params']['D'] < 0.0:
                            error_response('D must be non-negative for individual event')
                else:
                    error_response('Could not parse z value for individual event')
            else:
                if config['individual_params']['z'] < 0.0:
                    error_response('z must be non-negative for individual event')
                
            config['event_type'] = 'nsns'
            config['cal_snr'] = True
        else:
            error_response('Invalid event type')

        # with_events
        config['with_events'] = form.getvalue('with_events') is not None
        config['with_errors'] = form.getvalue('with_errors') is not None
        config['with_dtp']=form.getvalue('with_dtp') is not None
        config['with_angles']=form.getvalue('with_angles') is not None

        try:
            config['max_events'] = int(form.getvalue('max_events'))
        except Exception as e:
            print(e, file=sys.stderr)
            error_response('Could not parse max_events value')
        else:
            if config['max_events'] <= 0:
                error_response('max_events must be positive')

        return config



    # check captcha
    #if not recaptcha.verify(form.getvalue('recaptcha')):
    #    error_response('Your resquest was deemed too robot-like. Live a little! Aborting.')

    # get a conside job desciption from form inputs:
    config = get_parameters()
    
    tool = Tools(config['detector_type'],
                    config['event_type'],
                    config['population'])
    tool.cosmos = config['cosmology']
    det_setup = []
    if config['setup_ligo'] is not None:
        det_setup.append(config['setup_ligo'])
    if config['setup_et'] is not None:
        det_setup.append(config['setup_et'])
    if det_setup:
        tool.update_detector(det_setup=det_setup)
    if config['new_theta']:
        tool.new_theta = config['new_theta']

    sensitivity = tool.sensitivity_curve()
    response = {}
    response['success'] = True
    response['msg'] = "Success"
    config['cosmology'] = config['cosmology'].name
    config['detector_type'] = tool.detector_type
    response['config'] = config
    response['network'] = tool.network
    if tool.network:
        response['sensitivity'] = [[sen[0].tolist(), sen[1].tolist()] for sen in sensitivity]
    else:
        response['sensitivity'] = [sensitivity[0].tolist(), sensitivity[1].tolist()]
    if config['cal_snr']:
        if tool.network:
            ind_snr, ind_area = tool.snr_area(config['individual_params']['m1'],
                                        config['individual_params']['m2'],
                                        config['individual_params']['chi'],
                                        config['individual_params']['z'],
                                        config['individual_params']['D'],)
            response['e_snr'] = ind_snr
            response['e_area'] = ind_area
        else:
            ind_snr = tool.snr(config['individual_params']['m1'],
                           config['individual_params']['m2'],
                           config['individual_params']['chi'],
                           config['individual_params']['z'],
                           config['individual_params']['D'],)
            response['e_snr'] = ind_snr
    else:
        # do the calculations
        total = tool.total_number(time_obs = config['time'], rho_cri = config['snr'])
        total_poisson=np.random.poisson(lam=total) 
        events = None
        if config['with_events']:
            numevents = min(total_poisson, config['max_events'])
            events = tool.list_params(time_obs=config['time'],
                                    rho_cri=config['snr'], 
                                    size=numevents, 
                                    dtp=config['with_dtp'],
                                    witherrors=config['with_errors'],
                                    withangles=config['with_angles'])
        response['total'] = total
        if config['with_events']:
            # TODO: find a better orientation where the headers are sent even if there are 0 records
            response['events'] = json.loads(events.to_json(orient='records'))
        else:
            response['events'] = []
    # with open('/home/websiteadmin/response_earth.json','w') as f:
    #     json.dump(response,f)
    format_response(response)
