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
    from hetoolbox.tools_XRB import typical_BH

    form = cgi.FieldStorage()
    bh_type = form.getvalue("type")
    if bh_type not in ['HSS','HS']:
        error_response('Invalid type for typical Black Hole system')
    source_BH = typical_BH(state=bh_type)
    response = {
        'msg': 'Typical Black Hole system generated successfully',
        'success': True,
        'mass': source_BH.mBH,
        'distance': source_BH.distance,
        'mdot': source_BH.mdot/1.4e19,
        'theta': source_BH.theta,
        'rin': source_BH.rin,
        'Te': source_BH.Te,
        'cov_frac': source_BH.cov_frac,
        'H': source_BH.H,
        'Gamma': source_BH.Gamma,
        'Fe': source_BH.Fe,
        'KE': source_BH.KE,
    }

    format_response(response)
