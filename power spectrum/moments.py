import numpy as np

class Moments:
    def __init__(self, spectra, ipp, nci):
        self.spectra = spectra
        self.nrgb = spectra.shape[0]
        self.nfft = spectra.shape[1]
        self.ipp = ipp
        self.nci = nci

    def compute(self):
        # x = 1 / (2 * self.ipp * 1e-6 * self.nci)
        # res = 2 * x / self.nfft
        # xax = np.linspace(-self.nfft/2, self.nfft/2 - 1, self.nfft)
        # fn = xax * res
        # max_val = np.max(self.spectra, axis=1)
        # mxt1db = 10 * np.log10(max_val)
        # delpdb = 1
        # r1byr2 = 10

        # while r1byr2 > 1.0002:
        #     testdb = mxt1db - delpdb
        #     testval = 10**(testdb / 10)
        #     sn = np.minimum(self.spectra, testval)
        #     sumfn2sn = np.sum((fn**2) * sn)
        #     sumfnsn = np.sum(fn * sn)
        #     sumsn = np.sum(sn)
        #     sigma2 = (sumfn2sn / sumsn) - (sumfnsn / sumsn)**2
        #     sigmaN2 = ((2 * x)**2) / 2
        #     P = np.mean(sn)
        #     Q = np.mean(sn*2) - P*2
        #     R1 = sigmaN2 / sigma2
        #     R2 = P**2 / Q
        #     r1byr2 = R1 / R2
        #     delpdb += 0.01
        x = 1 / (2 * self.ipp * 1e-6 * self.nci)
        res = 2 * x / self.nfft
        xax = np.linspace(-self.nfft/2, self.nfft/2 - 1, self.nfft)
        fn = xax * res

        tot_power_list = []
        mndop_list = []
        dw_list = []
        snr_list = []
        noise_list = []
        for i in range(self.nrgb):

            t1 = self.spectra[i, :]
            max_val = np.max(t1)
            mxt1db = 10 * np.log10(max_val)
            delpdb = 1
            r1byr2 = 10

            while r1byr2 > 1.0002:
                testdb = mxt1db - delpdb
                testval = 10**(testdb / 10)
                sn = np.minimum(t1, testval)
                sumfn2sn = np.sum((fn**2) * sn)
                sumfnsn = np.sum(fn * sn)
                sumsn = np.sum(sn)
                sigma2 = (sumfn2sn / sumsn) - (sumfnsn / sumsn)**2
                sigmaN2 = ((2 * x)**2) / 2
                P = np.mean(sn)
                Q = np.mean(sn*2) - P*2
                R1 = sigmaN2 / sigma2
                R2 = P**2 / Q
                r1byr2 = R1 / R2
                delpdb += 0.01

            noise_list.append(P)
            pn = t1 - P
            tot_power = np.sum(np.maximum(pn, 0))
            mean_doppler = np.sum(fn * pn) / tot_power
            doppler_width = 2 * np.sqrt(np.sum((fn - mean_doppler)**2 * pn) / tot_power)
            snr_db = 10 * np.log10(tot_power / (self.nfft * P))

            tot_power_list.append(tot_power)
            mndop_list.append(mean_doppler)
            dw_list.append(doppler_width)
            snr_list.append(snr_db)

        return noise_list, tot_power_list, mndop_list, dw_list, snr_list