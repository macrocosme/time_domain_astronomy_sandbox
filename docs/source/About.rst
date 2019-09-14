About
======

This package consists of a series of classes to simulate time-domain astronomy data products.

Classes includes:
    - ``Backend``: properties describing an observatory backend,
    - ``Pulse``: a broadband dispersed pulse,
    - ``Observation``: an observation data product generated for a given ``Backend``,
    - ``RFIm``: radio frequency interference mitigation functions,
    - ``Plotting``: plotting functions.

Copyright (c) Dany Vohl. 2019.

Getting the code
----------------

.. code-block:: shell

    git clone https://github.com/macrocosme/time_domain_astronomy_sandbox.git
    cd amber_meta/

Usage
-----

1. Load classes:  

.. code-block:: python

    from time_domain_astronomy_sandbox.backend import Backend
	from time_domain_astronomy_sandbox.observation import Observation
	from time_domain_astronomy_sandbox.pulse import Pulse
	from time_domain_astronomy_sandbox.plotting import plot_multi_images, plot_multi_1D
	from time_domain_astronomy_sandbox.rfim import RFIm
	

2. Plot a dispersed pulse interactively (using `ipywidgets`)

.. code-block:: python

	def interactive_pulse_arts():
	    """Plot interactive dispersed pulse using ASTRON's ARTS backend."""
	    pulse = Pulse(Backend())
	    pulse.plot_delay_v_frequency_interactive(xscale='linear')

	interactive_pulse_arts()
	
.. code-block:: python

	def interactive_pulse_arts():
    	"""Plot interactive dispersed pulse using ASTRON's ARTS backend."""
    	pulse = Pulse(Backend())
    	pulse.plot_delay_v_frequency_interactive(xscale='linear')

		interactive_pulse_arts()

.. code-block:: python 

	def test_one_pulse_dedisperse():
	    """Plot one dispersed pulse, and it's dedispersed self."""
	    obs = Observation(Backend(), length=1.5*1.024)
	    noise_window = obs.window.copy()
	    obs.add_dispersed_pulse(dm=1000, width=0.006, pulse_t0=0.16, snr=20, verbose=True)
	    xstep = 1000
	    ystep = 500

	    rc('font', size=12)
	    rc('axes', titlesize=12)
	    rc('axes', labelsize=12)

	    plot_multi_images(
	        (
	            noise_window,
	            obs.window,
	            obs.dedisperse(dm=1000),
	        ),

	        noise_median=obs.noise_median,
	        noise_std=obs.noise_std,

	        direction='vertical',

	        xticks=obs.time_indices[::xstep],
	        xtick_labels=["%.2f" % t for t in obs.times[::xstep]],

	        yticks=obs.backend.freq_indices[::ystep],
	        ytick_labels=["%.0f" % f for f in obs.backend.frequencies[::ystep]],

	        xfig_size = 15,
	        yfig_size = 5,
	    )

	test_one_pulse_dedisperse()


License
-------

   This project is licensed under the terms of the GNU GPL v3+ license.
