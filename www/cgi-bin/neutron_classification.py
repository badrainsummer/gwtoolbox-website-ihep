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

    from hetoolbox.sources import NeutronStar

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
            'mdot': None,}
        
        get_and_check_value(config, 'mass', 'Mass', min=0)
        get_and_check_value(config, 'distance', 'Distance', min=0)
        get_and_check_value(config, 'radius', 'Radius', min=0)
        get_and_check_value(config, 'Bsurf', 'Surface Magnetic Field', min=0)
        get_and_check_value(config, 'P', 'Period', min=0)
        get_and_check_value(config, 'mdot', 'Accretion Rate', min=0)

        return config

    # get a conside job desciption from form inputs:
    config = get_parameters()

    NS=NeutronStar(m=config['mass'], d=config['distance'], r=config['radius'], Bsurf=config['Bsurf'], P=config['P'])
    AccFlow=NS.Accretion_Flow(mdot=config['mdot'], theNS=NS)

    response = {}
    response['success'] = True
    response['msg'] = "Success"
    response['config'] = config
    response['class'] = AccFlow.classification

    format_response(response)