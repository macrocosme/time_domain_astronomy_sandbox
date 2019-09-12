"""Test functions."""
from time_domain_astronomy_sandbox.backend import Backend
from time_domain_astronomy_sandbox.observation import Observation
from time_domain_astronomy_sandbox.pulse import Pulse
from time_domain_astronomy_sandbox.plotting import plot_multi_images
from matplotlib import rc


def interactive_pulse_arts():
    """Plot interactive dispersed pulse using ASTRON's ARTS backend."""
    pulse = Pulse(Backend())
    pulse.plot_delay_v_frequency_interactive(xscale='linear')


def interactive_pulse_arts_to_lofar_hba():
    """Plot interactive dispersed pulse using bands from ARTS to Lofar HBA."""
    fmin = 120
    n_channels = 3000
    channel_bandwidth = (Backend().fmax-fmin)/n_channels

    pulse = Pulse(
        Backend(
            fmin=fmin,
            n_channels=n_channels,
            channel_bandwidth=channel_bandwidth
            )
        )
    pulse.plot_delay_v_frequency_interactive(xscale='linear', dm_init=3000)


def test_one_pulse_dedisperse():
    """Plot one dispersed pulse, and it's dedispersed self."""
    obs = Observation(Backend(), length=1.024)
    obs.add_dispersed_pulse(dm=1000, width=0.006, pulse_t0=0.16, snr=400)
    xstep = 1000
    ystep = 500

    rc('font', size=12)
    rc('axes', titlesize=12)
    rc('axes', labelsize=12)

    plot_multi_images(
        (
            obs.window,
            obs.dedisperse(dm=1000),
        ),
        direction='vertical',

        xticks=obs.time_indices[::xstep],
        xtick_labels=["%.2f" % t for t in obs.times[::xstep]],

        yticks=obs.backend.freq_indices[::ystep],
        ytick_labels=["%.0f" % f for f in obs.backend.frequencies[::ystep]],

        xfig_size = 30,
        yfig_size = 10,
        spectrum=False
    )

def pulse_and_rfi__cleaned():
    """Plot multiple panels: noise, wide and narrow band pulses + RFIm."""
    obs = Observation(Backend(), length=1.024/1.5)
    raw = obs.window.copy()
    obs.add_dispersed_pulse(dm=500, width=0.006, pulse_t0=0.04, snr=15)
    frb = obs.window.copy()
    obs.add_dispersed_pulse(dm=1, width=0.006, pulse_t0=0.23, snr=125)
    obs.add_dispersed_pulse(dm=10, width=0.001, pulse_t0=0.33, snr=125)

    for t_start, t_step, t_width, f1, f2 in [
        [0., 0.01, 0.003, 350, 360],
        [0.1, 0.008, 0.005, 700, 715],
    #     [0.2, 0.007, 0.004, 1220, 1255]
    ]:
        obs.add_rfi(
            t_start=t_start,
            t_stop=t_start+0.3,
            t_step=t_step,
            t_width=t_width,

            f_start=f1,
            f_stop=f2,

            snr=125,
        )

    xstep = 1100
    ystep = 500

    rc('font', size=16)
    rc('axes', labelsize=18)

    o_window = obs.window.copy()

    plot_multi_images(
        (
            raw,
            frb,
            o_window,
        ),

        labels=(
            'Noise (gaussian)',
            'Noise + Faint FRB',
            'Noise + Faint FRB + Strong RFI',
        ),

        direction='vertical',

        xticks=obs.time_indices[::xstep],
        xtick_labels=["%.2f" % t for t in obs.times[::xstep]],

        yticks=obs.backend.freq_indices[::ystep],
        ytick_labels=["%.0f" % f for f in obs.backend.frequencies[::ystep]],

        xfig_size=12,
        yfig_size=7.3,
        spectrum=False,
        colorbar=False,
        savefig=False,
        fig_name='noise_pulses_rfi',
        ext='pdf'
    )

    o_tc = RFIm().tdsc_amber(obs.window.copy())
    o_fc = RFIm().fdsc_amber(obs.window.copy())
    plot_multi_images(
        (
            o_tc,
            o_fc,
            obs.frequency_cleaning(obs.time_cleaning(), keep_state=True),
            obs.dedisperse(dm=500),
        ),

        labels=(
            'RFI mitigation (time)',
            'RFI mitigation (freq.)',
            'RFI mitigation (time and freq.)',
            'Dedispersed RFI mitigation (time and freq., DM=500)',
        ),

        direction='vertical',

        xticks=obs.time_indices[::xstep],
        xtick_labels=["%.2f" % t for t in obs.times[::xstep]],

        yticks=obs.backend.freq_indices[::ystep],
        ytick_labels=["%.0f" % f for f in obs.backend.frequencies[::ystep]],

        xfig_size=12,
        yfig_size=9.4,
        spectrum=False,
        colorbar=False,
        savefig=False,
        fig_name='rficlean',
        ext='pdf'
    )
