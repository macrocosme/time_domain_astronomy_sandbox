import numpy as np
from .backend import Backend

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
