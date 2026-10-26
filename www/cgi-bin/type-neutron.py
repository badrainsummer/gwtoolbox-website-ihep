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

    config = {}
    config['type_kind'] = form.getvalue('type_kind')
    if config['type_kind'] == 'LMXB':
        config['type_state'] = form.getvalue('type_state')
    elif config['type_kind'] == 'AF-AXP':
        config['type_AF_AXP'] = form.getvalue('type_AF-AXP')

    if config['type_kind'] == 'LMXB':
        type_NS = tools_XRB.typical_NS(kind='LMXB',state=config['type_state'])
    elif config['type_kind'] == 'AF-AMXP':
        type_NS = tools_XRB.typical_NS(kind='AF-AMSP')
    elif config['type_kind'] == 'AF-AXP':
        type_NS = tools_XRB.typical_NS(kind=config['type_AF_AXP'])
    type_NS.spectrum()

    response = {}
    response['success'] = True
    response['msg'] = "Success"
    response['config'] = config
    response['mass'] = type_NS.mass
    response['distance'] = type_NS.distance
    response['B'] = type_NS.B
    response['period'] = type_NS.period
    response['mdot'] = type_NS.mdot
    if config['type_kind'] in ['LMXB', 'AF-AMXP']:
        response['disc_theta'] = type_NS.AccFlow.parent.naked_disk.theta
        response['disc_Te'] = type_NS.AccFlow.parent.coranated_disk.Te
        response['disc_cov_frac'] = type_NS.AccFlow.parent.coranated_disk.cov_frac
        response['disc_H'] = type_NS.AccFlow.parent.H
        response['disc_Gamma'] = type_NS.AccFlow.parent.coranated_disk.Gamma
        response['disc_Fe'] = type_NS.AccFlow.parent.Fe
        response['disc_KE'] = type_NS.AccFlow.parent.KE
        response['surface_r'] = type_NS.SF.rhs
        response['surface_Tbb'] = type_NS.SF.temp
        response['surface_Te'] = type_NS.SF.Te
        response['surface_cov_frac'] = type_NS.SF.cov_frac
        response['surface_Gamma'] = type_NS.SF.Gamma
        response['surface_tau'] = type_NS.SF.tau
        if config['type_kind'] == 'AF-AMXP':
            response['surface_theta'] = type_NS.SF.theta
            response['surface_iota'] = type_NS.SF.iota

    # with open('/Users/ball/GWtoolbox_modify/response_type_neutron.json','w') as f:
    #     json.dump(response,f)

    format_response(response)