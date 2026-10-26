Examples
========

Basic Usage
-----------

If you want to explore detector parameter space and plot sensitivity function for a new design, you would do
something like:

.. code-block:: python

    from gwtoolbox.tools_earth import Tools, set_cosmology
    from gwtoolbox.detectors_earth import LigoLike
    from numpy import sqrt
    from gwtoolbox.plots import plot_noise_withdefault

    # set default cosmology
    cosmos = set_cosmology()

    # initialize new detector
    new_det = LigoLike(-1)
    # define new parameters [arm length, laser power]
    det_new_param = [8995.,125.]
    # get noise function
    x,y = new_det.noise_curve(pars=det_new_param)
    # initialize default LIGO detector
    det_def = LigoLike(1)
    # get noise function
    x0,y0 = det_def.noise_curve()
    # plot
    plot_noise_withdefault(x,sqrt(y),x0,sqrt(y0))
    

To obtain the total number of detected sources and a list of parameters with errors for a sample of 10 systems:

.. code-block:: python

    # initialize Tools for detID=0 (Virgo) and popID=0 (BHB)
    t = Tools(detID=0,popID=0,cosmos=cosmos)
    # print total number of detected sources
    print (t.total_number())
    # print parameters for 10 systems
    print (t.list_params())
    # print errors
    print (t.list_param_errors()) 
    # print parameters for 20 systems
    print (t.list_params(size=20))

You can change observing time and/or signal to noise ratio (default values 10000 sec and 8):

.. code-block:: python

    # change observing time and snr 
    print (t.total_number(time_obs=5000,rho_cri=5))

You can change detector ID and population ID:

.. code-block:: python

    # initialize Tools for detID=0 (Virgo) and popID=1 (DNS)
    t = Tools(detID=0,popID=1,cosmos=cosmos)
    # print total number of detected sources
    print (t.total_number())
    #
    # initialize Tools for detID=0 (Virgo) and popID=2 (BHNS)
    t = Tools(detID=0,popID=2,cosmos=cosmos)
    # print total number of detected sources
    print (t.total_number())
    

You can change the cosmological model:

.. code-block:: python

    # set new cosmology model
    cosmos_w5 = set_cosmology(cosmoID='WMAP5')
    # initialize Tools for detID=0 (Virgo) and popID=0 (BHB)
    t = Tools(detID=0,popID=0,cosmos=cosmos_w5)
    # print total number of detected sources
    print (t.total_number())
    

You can change the parameters in cosmic merger rate:

.. code-block:: python

    # change parameters in cosmic merger rate
    new_theta = [2.5,0.1,12.8,1.0,15.,-0.1,5,-0.1,5,0.8]
    t.population_class.set_model_theta(new_theta)
    # print total number of detected sources
    print (t.total_number())
    # reset model
    t.population_class.set_model_theta()
    # print total number of detected sources
    print (t.total_number())


Default setup
-------------

.. code-block:: python

    # observing time
    TIME_OBS_EARTH = 10000.
    # SNR
    RHO_CRIT_EARTH = 8.
    # cosmic merger rates 
    thetaBHB = [1.5,0.1,12.8,1.0,15.,-0.1,5,-0.1,5,0.8]
    thetaDNS = [1.7,0.1,12.8,1.0,1.4,0.5,1.1,2.0]
    thetaBHNS = [1.,0.1,12.8,1.0,1.4,0.5,1.1,2.0,7,0,2,0,3,0]
    # cosmology Flat Lambda CDM
    H0_1 = 70. # km/s/Mpc
    Om0_1 = 0.3
    
    
    
