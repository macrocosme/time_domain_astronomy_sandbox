"""Test functions."""
from .classes.backend import Backend
from .classes.observation import Observation
from .classes.pulse import Pulse
from .classes.plotting import plot_multi_images
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

def pulse_and_rfi__cleaned(spectrum=False):
    """Plot pulses and rfi, and rfi clean.

    Plot DM=1000 Width=6ms S/N=12
    Plot DM=1 Width=6ms S/N=50
    Plot DM=10 Width=6ms S/N=15
    Plot RFI < 32 channels wide

    Property
    --------
    spectrum : bool
    """
    obs = Observation(Backend(), length=1.024)
    raw = obs.window.copy()
    obs.add_dispersed_pulse(dm=1000, width=0.006, pulse_t0=0.16, snr=400)
    obs.add_dispersed_pulse(dm=1, width=0.006, pulse_t0=0.33, snr=50)
    obs.add_dispersed_pulse(dm=10, width=0.006, pulse_t0=0.73, snr=15)

    for f1, f2 in [
        # [100, 132],
        [560, 575],
        # [1220, 1265]
    ]:
        obs.add_rfi(
            t_start=0.,
            t_stop=0.5,
            t_step=0.03,
            f_start=f1, f_stop=f2,
            width=0.01,
            snr=20,
        )

    xstep = 1000
    ystep = 500

    rc('font', size=12)
    rc('axes', titlesize=12)
    rc('axes', labelsize=12)

    o_window = obs.window.copy()
    o_tc = obs.time_cleaning().copy()
    o_fc = obs.frequency_cleaning().copy()

    plot_multi_images(
        (
            raw,
            o_window,
            o_tc,
            o_fc,
            obs.frequency_cleaning(obs.time_cleaning(), keep_state=True),
            obs.dedisperse(dm=1000),
        ),
        direction='vertical',

        xticks=obs.time_indices[::xstep],
        xtick_labels=["%.2f" % t for t in obs.times[::xstep]],

        yticks=obs.backend.freq_indices[::ystep],
        ytick_labels=["%.0f" % f for f in obs.backend.frequencies[::ystep]],

        xfig_size=30,
        yfig_size=10,
        spectrum=spectrum
    )
