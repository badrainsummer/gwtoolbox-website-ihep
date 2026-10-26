#!/Users/rjh/miniconda3/bin/python3
#/Users/rjh/miniconda3/bin/python3
# this shebang line replaces the path on the server. when developping locally
# the addition to the path will simply be ignored.
# Please change the first line of the file to the address of the python program you are using.

import os
import json
import cgi
import sys
import pandas as pd
import astropy.cosmology
# import numpy as np

if __name__=='__main__':
    # the path is the server
    os.environ["FINESSE_DIR"] = os.getenv("FINESSE_DIR") or  "/Users/rjh/miniconda3/bin/"
    os.environ["KATINI"] = os.getenv("KATINI") or "/Users/rjh/miniconda3/bin/"

    form = cgi.FieldStorage()

    def format_response(response):
        """ Prints the content-type header and formts the data as json"""
        print('Content-type:text/json\r\n\r\n')
        json.dump(response, sys.stdout)
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
            'arm_length': None,
            'laser_power': None,
            'cavity_mirror_transmission': None,
            'signal_recycling_transmission': None,
            'power_recycling_transmission': None,
            'mirror_mass': None,
            'signal_recycling_phase': None,
            'power_recycling_length': None,
            'signal_recycling_length': None,
            'event_type': None,
            'population': None,
            'HE_detector_type':None, ########################
            'signal_type':None,     #########################
            'grb_model':None,######################
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
        if config['detector_type'] not in ['ligo', 'virgo', 'et', 'kagra', 'ligo-like', 'et-like','ligo-o3','ce1','ce2']:
            print("Unrecognised detector type: {}".format(config['detector_type']), file=sys.stderr)
            error_response('Unrecognised detector type')


        # arm_length and laser power
        if config['detector_type'] == 'ligo-like':
            # arm_length
            try:
                config['arm_length'] = float(form.getvalue('arm_length_ligo'))
            except:
                error_response('Arm length has an invalid value')
            else:
                if config['arm_length'] <= 0.0:
                    error_response('Arm length must be positive')
            # laser_power
            try:
                config['laser_power'] = float(form.getvalue('laser_power_ligo'))
            except:
                error_response('Laser power has an invalid value')
            else:
                if config['laser_power'] <= 0.0:
                    error_response('Laser power must be positive')
            # cavity_mirror_transmission
            try:
                config['cavity_mirror_transmission'] = float(form.getvalue('cavity_mirror_transmission_ligo'))
            except:
                error_response('Cavity mirror transmission coefficient has an invalid value')
            else:
                if config['cavity_mirror_transmission'] <= 0.0:
                    error_response('Cavity mirror transmission coefficient must be positive')
                if config['cavity_mirror_transmission'] >= 1.0:
                    error_response('Cavity mirror transmission coefficient must be less than 1')
            # signal_recycling_transmission
            try:
                config['signal_recycling_transmission'] = float(form.getvalue('signal_recycling_transmission_ligo'))
            except:
                error_response('Signal recycling mirror transmission coefficient has an invalid value')
            else:
                if config['signal_recycling_transmission'] <= 0.0:
                    error_response('Signal recycling mirror transmission coefficient must be positive')
                if config['signal_recycling_transmission'] >= 1.0:
                    error_response('Signal recycling mirror transmission coefficient must be less than 1')
            # power_recycling_transmission
            try:
                config['power_recycling_transmission'] = float(form.getvalue('power_recycling_transmission_ligo'))
            except:
                error_response('Power recycling mirror transmission coefficient has an invalid value')
            else:
                if config['power_recycling_transmission'] <= 0.0:
                    error_response('Power recycling mirror transmission coefficient must be positive')
                if config['power_recycling_transmission'] >= 1.0:
                    error_response('Power recycling mirror transmission coefficient must be less than 1')
            # mirror_mass
            try:
                config['mirror_mass'] = float(form.getvalue('mirror_mass_ligo'))
            except:
                error_response('Mirror mass has an invalid value')
            else:
                if config['mirror_mass'] <= 0.0:
                    error_response('Mirror mass must be positive')
            # signal_recycling_phase
            try:
                config['signal_recycling_phase'] = float(form.getvalue('signal_recycling_phase_ligo'))
            except:
                error_response('Signal recycling phase has an invalid value')
            # power_recycling_length
            try:
                config['power_recycling_length'] = float(form.getvalue('power_recycling_length_ligo'))
            except:
                error_response('Power recycling cavity length has an invalid value')
            else:
                if config['power_recycling_length'] <= 0.0:
                    error_response('Power recycling cavity length must be positive')
            # signal_recycling_length
            try:
                config['signal_recycling_length'] = float(form.getvalue('signal_recycling_length_ligo'))
            except:
                error_response('Signal recycling cavity length has an invalid value')
            else:
                if config['signal_recycling_length'] <= 0.0:
                    error_response('Signal recycling cavity length must be positive')

        if config['detector_type'] == 'et-like':
            # arm_length
            try:
                config['arm_length'] = float(form.getvalue('arm_length_et'))
            except:
                error_response('Arm length has an invalid value')
            else:
                if config['arm_length'] <= 0.0:
                    error_response('Arm length must be positive')
            # laser_power
            try:
                config['laser_power'] = float(form.getvalue('laser_power_et'))
            except:
                error_response('Laser power has an invalid value')
            else:
                if config['laser_power'] <= 0.0:
                    error_response('Laser power must be positive')
            # cavity_mirror_transmission
            try:
                config['cavity_mirror_transmission'] = float(form.getvalue('cavity_mirror_transmission_et'))
            except:
                error_response('Cavity mirror transmission coefficient has an invalid value')
            else:
                if config['cavity_mirror_transmission'] <= 0.0:
                    error_response('Cavity mirror transmission coefficient must be positive')
                if config['cavity_mirror_transmission'] >= 1.0:
                    error_response('Cavity mirror transmission coefficient must be less than 1')
            # signal_recycling_transmission
            try:
                config['signal_recycling_transmission'] = float(form.getvalue('signal_recycling_transmission_et'))
            except:
                error_response('Signal recycling mirror transmission coefficient has an invalid value')
            else:
                if config['signal_recycling_transmission'] <= 0.0:
                    error_response('Signal recycling mirror transmission coefficient must be positive')
                if config['signal_recycling_transmission'] >= 1.0:
                    error_response('Signal recycling mirror transmission coefficient must be less than 1')
            # power_recycling_transmission
            try:
                config['power_recycling_transmission'] = float(form.getvalue('power_recycling_transmission_et'))
            except:
                error_response('Power recycling mirror transmission coefficient has an invalid value')
            else:
                if config['power_recycling_transmission'] <= 0.0:
                    error_response('Power recycling mirror transmission coefficient must be positive')
                if config['power_recycling_transmission'] >= 1.0:
                    error_response('Power recycling mirror transmission coefficient must be less than 1')
            # mirror_mass
            try:
                config['mirror_mass'] = float(form.getvalue('mirror_mass_et'))
            except:
                error_response('Mirror mass has an invalid value')
            else:
                if config['mirror_mass'] <= 0.0:
                    error_response('Mirror mass must be positive')
            # signal_recycling_phase
            try:
                config['signal_recycling_phase'] = float(form.getvalue('signal_recycling_phase_et'))
            except:
                error_response('Signal recycling phase has an invalid value')
            # power_recycling_length
            try:
                config['power_recycling_length'] = float(form.getvalue('power_recycling_length_et'))
            except:
                error_response('Power recycling cavity length has an invalid value')
            else:
                if config['power_recycling_length'] <= 0.0:
                    error_response('Power recycling cavity length must be positive')
            # signal_recycling_length
            try:
                config['signal_recycling_length'] = float(form.getvalue('signal_recycling_length_et'))
            except:
                error_response('Signal recycling cavity length has an invalid value')
            else:
                if config['signal_recycling_length'] <= 0.0:
                    error_response('Signal recycling cavity length must be positive')

        # event_type and population
        new_theta=None;
        config['event_type'] = form.getvalue('event_type')
        if config['event_type'] == 'bhbh':
            config['population'] = form.getvalue('bhbh_population')
            if config['population'] not in ['I', 'II','IS','IIS']:
                error_response('Invalid population')
            if config['population']=='IS':
                Rn=float(form.getvalue('Rn_BBH_IS'))
                tau=float(form.getvalue('tau_BBH_IS'))
                mu=float(form.getvalue('mu_BBH_IS'))
                c=float(form.getvalue('c_BBH_IS'))
                gamma=float(form.getvalue('gamma_BBH_IS'))
                mcut=float(form.getvalue('mcut_BBH_IS'))
                ql=float(form.getvalue('ql_BBH_IS'))
                sigx=float(form.getvalue('sigx_BBH_IS'))
                new_theta=[Rn,tau,mu,c,gamma,mcut,ql,sigx]
                config['population']='I'
            elif config['population']=='IIS':
                Rn=float(form.getvalue('Rn_BBH_IIS'))
                tau=float(form.getvalue('tau_BBH_IIS'))
                mu=float(form.getvalue('mu_BBH_IIS'))
                c=float(form.getvalue('c_BBH_IIS'))
                gamma=float(form.getvalue('gamma_BBH_IIS'))
                mcut=float(form.getvalue('mcut_BBH_IIS'))
                mpeak=float(form.getvalue('mpeak_BBH_IIS'))
                mpeakscale=float(form.getvalue('mpeakscale_BBH_IIS'))
                mpeaksig=float(form.getvalue('mpeaksig_BBH_IIS'))
                ql=float(form.getvalue('ql_BBH_IIS'))
                sigx=float(form.getvalue('sigx_BBH_IIS'))  
                new_theta=[Rn,tau,mu,c,gamma,mcut,mpeak,mpeakscale,mpeaksig,ql,sigx]
                #np.savetxt("new_theta_wtf.txt", new_theta)     
                config['population']='II'      
        elif config['event_type'] == 'bhns':
            config['population'] = form.getvalue('bhns_population')
            if config['population'] not in ['I','IS','II','IIS']:
                error_response('Invalid population')
            if config['population']=='IS':
                Rn=float(form.getvalue('Rn_BHNS_IS'))
                tau=float(form.getvalue('tau_BHNS_IS'))
                mmean=float(form.getvalue('mmean_BHNS_IS'))
                mscale=float(form.getvalue('mscale_BHNS_IS'))
                mlow=float(form.getvalue('mlow_BHNS_IS'))
                mhigh=float(form.getvalue('mhigh_BHNS_IS'))
                mu=float(form.getvalue('mu_BHNS_IS'))
                c=float(form.getvalue('c_BHNS_IS'))
                gamma=float(form.getvalue('gamma_BHNS_IS'))
                mcut=float(form.getvalue('mcut_BHNS_IS'))     
                sigx=float(form.getvalue('sigx_BHNS_IS'))           
                new_theta=[Rn,tau,mmean,mscale,mlow,mhigh,mu,c,gamma,mcut,sigx]
                config['population']='I'
            elif config['population']=='IIS':
                Rn=float(form.getvalue('Rn_BHNS_IIS'))
                tau=float(form.getvalue('tau_BHNS_IIS'))
                mmean=float(form.getvalue('mmean_BHNS_IIS'))
                mscale=float(form.getvalue('mscale_BHNS_IIS'))
                mlow=float(form.getvalue('mlow_BHNS_IIS'))
                mhigh=float(form.getvalue('mhigh_BHNS_IIS'))
                mu=float(form.getvalue('mu_BHNS_IIS'))
                c=float(form.getvalue('c_BHNS_IIS'))
                gamma=float(form.getvalue('gamma_BHNS_IIS'))
                mcut=float(form.getvalue('mcut_BHNS_IIS'))   
                mpeak=float(form.getvalue('mpeak_BHNS_IIS'))
                mpeakscale=float(form.getvalue('mpeakscale_BHNS_IIS'))
                mpeaksig=float(form.getvalue('mpeaksig_BHNS_IIS'))
                sigx=float(form.getvalue('sigx_BHNS_IIS'))           
                new_theta=[Rn,tau,mmean,mscale,mlow,mhigh,mu,c,gamma,mcut,mpeak,mpeakscale,mpeaksig,sigx]
                config['population']='II'                
        elif config['event_type'] == 'nsns':
            config['population'] = form.getvalue('nsns_population')
            if config['population'] not in ['I','IS']:
                error_response('Invalid population')
            if config['population']=='IS':
                Rn=float(form.getvalue('Rn_DNS_IS'))
                tau=float(form.getvalue('tau_DNS_IS'))
                mmean=float(form.getvalue('mmean_DNS_IS'))
                mscale=float(form.getvalue('mscale_DNS_IS'))
                mlow=float(form.getvalue('mlow_DNS_IS'))
                mhigh=float(form.getvalue('mhigh_DNS_IS'))
                sigx=float(form.getvalue('sigx_DNS_IS')) 
                new_theta=[Rn,tau,mmean,mscale,mlow,mhigh,sigx]
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
        #grb model para#################################################
        model_para=None
        config['grb_model'] = form.getvalue('grb_model')
        if config['grb_model']:
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

###########################################################################
        return [config, new_theta, model_para]



    def new_df():
         
        with open('response_tes.json','r') as f:
            res=json.load(f)

        response=res.copy()

        # events = pd.read_json(json.dumps(response['events']))
        # eventall = pd.read_json(json.dumps(response['eventall']))

        with open('events_new2.json', 'r') as f:
            json_str = json.load(f)
        events = pd.read_json(json_str)

        events.loc[events['detected'] == False, ['T90', 'F_max', 't_max', 'Epeak','fluence']] = 'NaN'
        #events = events.iloc[:, :-6]

             
        #有detected 的数据，服务器跑的
        with open('eventall_with_detected2.json', 'r') as f:
                json_str = json.load(f)
        eventall = pd.read_json(json_str)
        eventall=eventall[eventall['detected']==True]
        eventall=eventall.iloc[:,[0,1,6,-5,-4,-3,-2,-1]]       

        # size=100000
        # # response['total']=[331.788731,len(events[events['detected']==True])]
        # response['total']=[331.788731,1]
        # response['tot_all']=[398655.322825,len(eventall)*398655.322825/size]
        # events = pd.read_json('1.json')
        # eventall = pd.read_json('2.json')
       
        # response['sensitivity']=sensitivity
        response['events'] = json.loads(events.to_json(orient='records'))
        response['eventall'] = json.loads(eventall.to_json(orient='records'))


        size=100000
        # response['total']=[331.788731,1]
        response['total_true']=len(events[events['detected']==True])
        # response['total_true']=1
        response['tot_all']=len(eventall)*398655.322825/size


        return response

    # def old_df():
         
    #     with open('response_off.json','r') as f:
    #         res=json.load(f)

    #     response=res.copy()

    #     # events = pd.read_json(json.dumps(response['events']))
    #     with open('events_off.json', 'r') as f:
    #         json_str = json.load(f)
    #     events = pd.read_json(json_str)
        
    #     # with open('sensitivity.json', 'r') as f:
    #     #     sensitivity = json.load(f)

    #     # response['sensitivity']=sensitivity
    #     response['events'] = json.loads(events.to_json(orient='records'))
    #     return response


    config,new_theta,model_para = get_parameters()
    
    # from gwtoolbox.HE_models import *
    
    # if model_para==None:
    #     model_para=[half_open_mean,half_open_std, lg_r_grb_mean, lg_r_grb_std,lgEgrb_mean, lgEgrb_std,nup0_mean, nup0_std, jet_Gamma_mean, jet_Gamma_std]

    response = new_df()
    # response = old_df()

    config['cosmology'] = config['cosmology'].name # To make it serializeable
    response['config'] = config

    # response['new_theta']=new_theta
    # response['model_para']=model_para
    # res=response.copy()
    # with open('response.json','w') as f:
    #         json.dump(res,f)

    format_response(response)
    # error_response('did it runed?')

