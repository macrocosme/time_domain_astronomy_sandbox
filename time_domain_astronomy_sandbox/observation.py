import numpy as np
from .backend import Backend
from .pulse import Pulse
from .rfim import RFIm

class Observation():
    def __init__(self,
                 backend:Backend,
                 length:int = 1, # length in second
                 t0:float = 0.
                ):
        self.backend = backend
        self.length = length
        self.t0 = t0
        self.window = np.random.normal(0, 1, (self.backend.n_channels,
                                              int(self.length*backend.samples_per_second)))
        self.noise_median = np.median(self.window).copy()
        self.noise_std = np.std(self.window).copy()

        # Time
        self.time_to_index = lambda t_i : np.ceil((t_i-self.t0)/self.backend.sampling_time).astype(int)
        self.index_to_time = lambda index : index * self.backend.sampling_time + self.t0
        self.next_time = lambda i : i * self.backend.sampling_time

        self.times = np.array([self.next_time(i) for i in range(int(self.backend.samples_per_second *
                                                                    self.length))])
        self.time_indices = np.array([self.time_to_index(t) for t in self.times])

    def time_cleaning(self, window=[], n_iter=1, keep_state=False):
        if keep_state:
            if len(window) == 0:
                window = RFIm().tdsc_amber(self.window, n_iter=n_iter)
            else:
                window = RFIm().tdsc_amber(window, n_iter=n_iter)
        else:
            if len(window) == 0:
                return RFIm().tdsc_amber(self.window, n_iter=n_iter)
            else:
                return RFIm().tdsc_amber(window, n_iter=n_iter)

        self.window = window
        return window

    def frequency_cleaning(self, window=[], n_iter=1, keep_state=False):
        if keep_state:
            if len(window) == 0:
                window = RFIm().fdsc_amber(self.window, n_iter=n_iter)
            else:
                window = RFIm().fdsc_amber(window, n_iter=n_iter)
        else:
            if len(window) == 0:
                return RFIm().fdsc_amber(self.window, n_iter=n_iter)
            else:
                return RFIm().fdsc_amber(window, n_iter=n_iter)

        self.window = window
        return window

    def dedisperse(self, dm):
        return np.array([
            np.roll(self.window[i].copy(), -r) for i, r in zip(
                range(self.window.shape[0]),
                self.time_to_index(Pulse(self.backend).delays(dm))
            )
        ])

    def add_signal(self, signal_value, x_t0, x_t1, y_t0, y_t1):
        self.window[x_t0:x_t1, y_t0:y_t1] = signal_value

    def add_dispersed_pulse(self, dm, width, pulse_t0, snr=100):
        pulse = Pulse(self.backend, width=width)
        pulse_t_start = self.index_to_time(index=self.time_to_index(pulse_t0).astype(int))
        value = ((self.noise_median + self.noise_std*snr)/self.backend.n_channels)
        t_idx = self.time_to_index(t_i=pulse_t_start+pulse.delays(dm=dm))

        for i in range(t_idx.shape[0]):
            self.add_signal(value, i, i+1, t_idx[i], t_idx[i]+self.time_to_index(pulse.width))

    def add_rfi(self,
                t_start:float=0,
                t_stop:float=10,
                t_step:float=100,
                f_start=200, f_stop=250,
                width=10,
                snr=50,
               ):

        start = self.time_to_index(t_start)
        stop = self.time_to_index(t_stop)
        step = self.time_to_index(t_step)
        width = self.time_to_index(width)

        value = (self.noise_median + snr * self.noise_std)/np.ceil((stop-start)/(step*width)).astype(int)

        for t in range(start, stop, step):
            self.add_signal(value, f_start, f_stop, t, t+width)
