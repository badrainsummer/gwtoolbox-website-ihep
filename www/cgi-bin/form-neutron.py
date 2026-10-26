#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import subprocess

class DevNull:
    def write(self, _): pass
    def flush(self): pass
sys.stdout = DevNull()

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
python_exec = os.getenv("PY_EXEC_HE", sys.executable)
conda_dir = os.getenv("CONDA_PATH", "")
home_dir = os.getenv("HOME_PATH", "")
terminal = os.getenv("TERMINAL", "")

if os.path.realpath(sys.executable) != os.path.realpath(python_exec) or os.environ.get("CONDA_DEFAULT_ENV") != "hetoolbox":
    cmd = f'''
    source {conda_dir}/etc/profile.d/conda.sh > /dev/null 2>&1
    conda activate hetoolbox > /dev/null 2>&1
    exec {python_exec} {" ".join(sys.argv)}
    '''
    os.execve(terminal, [terminal, "-c", cmd], os.environ)
os.environ["HOME"] = home_dir

import cgi
from pprint import pprint
import numpy as np
import json
import math

if __name__=='__main__':
    def format_response(response):
        """ Prints the content-type header and formts the data as json"""
        sys.__stdout__.write('Content-type: text/json\r\n\r\n')
        json.dump(response, sys.__stdout__)
        sys.exit()
    def error_response(msg):
        format_response({'msg': msg, 'success': False})

    # the path to the main codes
    hetoolbox_path = os.getenv("PATH_HETOOLBOX", sys.executable)
    sys.path.insert(0, hetoolbox_path)

    import xspec
    xspec.Xset.chatter = 0
    xspec.Xset.show = 0
    from hetoolbox.sources import NeutronStar
    import hetoolbox.tools_XRB as tools_XRB
    from hetoolbox.observation import *
    from hetoolbox.telescopes import *

    # Get the fields from the form 
    form = cgi.FieldStorage()

    def get_and_check_value(config, field_name, display_name, max=None, min=None):
        try:
            value = form.getvalue(field_name)
            if value is None:
                error_response(f'{display_name} is required')
            value = float(value)
            config[field_name] = value
        except Exception:
            error_response(f'{display_name} has an invalid value')
        
        if max is not None and config[field_name] > max:
            error_response(f'{display_name} must be less than {max}')
        if min is not None and config[field_name] < min:
            error_response(f'{display_name} must be greater than {min}')

    def get_parameters():
        """ Gets the requires fields from the html form, sanitizes input and checks that it's all there and in range"""

        # create a named tuple to contain everything needed
        config = {
            'mass': None,
            'distance': None,
            'radius': None,
            'Bsurf': None,
            'P': None,
            'mdot': None,
            'type': None,
            'disc': None,
            'disc_theta': None,
            'disc_Te': None,
            'disc_cov_frac': None,
            'disc_H': None,
            'disc_Gamma': None,
            'disc_Fe': None,
            'disc_KE': None,
            'surface': None,
            'surface_r': None,
            'surface_Tbb': None,
            'surface_Te': None,
            'surface_cov_frac': None,
            'surface_Gamma': None,
            'surface_tau': None,
            'surface_theta': None,
            'surface_iota': None,
            'angles': None,
            'telescope': None,}
        
        get_and_check_value(config, 'mass', 'Mass', min=0)
        get_and_check_value(config, 'distance', 'Distance', min=0)
        get_and_check_value(config, 'radius', 'Radius', min=0)
        get_and_check_value(config, 'Bsurf', 'Surface Magnetic Field', min=0)
        get_and_check_value(config, 'P', 'Period', min=0)
        get_and_check_value(config, 'mdot', 'Accretion Rate', min=0)
        config['type'] = form.getvalue('type')

        NS=NeutronStar(m=config['mass'], d=config['distance'], r=config['radius'], Bsurf=config['Bsurf'], P=config['P'])
        AccFlow=NS.Accretion_Flow(mdot=config['mdot'], theNS=NS)
        NS.accretion_flow=AccFlow
        if config['type'] != AccFlow.classification:
            error_response(f'Source type has been changed, please check the type and fill the right parameters')

        if config['type'] in ["LMXB", "AF-AMSP", "AF-AXP-pencil", "AF-AXP-mix", "AF-AXP-fan"]:
            config['telescope'] = form.getlist('telescope')
            if not config['telescope']:
                error_response(f'Must choose a telescope')
            config['disc'] = form.getvalue('disc') == 'on'
            if config['type'] in ["LMXB", "AF-AMSP"]:
                if config['disc']:
                    get_and_check_value(config, 'disc_theta', 'Inclination Angle', min=0, max=180)
                    get_and_check_value(config, 'disc_Te', 'Electron Temperature', min=0)
                    get_and_check_value(config, 'disc_cov_frac', 'Covering Fraction', min=0, max=1)
                    get_and_check_value(config, 'disc_H', 'Corona Height', min=0)
                    get_and_check_value(config, 'disc_Gamma', 'Photon Index', min=0)
                    get_and_check_value(config, 'disc_Fe', 'Iron Abundance', min=0)
                    get_and_check_value(config, 'disc_KE', 'High-Energy Cutoff', min=0)
                config['surface'] = form.getvalue('surface') == 'on'
                if config['surface']:
                    get_and_check_value(config, 'surface_r', 'Intrinsic Hotspot Radius', min=0)
                    get_and_check_value(config, 'surface_Tbb', 'Temperature', min=0)
                    get_and_check_value(config, 'surface_Te', 'Electron Temperature', min=0)
                    get_and_check_value(config, 'surface_cov_frac', 'Covering Fraction', min=0, max=1)
                    try:
                        value = form.getvalue('surface_Gamma')
                        config['surface_Gamma'] = value
                    except Exception:
                        error_response(f'Photon Index has an invalid value')
                    try:
                        value = form.getvalue('surface_tau')
                        config['surface_tau'] = value
                    except Exception:
                        error_response(f'Electron Optical Depth has an invalid value')
                    if config['surface_Gamma']==None and config['surface_tau']==None:
                        error_response("you should set the Gamma (photon index) or Tau (electron optical depth).")
                    if config['surface_Gamma']!=None and config['surface_tau']!=None:
                        error_response("you can't set Gamma and Tau at the same time.")
                    if config['surface_Gamma']:
                        config['surface_Gamma'] = float(config['surface_Gamma'])
                    if config['surface_tau']:
                        config['surface_tau'] = float(config['surface_tau'])
                if not (config['disc'] or config['surface']):
                    error_response(f'Must add dist or suface')
                if config['type'] == "AF-AMSP":
                    get_and_check_value(config, 'surface_theta', 'Colatitude', min=0, max=180)
                    get_and_check_value(config, 'surface_iota', 'Observer inclination', min=0, max=180)
                    config['angles'] = [config['surface_theta'], config['surface_iota']]
                if config['disc']:
                    AccFlow.creat_disk(theta=config['disc_theta'], Te=config['disc_Te'], cov_frac=config['disc_cov_frac'],
                                        H=config['disc_H'], Gamma=config['disc_Gamma'], Fe=config['disc_Fe'], KE=config['disc_KE'])
                NS.accretion_flow=AccFlow
                if config['surface']:
                    SF=NS.Surface(r=config['surface_r'], Tbb=config['surface_Tbb'], Te=config['surface_Te'],
                                    cov_frac=config['surface_cov_frac'], Gamma=config['surface_Gamma'], tau=config['surface_tau'], angles=config['angles'])
                    NS.surface=SF

        return config, NS

    # get a conside job desciption from form inputs:
    config, NS = get_parameters()

    response = {}
    response['success'] = True
    response['msg'] = "Success"
    response['config'] = config
    
    Texpo=10000
    response['OSpectrum'] = {}
    if config['type'] == "AF-AMSP":
        phases = np.linspace(0,1,10)
        energies, total_flux = [], []
        for phi in phases:
            en, tf, com=NS.spectrum(phi=phi*2*np.pi)
            if phi == 0:
                components = {key: [] for key in com}
            energies.append(en.tolist())
            total_flux.append(tf.tolist())
            for key in components:
                components[key].append(com[key].tolist())
        response['TSpectrum'] = {"total": {
            'Energy': energies,
            'Flux': total_flux}}
        for key in components:
            response['TSpectrum'][key] = {
                'Energy': energies,
                'Flux': components[key]
            }
        Texpo=10000
        response['OSpectrum'] = {}
        for telescope in config['telescope']:
            energies, model_total_counts, model_components_counts, phases, bgk_counts, uncertainties = ObsSpectrum(NS, telescope, T=Texpo)
            model_total_counts = np.array(model_total_counts)
            response['OSpectrum'][telescope] = {
                'Energy': energies.tolist(),
                'Counts': model_total_counts.tolist(),
                'uncertainties': [[x if not math.isnan(x) else 0 for x in row] for row in uncertainties]
                }
                
    elif config['type'] in ["LMXB", "AF-AXP-pencil", "AF-AXP-mix", "AF-AXP-fan"]:
        energies, total_flux, components=NS.spectrum()
        response['TSpectrum'] = {"total": {
            'Energy': energies.tolist(),
            'Flux': total_flux.tolist()}}
        for key in components:
            response['TSpectrum'][key] = {
                'Energy': energies.tolist(),
                'Flux': components[key].tolist()
            }
        Texpo=10000
        response['OSpectrum'] = {}
        for telescope in config['telescope']:
            energies, model_total_counts, _, _, uncertainties = ObsSpectrum(NS, telescope, T=Texpo)
            response['OSpectrum'][telescope] = {
                'Energy': energies.tolist(),
                'Counts': model_total_counts.tolist(),
                'uncertainties': [x if not math.isnan(x) else 0 for x in uncertainties]
                }
            
    # with open('/Users/ball/GWtoolbox_modify/response_neutron.json','w') as f:
    #     json.dump(response,f)

    format_response(response)