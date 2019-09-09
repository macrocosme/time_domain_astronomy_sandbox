"""Pulse class."""
import numpy as np
from .backend import Backend
from ipywidgets import interact
import ipywidgets as widgets
from matplotlib import pyplot as plt
from matplotlib import rc

rc('font', size=16)
rc('axes', titlesize=18)
rc('axes', labelsize=18)

class Pulse():
    def __init__(self,
                 backend : Backend = Backend(),
                 width : int = 10,
                ):
        """Initialise Pulse class.

        Parameters
        ----------
        backend : Backend
            Backend class
        width : int
            Pulse width in second (default: 10)

        """
        self.backend = backend
        self.width = width

        # Frequency delay
        self.dt = lambda dm, f_i : (4.148808 * 1000 * (f_i**-2 - self.backend.fmax**-2)) * dm
    def delays(self, dm):
        """Create array of delays for each backend frequency channel.

        Parameters
        ----------
        dm:int
            Value for dispersion measure of the pulse

        Returns
        -------
        delays:Numpy.array
            Array of delays (in second)

        """
        return np.array([self.dt(dm, f) for f in  self.backend.frequencies])

    def plot_delay_v_frequency(self, dm, xscale='linear',
                               savefig=False, ext='png'):
        """Plot pulse's delay vs frequency.

        Parameters
        ----------
        dm : int
            Value for dispersion measure of the pulse
        xscale : str
            matplotlib's xscale option (default: 'linear')
        savefig : bool
            save figure to disk (default: False)
        ext : 'str'
            figure's file extention (default: png)

        """
        ncols=1
        nrows=1
        fig, ax = plt.subplots(figsize=(10, 5), ncols=ncols, nrows=nrows)
        ax.plot(self.delays(dm), self.backend.frequencies)
        ax.set_xlabel('Delay (s)')
        ax.set_ylabel('Frequency (MHz)')
        if xscale:
            ax.set_xscale(xscale)

        if savefig:
            fig.savefig('%d.pdf' % dm, )

    def plot_delay_v_frequency_interactive(self, xscale='linear', dm_min=0,
                                           dm_max=5000, dm_step=5, dm_init=0,
                                           savefig=False):
        """Plot pulse's delay vs frequency interactively with ipywidgets.

        Parameters
        ----------
        xscale : str
            matplotlib's xscale option
        dm_min : int
            minimum dm for interactive widget (default: 0)
        dm_max : int
            maximum dm for interactive widget (default: 5000)
        dm_step : int
            increment step dm for interactive widget (default: 0)
        dm_init : int
            initial dm for interactive widget (default: 5000)
        savefig : bool
            save figure to disk (default: False)
        ext : 'str'
            figure's file extention

        """
        interact(
            self.plot_delay_v_frequency,
            dm=widgets.IntSlider(min=dm_min, max=dm_max, step=dm_step, value=dm_init),
            xscale=xscale,
        )
