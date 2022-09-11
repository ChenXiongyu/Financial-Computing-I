#
# File: VanillaOptions.py
# Author(s): xiongyuc
#

import time
from numpy import log,exp,sqrt
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

    class _PriceNode:
        def __init__(self):
            self._stock_price = 0
            self._option_price = 0

    def binomialTreePretty(self, binom_tree):
        nlevels = len(binom_tree)
        if nlevels < 10:
            print('\nBinomialTree with', nlevels - 1, 'time steps:')
            for row in range(nlevels):
                print('\nStock:  ', end='')
                ncols = len(binom_tree[row])
                for col in range(ncols):
                    print('{:8.4f}'.format(binom_tree[row][col]._stock_price), end='')
                print('')
                print('Option: ', end='')
                for col in range(ncols):
                    print('{:8.4f}'.format(binom_tree[row][col]._option_price), end='')
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
        binom_tree = []
        for i in range(ni + 1):
            ith_row = [self._PriceNode()
                              for j in range(i+1)]
            binom_tree.append(ith_row)
        if ni < 10:
            print('\nAfter filled in with all 0.0:')
            self.binomialTreePretty(binom_tree)
        # fill tree with stock prices
        for i in range(ni + 1):
            for j in range(i + 1):
                binom_tree[i][j]._stock_price = (
                        self._S0 * u ** j * d ** (i-j))
        if ni < 10:
            print('\nAfter filled in with stock prices:')
            self.binomialTreePretty(binom_tree)
        # fill in terminal node option prices
        for j in range(ni + 1):
            binom_tree[ni][j]._option_price = \
                self.pf(binom_tree[ni][j]._stock_price, self._K)
        if ni < 10:
            print('\nAfter filled in with terminal option values:')
            self.binomialTreePretty(binom_tree)
        # Now work backwards, filling in the
        # option prices in the rest of the tree
        for i in range(ni - 1, -1, -1):
            for j in range(i + 1):
                binom_tree[i][j]._option_price = \
                    self.bi(self._r, self._K, deltaT, p, q, 
                            binom_tree[i][j]._stock_price, 
                            binom_tree[i+1][j+1]._option_price, 
                            binom_tree[i+1][j]._option_price)

        if ni < 10:
            print('\nAfter filled in with all option values:')
            self.binomialTreePretty(binom_tree)
        return binom_tree[0][0]._option_price


class EuropeanCallOption(PlainVanillaOption):
    def __init__(self, S0, K, r, sigma, T):
        
        def pf_fun(stock, K):
            return max(stock - K, 0.0)

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


class EuropeanPutOption(PlainVanillaOption):
    def __init__(self, S0, K, r, sigma, T):
        
        def pf_fun(stock, K):
            return max(K - stock, 0.0)

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


class AmericanCallOption(PlainVanillaOption):
    def __init__(self, S0, K, r, sigma, T):
        
        def pf_fun(stock, K):
            return max(stock - K, 0.0)

        def bi_met(r, K, deltaT, p, q, price_n, price_p, price_q):
            return max(price_n - K, exp(-r * deltaT) * (p * price_p + q * price_q))

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
            return max(K - stock, 0.0)

        def bi_met(r, K, deltaT, p, q, price_n, price_p, price_q):
            return max(K - price_n, exp(-r * deltaT) * (p * price_p + q * price_q))

        PlainVanillaOption.__init__(self, S0, K, r, sigma, T, pf_fun, bi_met)

    def __str__(self):
        return ('AmericanPutOption:\n'
                + '  S0: ' + str(self._S0)
                + '  K: ' + str(self._K)
                + '  r: ' + str(self._r)
                + '  sigma: ' + str(self._sigma)
                + '  T: ' + str(self._T))


if __name__ == '__main__':
    
# 3a Test Code
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