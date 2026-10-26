#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

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

import recaptcha
import time
tick=time.time()
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
import astropy.units as u
import numpy as np
import json
import cgi
gwtoolbox_path = os.getenv("PATH_GWTOOLBOX", sys.executable)
sys.path.insert(0, gwtoolbox_path)
from astropy.constants import c
from gwtoolbox.tools_pta import PTA_individual, set_cosmology, PTA_SGWB
from gwtoolbox import parameters
from gwtoolbox import plotshtml as gwplots

from gwtoolbox.functions_pta import strain_amplitude 
def html_start():
    print ('Content-type:text/html\r\n\r\n')
    print ('<html>')
    print ('<head>')
def html_start_txt():
    print ('Content-type: text/ascii \r\n\r\n')

def format_response(response):
        """ Prints the content-type header and formts the data as json"""
        #print('Content-type:text/json\r\n\r\n')
        json.dump(response, sys.stdout)
        quit()

def html_end():
    print ('<br>')
    print ('</body>')
    print ('</html>')

form = cgi.FieldStorage()

tock=time.time()
time_initialize=tock-tick
def plot_PTA(PulsarArray):
    lenPTA=len(PulsarArray)
    print("Number of Pulsars:", lenPTA)
    colors=[]
    ntoas=[]
    for i in range(lenPTA):
        if PulsarArray[i]['PTA']=='NEW':
            colors.append('C1')
        #print("PSR name: %s" % PulsarArray[i]['name'])
        else:
            colors.append('C0')
        ntoa=PulsarArray[i]['Tyear']*365/1.
        ntoas.append(ntoa)
    from io import BytesIO
    import urllib.parse, base64
    imgdata = BytesIO()
    RAs_hms=np.array([PulsarArray[i]["RA"] for i in range(len(PulsarArray))])
    DECs_dms=np.array([PulsarArray[i]["DEC"] for i in range(len(PulsarArray))])
    eq=SkyCoord(RAs_hms, DECs_dms, unit=(u.hourangle, u.deg))
    gal = eq.galactic
    plt.figure(figsize=(6,5))
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="aitoff")
    ax.grid('True')
    xtics_radian=ax.get_xticks()
    xtics_str=['150$^\circ$','120$^\circ$','90$^\circ$','60$^\circ$','30$^\circ$','0$^\circ$','330$^\circ$','300$^\circ$','270$^\circ$','240$^\circ$','210$^\circ$']
#ax.set_xlim(360., 0.)
#ax.set_xticks([])
#ax.set_xticks(xtics_radian, xtics_str)
    ax.set_xticklabels(xtics_str, fontsize=14)
    #ax.set_yticklabels(ax.get_yticks(), fontsize=10)
    ax.scatter(-gal.l.wrap_at('180d').radian, gal.b.radian, linestyle='None', color=colors, s=0.01*np.array(ntoas))
    ax.scatter([],[], color='C0',label='known pulsars')
    ax.scatter([],[], color='C1',label='new pulsars')
#ax.scatter(gal.l, gal.b, linestyle='None')
    ax.legend(loc='lower center', fontsize=14, ncol=2, bbox_to_anchor=(0.5, -0.2))
    fig.savefig(imgdata, format='png',dpi=150,bbox_inches='tight', transparent=True)
    imgdata.seek(0)  # rewind the data
    image_base64 = base64.b64encode(imgdata.getvalue()).decode('utf-8').replace('\n', '')
    uri = 'data:image/png;base64,' + urllib.parse.quote(image_base64)
    imgdata.close()
    plt.close(fig)
    print ('<img src = "'+uri+'" width="500">')
    print ('<br>')
    return None

if not recaptcha.verify(form.getvalue('recaptcha')):
    html_start()
    print("You're requests are deemed too robot-like. Aborting.")
    html_end()
    quit()
#_cosmology = form.getvalue('cosmo_model') # string
_plan=float(form.getvalue('plan')) # int -1 exsting, 0 plan 
if _plan ==-1:
    _PTA= form.getvalue('PTA') # string
elif _plan ==0:
    _PTA= form.getvalue('PTA_future') # string
_T = int(float(form.getvalue('T'))) # float, read in days, convert to minutes
_dt  = int(float(form.getvalue('dt'))) #
_Ndot = int(float(form.getvalue('Ndot'))) # string
_IDsource = int(form.getvalue('IDsource')) # -1: indiviudal BH; 0: SGWB; 1: Indi_sens
_lambda = form.getvalue('lambda') # string, in [hh:mm:ss] Ecliptic Longitude of indi source
_beta = form.getvalue('beta') # string, in[dd:mm:ss] Ecliptic Latitude of indi source
_fs = float(form.getvalue('fs')) # float, frequency of the individual GW
flag_inputs=form.getvalue('flag_inputs') # Should be a string!!!
#print(_flag_inputs)
if flag_inputs=="masses":    
    m1 = float(form.getvalue('m1'))
    m2 = float(form.getvalue('m2'))
    D = float(form.getvalue('Dl'))
    _A = strain_amplitude(m1,m2,D,_fs*3.171e-8) 
elif flag_inputs=="hs":
#else:
    _A = float(form.getvalue('A')) # float, amplitude of indivudal GW
_typeSGWB= form.getvalue('typeSGWB') # -1: SMBHB, 0: Cosmic String, 1: Relic GW
_SNRcri= float(form.getvalue('SNRcri')) # 0 1
_rhostar=float(form.getvalue('rhostar'))
_Cosmology_model=form.getvalue('cosmology')
_gamma=float(form.getvalue('gamma'))

if _plan==-1:
    obs_plan='A'
elif _Ndot==0:
    obs_plan='B'
elif _Ndot>0:
    obs_plan='C' 

if _typeSGWB=='-1':
    types='SBHBH'
    typename='Supermassive BH binaries overlapping'
elif _typeSGWB=='0':
    types='CS'
    typename='Cosmic strings'
elif _typeSGWB=='-1':
    types='primordial'
    typename='Relic GW'
elif _typeSGWB=='2':
    types='selfdefine'
    typename='self defined power law spectrum'

if _Cosmology_model in ['WMAP5','WMAP7','WMAP9','Planck13','Planck15']:
    cosmos=set_cosmology(_Cosmology_model)
elif _Cosmology_model=='FlatLambdaCDM':
    H0=float(form.getvalue('H0'))
    Om0=float(form.getvalue('omega'))
    Tcmb=float(form.getvalue('Tcmb'))
    cosmos=set_cosmology(cosmoID=_Cosmology_model,H0=H0,Om0=Om0,Tcmb=Tcmb)
#cosmos=set_cosmology(_Cosmology_model)
def listToString(s): 
    
    # initialize an empty string
    str1 = "" 
    
    # traverse in the string  
    for ele in s: 
        str1 += str(ele)
        str1 += ','  
    
    # return string  
    return str1[:-1]
    
if _IDsource==-1:
    #print(obs_plan, _dt, _T, _Ndot, _PTA[0])
    #BHBIndi=PTA_individual(obs_plan="C", delta_t=1, T=10, Ndot=2,which_PTA='IPTA')
    BHBIndi=PTA_individual(obs_plan=obs_plan, delta_t=_dt, T=_T, Ndot=_Ndot, which_PTA=_PTA)
    rho=BHBIndi.SNR(ra=_lambda, dec=_beta, hs=_A, frequency=_fs, phi=0, iota=0)
    html_start()
    #print(flag_inputs+'<br>')
    print("The skype map of the Pulsar Timing Array"+'<br>')
    PulsarArray=BHBIndi.PTA
    plot_PTA(PulsarArray)
    print("The parameters of the individual GW source are:"+'<br>')
    print("RA [h:m:s]",_lambda, "; DEC [d:m:s]",_beta+'<br>')
    print("frequency: %.2f yr<sup>-1</sup>; amplitude %.1e" % (_fs,_A))
    print('<br>')
    print("------------"+'<br>')
    print("SNR of the source is: <b>%.3f</b>" % rho)
    print('<br>') 
    html_end()
elif _IDsource==0:
    if not types=='selfdefine':
    	SGWB=PTA_SGWB(cosmos=cosmos, obs_plan=obs_plan, delta_t=_dt, T=_T, Ndot=_Ndot, which_PTA=_PTA, which_SGWB=types)
    else:
        SGWB=PTA_SGWB(cosmos=cosmos, obs_plan=obs_plan, delta_t=_dt, T=_T, Ndot=_Ndot, which_PTA=_PTA, which_SGWB=types, index=-_gamma)
    html_start()
    print("The skype map of the Pulsar Timing Array"+'<br>')
    PulsarArray=SGWB.PTA
    plot_PTA(PulsarArray)
    Upper_A=SGWB.Upper_A(rho_cri=_SNRcri)
    Omegah2=SGWB.UpperLimit(rho_cri=_SNRcri)
    print("The characteristic strain of Stochastic GW backgound from <b>%s</b> can be constrained down to:<p>%e</p>" % (typename,Upper_A))
    print('<br>')
    print("or equivalently, the &Omega;*h<sup>2</sup> (Cosmology independent dimensionless energy density) can be constrained down to: <p>%e</p>" % Omegah2)
    html_end()
elif _IDsource==1: # sens_curve
    BHBIndi=PTA_individual(obs_plan=obs_plan, delta_t=_dt, T=_T, Ndot=_Ndot, which_PTA=_PTA)
    html_start()


    print("The skype map of the Pulsar Timing Array"+'<br>')
    PulsarArray=BHBIndi.PTA
    plot_PTA(PulsarArray)
    #print("I'm doing this!")
    sens, freqs = BHBIndi.sens_curve_skyave(_rhostar)
    print("Sensivity curve averaged over the source coordinates over the celestial sphere:"+'<br>')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid('True')
    ax.set_ylabel('$h_s$')
    ax.set_xlabel('Frequency (Hz)')
    ax.set_yscale("log")
    ax.set_xscale("log")
    # ax.set_ylim([0.5*min(sens),1e-12])
    ax.plot(freqs, sens)
    from io import BytesIO
    import urllib.parse, base64
    imgdata = BytesIO()
    fig.savefig(imgdata, format='png',dpi=150,bbox_inches='tight', transparent=True)
    imgdata.seek(0)  # rewind the data
    image_base64 = base64.b64encode(imgdata.getvalue()).decode('utf-8').replace('\n', '')
    uri = 'data:image/png;base64,' + urllib.parse.quote(image_base64)
    imgdata.close()
    plt.close(fig)
    print ('<img src = "'+uri+'" width="500">')
    #print(sens, freqs)

    print ('<br>')
    print('<div id="downloadtab">')
    print('<label style="display: inline; width: 20%;"> File Name: </label><input type="text" id="filename" style="display: inline; width: 20%;"><label style="display: inline; width: 20%;">.txt</label>')                
    print('<button onclick="savetable()">download Curve data</button>')
    print('</div>')
    # very ugly codes below :(
    #print('<label>testing here</label>')
    print('<input type="text" id="sens_freqs" style="display:none" value="['+listToString(freqs)+']" >')
    print('<input type="text" id="sens_sens" style="display:none" value="['+listToString(sens)+']" >')
    html_end()
    #response = {}
    #response['senscurve']=[sens, freqs]
    #response['hs']=sens
    #format_response(response)
    
    
