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

    from astropy import units as u
    from hetoolbox.binary_common import Kepler_Orbit

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
            'mass_1': None,
            'mass_2': None,
            'a': None,
            'e': None,
            'iota': None,
            'Omega': None,
            'omega': None,}
        
        get_and_check_value(config, 'mass_1', 'Primary Mass', min=0)
        get_and_check_value(config, 'mass_2', 'Secondary Mass', min=0)
        get_and_check_value(config, 'a', 'Semi-major Axis', min=0)
        get_and_check_value(config, 'e', 'Eccentricity', min=0, max=1)
        get_and_check_value(config, 'iota', 'Inclination', min=0, max=180)
        get_and_check_value(config, 'Omega', 'Longitude of Ascending Node', min=0, max=360)
        get_and_check_value(config, 'omega', 'Argument of Periapsis', min=0, max=360)

        return config

    config = get_parameters()

    Orbit_A=Kepler_Orbit(m1=config['mass_1'], m2=config['mass_2'], a=config['a'], e=config['e'],
                         iota=config['iota']/180*np.pi, Omega=config['Omega']/180*np.pi, omega=config['omega']/180*np.pi)

    vel_p=[]
    vel_s=[]
    phase=np.linspace(0,6*np.pi,1800)
    for p in phase:
        velocity = Orbit_A.vlos_at_phase(phase=p)
        vel_p.append(velocity[0].value)
        vel_s.append(velocity[1].value)

    separation=[]
    time=phase*Orbit_A.P/(2*np.pi)
    for t in time:
        separation.append(Orbit_A.separation_at_t(t).value)

    response = {}
    response['success'] = True
    response['msg'] = "Success"
    response['config'] = config
    response['period'] = Orbit_A.P.to(u.d).value
    response['pdis'] = (Orbit_A.a*(1-Orbit_A.e)).to(u.AU).value
    response['adis'] = (Orbit_A.a*(1+Orbit_A.e)).to(u.AU).value
    response['sconj'] = (Orbit_A.conjunctions_t()[0]).to(u.d).value
    response['iconj'] = (Orbit_A.conjunctions_t()[1]).to(u.d).value
    response['Radial_Velocity'] = {
        'phase': phase.tolist(),
        'velocity_primary': vel_p,
        'velocity_secondary': vel_s
    }
    response['Separation'] = {
        'time': time.value.tolist(),
        'separation': separation
    }
    
    # with open('/Users/ball/GWtoolbox_modify/response_binary.json','w') as f:
    #     json.dump(response,f)

    format_response(response)