
#
# File: OptionPrices2.py
# Author(s): xiongyuc
#

import time
from numpy import log,exp,sqrt
from scipy.stats import norm   # for Normal CDF
import matplotlib.pyplot as plt

class EuropeanCallOption:
    def __init__(self, S0, K, r, sigma, T):
        self._S0 = S0        # initial stock price
        self._K = K          # strike price
        self._r = r          # risk-free rate
        self._sigma = sigma  # volatility
        self._T = T          # expiration time
    
    def BSMPrice(self):
        d1 = (log(self._S0 / self._K) + (self._r + self._sigma**2 / 2) \
            * self._T) / (self._sigma * sqrt(self._T))
        d2 = d1 - self._sigma * sqrt(self._T)
        return norm.cdf(d1) * self._S0 - \
            norm.cdf(d2) * self._K * exp(-self._r * self._T)

    # Inner class used by the binomial tree model
    class _PriceNode:
        def __init__(self):
            self._stock_price = 0
            self._option_price = 0

    # EuropeanCallOption methods:
    def __str__(self):
        return ('EuropeanCallOption:\n'
                + '  S0: ' + str(self._S0)
                + '  K: ' + str(self._K)
                + '  r: ' + str(self._r)
                + '  sigma: ' + str(self._sigma)
                + '  T: ' + str(self._T))

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
            binom_tree[ni][j]._option_price = (
                max(binom_tree[ni][j]._stock_price - self._K, 0.0))
        if ni < 10:
            print('\nAfter filled in with terminal option values:')
            self.binomialTreePretty(binom_tree)
        # Now work backwards, filling in the
        # option prices in the rest of the tree
        for i in range(ni - 1, -1, -1):
            for j in range(i + 1):
                binom_tree[i][j]._option_price = (
                    exp(-self._r * deltaT)
                    * (p * binom_tree[i+1][j+1]._option_price
                       + q * binom_tree[i+1][j]._option_price))
        if ni < 10:
            print('\nAfter filled in with all option values:')
            self.binomialTreePretty(binom_tree)
        return binom_tree[0][0]._option_price

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


class EuropeanPutOption:
    def __init__(self, S0, K, r, sigma, T):
        self._S0 = S0        # initial stock price
        self._K = K          # strike price
        self._r = r          # risk-free rate
        self._sigma = sigma  # volatility
        self._T = T          # expiration time
    
    def BSMPrice(self):
        d1 = (log(self._S0 / self._K) + (self._r + self._sigma**2 / 2) \
            * self._T) / (self._sigma * sqrt(self._T))
        d2 = d1 - self._sigma * sqrt(self._T)
        return self._K * exp(-self._r * self._T) * (1 - norm.cdf(d2)) - \
            self._S0 * (1 - norm.cdf(d1))

    # Inner class used by the binomial tree model
    class _PriceNode:
        def __init__(self):
            self._stock_price = 0
            self._option_price = 0

    # EuropeanPutOption methods:
    def __str__(self):
        return ('EuropeanPutOption:\n'
                + '  S0: ' + str(self._S0)
                + '  K: ' + str(self._K)
                + '  r: ' + str(self._r)
                + '  sigma: ' + str(self._sigma)
                + '  T: ' + str(self._T))

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
            binom_tree[ni][j]._option_price = (
                max(self._K - binom_tree[ni][j]._stock_price, 0.0))
        if ni < 10:
            print('\nAfter filled in with terminal option values:')
            self.binomialTreePretty(binom_tree)
        # Now work backwards, filling in the
        # option prices in the rest of the tree
        for i in range(ni - 1, -1, -1):
            for j in range(i + 1):
                binom_tree[i][j]._option_price = (
                    exp(-self._r * deltaT)
                    * (p * binom_tree[i+1][j+1]._option_price
                       + q * binom_tree[i+1][j]._option_price))
        if ni < 10:
            print('\nAfter filled in with all option values:')
            self.binomialTreePretty(binom_tree)
        return binom_tree[0][0]._option_price

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


class AmericanCallOption:
    def __init__(self, S0, K, r, sigma, T):
        self._S0 = S0        # initial stock price
        self._K = K          # strike price
        self._r = r          # risk-free rate
        self._sigma = sigma  # volatility
        self._T = T          # expiration time

    # Inner class used by the binomial tree model
    class _PriceNode:
        def __init__(self):
            self._stock_price = 0
            self._option_price = 0

    # AmericanCallOption methods:
    def __str__(self):
        return ('AmericanCallOption:\n'
                + '  S0: ' + str(self._S0)
                + '  K: ' + str(self._K)
                + '  r: ' + str(self._r)
                + '  sigma: ' + str(self._sigma)
                + '  T: ' + str(self._T))

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
            binom_tree[ni][j]._option_price = (
                max(binom_tree[ni][j]._stock_price - self._K,
                            0.0))
        if ni < 10:
            print('\nAfter filled in with terminal option values:')
            self.binomialTreePretty(binom_tree)
        # Now work backwards, filling in the
        # option prices in the rest of the tree
        for i in range(ni - 1, -1, -1):
            for j in range(i + 1):
                binom_tree[i][j]._option_price = \
                    max(binom_tree[i][j]._stock_price - self._K, 
                        (exp(-self._r * deltaT) * 
                         (p * binom_tree[i+1][j+1]._option_price + 
                          q * binom_tree[i+1][j]._option_price)))
        if ni < 10:
            print('\nAfter filled in with all option values:')
            self.binomialTreePretty(binom_tree)
        return binom_tree[0][0]._option_price

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


class AmericanPutOption:
    def __init__(self, S0, K, r, sigma, T):
        self._S0 = S0        # initial stock price
        self._K = K          # strike price
        self._r = r          # risk-free rate
        self._sigma = sigma  # volatility
        self._T = T          # expiration time

    # Inner class used by the binomial tree model
    class _PriceNode:
        def __init__(self):
            self._stock_price = 0
            self._option_price = 0

    # AmericanPutOption methods:
    def __str__(self):
        return ('AmericanPutOption:\n'
                + '  S0: ' + str(self._S0)
                + '  K: ' + str(self._K)
                + '  r: ' + str(self._r)
                + '  sigma: ' + str(self._sigma)
                + '  T: ' + str(self._T))

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
            binom_tree[ni][j]._option_price = (
                max(self._K - binom_tree[ni][j]._stock_price, 0.0))
        if ni < 10:
            print('\nAfter filled in with terminal option values:')
            self.binomialTreePretty(binom_tree)
        # Now work backwards, filling in the
        # option prices in the rest of the tree
        for i in range(ni - 1, -1, -1):
            for j in range(i + 1):
                binom_tree[i][j]._option_price = \
                    max(self._K - binom_tree[i][j]._stock_price, 
                        (exp(-self._r * deltaT) * 
                         (p * binom_tree[i+1][j+1]._option_price + 
                          q * binom_tree[i+1][j]._option_price)))
        if ni < 10:
            print('\nAfter filled in with all option values:')
            self.binomialTreePretty(binom_tree)
        return binom_tree[0][0]._option_price

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


if __name__ == '__main__':
    
    ec = EuropeanCallOption(50.0, 50.0, 0.1, 0.4, 0.4167)

    print(ec)

# 1.a and 1.b
    print('Binomial Tree Euro call price, 5 time intervals: '
          + '${:.4f}'.format(ec.binomialPrice(5)))

# 1.c
    for steps in [10,20,50,100,200,500,1000]:
        print(('Binomial Tree Euro call price, {:d} time intervals: '
              + '${:.4f}').format(steps, ec.binomialPrice(steps)))

# 1.d
    for S0 in [5, 50, 500]:
        # strike price equals stock price
        ecS0 = EuropeanCallOption(S0, S0, 0.1, 0.4, 0.4167)
        print('With S0, K ==', S0, ecS0)
        print(('Binomial Tree Euro call price, 1000 time intervals: '
              + '${:.4f}').format(ecS0.binomialPrice(1000)))

# 1.e

    print(ec)   # same as above
    print(('BSM Euro call price: '
              + '${:.4f}').format(ec.BSMPrice()))
              
    for S0 in [5, 50, 500]:
        # strike price equals stock price
        ecS0 = EuropeanCallOption(S0, S0, 0.1, 0.4, 0.4167)
        print('With S0, K ==', S0, ecS0)
        print(('BSM Euro call price: '
              + '${:.4f}').format(ecS0.BSMPrice()))
    # The result is close to the simulation results

# 1.f
    Sigma = [0.05, 0.10, 0.20, 0.40, 0.80, 1.60, 3.20]
    Price = []
    for sigma in Sigma:
        ecS0 = EuropeanCallOption(50, 50, 0.1, sigma, 0.4167)
        print('With sigma ==', sigma, ecS0)
        result = ecS0.binomialPrice(1000)
        print(('Binomial Tree Euro call price, 1000 time intervals: '
              + '${:.4f}').format(result))
        Price.append(result)
    plt.figure()
    plt.plot(Sigma, Price)  # The price is non-linear with increasing volatility, more like a concave relationship
    plt.title('Binomial Tree Euro call price')
    plt.xlabel('Volatility')
    plt.ylabel('Price')

# 1.g
    
    ec = EuropeanPutOption(50.0, 50.0, 0.1, 0.4, 0.4167)
    print(ec)

    print('Binomial Tree Euro put price, 5 time intervals: '
          + '${:.4f}'.format(ec.binomialPrice(5)))

    for steps in [10,20,50,100,200,500,1000]:
        print(('Binomial Tree Euro put price, {:d} time intervals: '
              + '${:.4f}').format(steps, ec.binomialPrice(steps)))

    for S0 in [5, 50, 500]:
        # strike price equals stock price
        ecS0 = EuropeanPutOption(S0, S0, 0.1, 0.4, 0.4167)
        print('With S0, K ==', S0, ecS0)
        print(('Binomial Tree Euro put price, 1000 time intervals: '
              + '${:.4f}').format(ecS0.binomialPrice(1000)))

    print(ec)   # same as above
    print(('BSM Euro put price: '
              + '${:.4f}').format(ec.BSMPrice()))
              
    for S0 in [5, 50, 500]:
        # strike price equals stock price
        ecS0 = EuropeanPutOption(S0, S0, 0.1, 0.4, 0.4167)
        print('With S0, K ==', S0, ecS0)
        print(('BSM Euro put price: '
              + '${:.4f}').format(ecS0.BSMPrice()))

    Sigma = [0.05, 0.10, 0.20, 0.40, 0.80, 1.60, 3.20]
    Price = []
    for sigma in Sigma:
        ecS0 = EuropeanPutOption(50, 50, 0.1, sigma, 0.4167)
        print('With sigma ==', sigma, ecS0)
        result = ecS0.binomialPrice(1000)
        print(('Binomial Tree Euro put price, 1000 time intervals: '
              + '${:.4f}').format(result))
        Price.append(result)
    plt.figure()
    plt.plot(Sigma, Price)  # The price is non-linear with increasing volatility, more like a concave relationship
    plt.xlabel('Volatility')
    plt.ylabel('Price')
    plt.title('Binomial Tree Euro put price')

# 1.h
    plt.figure()
    for S0 in [5, 50, 500]:
        for sigma in [0.05, 0.10, 0.20, 0.40, 0.80, 1.60, 3.20]:
            ecS0 = EuropeanPutOption(S0, S0, 0.1, sigma, 0.4167)
            plt.scatter(ecS0.binomialPrice(1000), ecS0.BSMPrice())
    plt.plot(range(0, 350), range(0, 350), '--')
    plt.xlabel('Bionomial Price')
    plt.ylabel('BSM Price')
    plt.title('Comparison')

# 1.i
# For S0, K = 50, T = 0.4167, r = 0.1, sigma = 0.4, 
# Binomial Tree with 1000 time intervals call price: $6.1155
# BSM Euro call price: $6.1168
# ERI price: $6.1168
# Binomial Tree with 1000 time intervals put price: $4.0748
# BSM Euro put price: $4.0761
# ERI price: $4.0761

# 2.a

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

# Conclusion: European Call and American Call have the same price under the same setup, 
# European Put is cheaper than American Put under the same setup.

# 2.b
    ecAmer = AmericanCallOption(50, 50, 0.1, 0.4, 0.4167).binomialPrice(1000)
    print(ecAmer)  # 10.1572
    # 10.16 on http://www.coggit.com/freetools
    
    ecAmer = AmericanPutOption(50, 50, 0.1, sigma, 0.4167).binomialPrice(1000)
    print(ecAmer)  # 5.9784
    # 6.01 on http://www.coggit.com/freetools

# 3c
    before_foo = time.time()
    for _ in range(3):
        EuropeanCallOption(50, 50, 0.1, 0.4, 0.4167).binomialPrice(1000)
    after_foo = time.time()
    print('1000-step EuropeanCallOption took average', (after_foo - before_foo) / 3,
                        'seconds to run.')
