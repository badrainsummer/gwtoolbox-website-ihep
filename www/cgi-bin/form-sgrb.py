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
    from hetoolbox.sources import sGRB
    from hetoolbox.observation import *

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
            'z': None,
            'p': None,
            'deltar': None,
            'Gamma': None,
            'r0': None,
            'B0_prime': None,
            'gamma_m': None,
            'gamma_M': None,
            'N_rings': None,
            'telescope': None,
            'output_type': None,
            'E_min': None,
            'E_max': None,
            'T_min': None,
            'T_max': None,}
        
        get_and_check_value(config, 'z', 'Redshift', min=0)
        get_and_check_value(config, 'p', 'Power law index', min=0)
        get_and_check_value(config, 'deltar', 'Width', min=0)
        get_and_check_value(config, 'Gamma', 'Bulk Lorentz factor', min=0)
        get_and_check_value(config, 'r0', 'Dissipation radius', min=0)
        get_and_check_value(config, 'B0_prime', 'Magnetic field', min=0)
        get_and_check_value(config, 'gamma_m', 'Minimum Lorentz factor', min=0)
        get_and_check_value(config, 'gamma_M', 'Maximum Lorentz factor', min=0)
        get_and_check_value(config, 'N_rings', 'number of rings', min=0)
        config['telescope'] = form.getlist('telescope')
        if not config['telescope']:
            error_response('You should at least choose one telescope')
        config['output_type'] = form.getvalue('output_type')
        if config['output_type'] == 'light_curve':
            get_and_check_value(config, 'E_min', 'minimun of Energy range', min=1e3)
            get_and_check_value(config, 'E_max', 'maximum of Energy range', max=1e7)
            if config['E_min'] >= config['E_max']:
                error_response('minimun of Energy range must be less than maximum of Energy range')
        elif config['output_type'] == 'spectrum':
            get_and_check_value(config, 'T_min', 'minimun of Time range', min=0)
            get_and_check_value(config, 'T_max', 'maximum of Time range', max=1e2)
            if config['T_min'] >= config['T_max']:
                error_response('minimun of Time range must be less than maximum of Time range')

        try:
            config['N_rings'] = int(config['N_rings'])
        except ValueError:
            error_response('number of rings must be an integer')

        if config['gamma_m'] >= config['gamma_M']:
            error_response('Minimum Lorentz factor must be less than Maximum Lorentz factor')

        return config

    # get a conside job desciption from form inputs:
    config = get_parameters()

    source_GRB_A=sGRB(z=config['z'], p=config['p'], deltar=config['deltar'],
                      Gamma=config['Gamma'], r0=config['r0'], B0_prime=config['B0_prime'],
                      gamma_m=config['gamma_m'], gamma_M=config['gamma_M'], N_rings=config['N_rings'])
    FET_matrix, E_array, T_array = source_GRB_A.FET()

    response = {}
    response['success'] = True
    response['msg'] = "Success"
    response['config'] = config

    if config['output_type']=='light_curve':
        E_range = (config['E_min'], config['E_max'])  # convert keV to eV
        light_curve = FET_matrix[:,(E_array >= E_range[0]) & (E_array <= E_range[1])].sum(axis=1)
        response['lightcurve'] = {
            'T_array': T_array.tolist(),
            'lightcurve': light_curve.tolist()
        }
        response['telescope'] = {}
        for telescope in config['telescope']:
            response['telescope'][telescope] = {}
            energies, model_total_counts_t, time_array, bgk_counts= ObsSpectrum(source_GRB_A, telescope)
            energy_mask = (energies >= E_range[0]/1000) & (energies <= E_range[1]/1000)
            energies_filtered = energies[energy_mask]
            model_total_counts_t = model_total_counts_t[:, energy_mask]
            bgk_counts = bgk_counts[:, energy_mask]
            time_new, counts_new, new_bgk= time_rebin(time_array, model_total_counts_t, bgk_counts, 0.5)
            counts_new, new_bgk = np.nan_to_num(counts_new, nan=0.0), np.nan_to_num(new_bgk, nan=0.0)
            uncertainties_new = np.sqrt(counts_new.sum(axis=1)+new_bgk.sum(axis=1))
            response['telescope'][telescope]['time'] = time_new.tolist()
            response['telescope'][telescope]['counts'] = counts_new.sum(axis=1).tolist()
            response['telescope'][telescope]['uncertainties'] = uncertainties_new.tolist()
    elif config['output_type']=='spectrum':
        T_range = (config['T_min'], config['T_max'])  # in seconds
        t_mask = (T_array >= T_range[0]) & (T_array < T_range[1])
        spectrum = FET_matrix[t_mask, :].sum(axis=0)
        response['spectrum'] = {
            'E_array': E_array.tolist(),
            'spectrum': spectrum.tolist()
        }
        response['telescope'] = {}
        for telescope in config['telescope']:
            response['telescope'][telescope] = {}
            energies, model_total_counts_t, time_array, bgk_counts= ObsSpectrum(source_GRB_A, telescope)
            time_filtered = time_array[t_mask]
            model_total_counts_t = model_total_counts_t[t_mask, :]
            bgk_counts = bgk_counts[t_mask, :]
            time_new, counts_new, new_bgk= time_rebin(time_filtered, model_total_counts_t, bgk_counts, 0.5)
            counts_new, new_bgk = np.nan_to_num(counts_new, nan=0.0), np.nan_to_num(new_bgk, nan=0.0)
            uncertainties_new = np.sqrt(counts_new.sum(axis=0)+new_bgk.sum(axis=0))
            response['telescope'][telescope]['energies'] = (energies/1e3).tolist()
            response['telescope'][telescope]['spectrum'] = counts_new.sum(axis=0).tolist()
            response['telescope'][telescope]['uncertainties'] = uncertainties_new.tolist()

    # with open('/Users/ball/GWtoolbox_modify/response_sgrb.json','w') as f:
    #     json.dump(response,f)

    format_response(response)