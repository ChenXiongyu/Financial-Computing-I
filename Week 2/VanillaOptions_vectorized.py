#
# File: VanillaOptions_vectorized.py
# Author(s): xiongyuc
#

import time
import numpy as np
from numpy import log,exp,sqrt, zeros, array
from scipy.stats import norm   # for Normal CDF
import matplotlib.pyplot as plt

class PlainVanillaOption:
    def __init__(self, S0, K, r, sigma, T, pf_fun, bi_met):
        self._S0 = S0        # initial stock price
        self._K = K          # strike price
        self._r = r          # risk-free rate
        self._sigma = sigma  # volatility
        self._T = T          # expiration time
        self.pf = pf_fun     # payoff function
        self.bi = bi_met     # backward induction met

    def binomialTreePretty(self, binom_tree_stock, binom_tree_option):
        nlevels = len(binom_tree_stock)
        if nlevels < 10:
            print('\nBinomialTree with', nlevels - 1, 'time steps:')
            for row in range(nlevels):
                print('\nStock:  ', end='')
                ncols = len(binom_tree_stock[row])
                for col in range(ncols):
                    print('{:8.4f}'.format(binom_tree_stock[row][col]), end='')
                print('')
                print('Option: ', end='')
                for col in range(ncols):
                    print('{:8.4f}'.format(binom_tree_option[row][col]), end='')
                print('')
            print('')

    def binomialPrice(self, num_intervals):
        # local variables used by this function
        deltaT = self._T / num_intervals
        u = exp(self._sigma * deltaT ** 0.5)
        d = 1 / u
        a = exp(self._r * deltaT)
        p = (a - d) / (u - d)
        q = 1 - p
        # abbreviated name
        ni = num_intervals
        # fill tree with all 0.0s
        
        binom_tree_stock = zeros((ni + 1, ni + 1), dtype=float)
        binom_tree_option = zeros((ni + 1, ni + 1), dtype=float)
        
        if ni < 10:
            print('\nAfter filled in with all 0.0:')
            self.binomialTreePretty(binom_tree_stock, binom_tree_option)

        # fill tree with stock prices
        for i in range(ni + 1):
            binom_tree_stock[i][:(i + 1)] = self._S0 * u ** array(range(0, i + 1)) * \
                d ** (i - array(range(0, i + 1)))

        if ni < 10:
            print('\nAfter filled in with stock prices:')
            self.binomialTreePretty(binom_tree_stock, binom_tree_option)

        # fill in terminal node option prices
        binom_tree_option[ni][:(ni + 1)] = self.pf(binom_tree_stock[ni][:(ni + 1)], self._K)

        if ni < 10:
            print('\nAfter filled in with terminal option values:')
            self.binomialTreePretty(binom_tree_stock, binom_tree_option)

        # Now work backwards, filling in the
        # option prices in the rest of the tree
        for i in range(ni - 1, -1, -1):
            binom_tree_option[i][:(i + 1)] = self.bi(self._r, self._K, deltaT, p, q, 
                                                     binom_tree_stock[i][:(i + 1)], 
                                                     binom_tree_option[i+1][1:(i + 2)], 
                                                     binom_tree_option[i+1][:(i + 1)])

        if ni < 10:
            print('\nAfter filled in with all option values:')
            self.binomialTreePretty(binom_tree_stock, binom_tree_option)

        return binom_tree_option[0][0]


class EuropeanCallOption(PlainVanillaOption):
    def __init__(self, S0, K, r, sigma, T):
        
        def pf_fun(stock, K):
            return np.max((stock - K, np.zeros(len(stock))), axis=0)

        def bi_met(r, K, deltaT, p, q, price_n, price_p, price_q):
            return exp(-r * deltaT) * (p * price_p + q * price_q)

        PlainVanillaOption.__init__(self, S0, K, r, sigma, T, pf_fun, bi_met)

    def __str__(self):
        return ('EuropeanCallOption:\n'
                + '  S0: ' + str(self._S0)
                + '  K: ' + str(self._K)
                + '  r: ' + str(self._r)
                + '  sigma: ' + str(self._sigma)
                + '  T: ' + str(self._T))

    def BSMPrice(self):
        d1 = (log(self._S0 / self._K) + (self._r + self._sigma**2 / 2) \
            * self._T) / (self._sigma * sqrt(self._T))
        d2 = d1 - self._sigma * sqrt(self._T)
        return norm.cdf(d1) * self._S0 - \
            norm.cdf(d2) * self._K * exp(-self._r * self._T)

    def simPrice(self, precision=0.005):
        n_initial = 10000
        zi = np.random.randn(n_initial)
        Si = self._S0 * exp((self._r - 0.5 * self._sigma**2) * self._T + 
                            self._sigma * self._T**0.5 * zi)
        Ci = exp(-self._r * self._T) * \
            np.max((Si - self._K, np.zeros(len(Si))), axis=0)
        Sigmai = sqrt(sum((Ci - np.mean(Ci))**2) / (n_initial - 1))  
              
        n = (norm.ppf(1 - 0.05 / 2) * Sigmai/ precision)**2
        zi = np.random.randn(int(n))
        Si = self._S0 * exp((self._r - 0.5 * self._sigma**2) * self._T + 
                            self._sigma * self._T**0.5 * zi)
        Ci = exp(-self._r * self._T) * \
            np.max((Si - self._K, np.zeros(len(Si))), axis=0)
        return np.mean(Ci)


class EuropeanPutOption(PlainVanillaOption):
    def __init__(self, S0, K, r, sigma, T):
        
        def pf_fun(stock, K):
            return np.max((K - stock, np.zeros(len(stock))), axis=0)

        def bi_met(r, K, deltaT, p, q, price_n, price_p, price_q):
            return exp(-r * deltaT) * (p * price_p + q * price_q)

        PlainVanillaOption.__init__(self, S0, K, r, sigma, T, pf_fun, bi_met)

    def __str__(self):
        return ('EuropeanPutOption:\n'
                + '  S0: ' + str(self._S0)
                + '  K: ' + str(self._K)
                + '  r: ' + str(self._r)
                + '  sigma: ' + str(self._sigma)
                + '  T: ' + str(self._T))

    def BSMPrice(self):
        d1 = (log(self._S0 / self._K) + (self._r + self._sigma**2 / 2) \
            * self._T) / (self._sigma * sqrt(self._T))
        d2 = d1 - self._sigma * sqrt(self._T)
        return self._K * exp(-self._r * self._T) * (1 - norm.cdf(d2)) - \
            self._S0 * (1 - norm.cdf(d1))

    def simPrice(self, precision=0.005):
        n_initial = 10000
        zi = np.random.randn(n_initial)
        Si = self._S0 * exp((self._r - 0.5 * self._sigma**2) * self._T + 
                            self._sigma * self._T**0.5 * zi)
        Pi = exp(-self._r * self._T) * \
            np.max((self._K - Si, np.zeros(len(Si))), axis=0)
        Sigmai = sqrt(sum((Pi - np.mean(Pi))**2) / (n_initial - 1))  

        n = (norm.ppf(1 - 0.05 / 2) * Sigmai/ precision)**2
        zi = np.random.randn(int(n))
        Si = self._S0 * exp((self._r - 0.5 * self._sigma**2) * self._T + 
                            self._sigma * self._T**0.5 * zi)
        Pi = exp(-self._r * self._T) * \
            np.max((self._K - Si, np.zeros(len(Si))), axis=0)
        return np.mean(Pi)


class AmericanCallOption(PlainVanillaOption):
    def __init__(self, S0, K, r, sigma, T):
        
        def pf_fun(stock, K):
            return np.max((stock - K, np.zeros(len(stock))), axis=0)

        def bi_met(r, K, deltaT, p, q, price_n, price_p, price_q):
            return np.max((price_n - K, exp(-r * deltaT) * (p * price_p + q * price_q)), axis=0)

        PlainVanillaOption.__init__(self, S0, K, r, sigma, T, pf_fun, bi_met)

    def __str__(self):
        return ('AmericanCallOption:\n'
                + '  S0: ' + str(self._S0)
                + '  K: ' + str(self._K)
                + '  r: ' + str(self._r)
                + '  sigma: ' + str(self._sigma)
                + '  T: ' + str(self._T))


class AmericanPutOption(PlainVanillaOption):
    def __init__(self, S0, K, r, sigma, T):
        
        def pf_fun(stock, K):
            return np.max((K - stock, np.zeros(len(stock))), axis=0)

        def bi_met(r, K, deltaT, p, q, price_n, price_p, price_q):
            return np.max((K - price_n, exp(-r * deltaT) * (p * price_p + q * price_q)), axis=0)

        PlainVanillaOption.__init__(self, S0, K, r, sigma, T, pf_fun, bi_met)

    def __str__(self):
        return ('AmericanPutOption:\n'
                + '  S0: ' + str(self._S0)
                + '  K: ' + str(self._K)
                + '  r: ' + str(self._r)
                + '  sigma: ' + str(self._sigma)
                + '  T: ' + str(self._T))


if __name__ == '__main__':
    
# 3b Test Code
    plt.figure()
    EuroPrice = []
    AmerPrice = []
    for S0 in [5, 50, 500]:
        EuroPrice.append(EuropeanCallOption(S0, S0, 0.1, 0.4, 0.4167).binomialPrice(1000))
        AmerPrice.append(AmericanCallOption(S0, S0, 0.1, 0.4, 0.4167).binomialPrice(1000))
    plt.plot(EuroPrice, [AmerPrice[i] - EuroPrice[i] for i in range(len(EuroPrice))])
    plt.xlabel('European Call')
    plt.ylabel('American Call - European Call')
    plt.title('Option Price with S0, K increasing')

    plt.figure()
    EuroPrice = []
    AmerPrice = []
    Sigma = [0.05, 0.10, 0.20, 0.40, 0.80, 1.60, 3.20]
    for sigma in Sigma:
        EuroPrice.append(EuropeanCallOption(50, 50, 0.1, sigma, 0.4167).binomialPrice(1000))
        AmerPrice.append(AmericanCallOption(50, 50, 0.1, sigma, 0.4167).binomialPrice(1000))
    plt.plot(EuroPrice, [AmerPrice[i] - EuroPrice[i] for i in range(len(EuroPrice))])
    plt.xlabel('European Call')
    plt.ylabel('American Call - European Call')
    plt.title('Option Price with Sigma increasing')

    plt.figure()
    EuroPrice = []
    AmerPrice = []
    for S0 in [5, 50, 500]:
        EuroPrice.append(EuropeanPutOption(S0, S0, 0.1, 0.4, 0.4167).binomialPrice(1000))
        AmerPrice.append(AmericanPutOption(S0, S0, 0.1, 0.4, 0.4167).binomialPrice(1000))
    plt.plot(EuroPrice, [AmerPrice[i] - EuroPrice[i] for i in range(len(EuroPrice))])
    plt.xlabel('European Put')
    plt.ylabel('American Put - European Put')
    plt.title('Option Price with S0, K increasing')

    plt.figure()
    EuroPrice = []
    AmerPrice = []
    Sigma = [0.05, 0.10, 0.20, 0.40, 0.80, 1.60, 3.20]
    for sigma in Sigma:
        EuroPrice.append(EuropeanPutOption(50, 50, 0.1, sigma, 0.4167).binomialPrice(1000))
        AmerPrice.append(AmericanPutOption(50, 50, 0.1, sigma, 0.4167).binomialPrice(1000))
    plt.plot(EuroPrice, [AmerPrice[i] - EuroPrice[i] for i in range(len(EuroPrice))])
    plt.xlabel('European Put')
    plt.ylabel('American Put - European Put')
    plt.title('Option Price with Sigma increasing')


# 3c
    before_foo = time.time()
    for _ in range(3):
        EuropeanCallOption(50, 50, 0.1, 0.4, 0.4167).binomialPrice(1000)
    after_foo = time.time()
    print('1000-step EuropeanCallOption took average', (after_foo - before_foo) / 3,
                        'seconds to run.')
    
    # For VanillaOptions_vectorized.py, the time is 0.1088864008585612 seconds, 
    # For VanillaOptions.py, the time is 1.5737332503000896 seconds,
    # For OptionPrice2.py, the time is 1.6163543065388997 seconds.
    # Therefore, using inheritance doesn't have an impact on runtime in this case.
    # Using vectorized Numpy code improves the running speed obviously.


# 4
    SimPrices = []
    for precision in [0.01, 0.005, 0.001]:
        before_foo = time.time()
        times = 5
        for _ in range(times):
            SimPrices.append(EuropeanCallOption(50, 50, 0.1, 0.4, 0.4167).
                             simPrice(precision))
        print('Simulation Price: %.3f' % np.mean(SimPrices))
        after_foo = time.time()
        print('simPrice with precision %.3f took average' % precision, 
              (after_foo - before_foo) / times,
              'seconds to run.')
    
    # With precision decreases from 0.01, 0.005, to 0.001, 
    # the average timing results are 0.222s, 0.877s, 32.475s.
    # Therefore, if a result is more precise, more time will be taken to simulate. 