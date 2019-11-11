import numpy as np

class SNR():
    def __init__(self):
        pass

    def simple_snr(self, a, axis=0):
        a = np.asanyarray(a)
        m = a.mean(axis=axis)
        m_max = m.max()
        sd = m.std()

        vals = np.where(sd == 0, 0, (m-m.mean())/sd)
        return vals
