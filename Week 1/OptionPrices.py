
#
# File: OptionPrices.py
# Author(s):
#

from numpy import log,exp,sqrt
from scipy.stats import norm   # for Normal CDF

class EuropeanCallOption:
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
                max(binom_tree[ni][j]._stock_price - self._K,
                            0.0))
        if ni < 10:
            print('\nAfter filled in with terminal option values:')
            self.binomialTreePretty(binom_tree)
        # Now work backwards, filling in the
        # option prices in the rest of the tree
        # Your code here

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
'''
    for steps in [10,20,50,100,200,500,1000]:
        print(('Binomial Tree Euro call price, {:d} time intervals: '
              + '${:.4f}').format(steps, ec.binomialPrice(steps)))
'''

# 1.d
'''
    for S0 in [5, 50, 500]:
        # strike price equals stock price
        ecS0 = EuropeanCallOption(S0, S0, 0.1, 0.4, 0.4167)
        print('With S0, K ==', S0, ecS0)
        print(('Binomial Tree Euro call price, 1000 time intervals: '
              + '${:.4f}').format(ecS0.binomialPrice(1000)))
'''

