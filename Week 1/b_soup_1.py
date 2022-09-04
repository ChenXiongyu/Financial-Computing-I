
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from urllib.request import urlopen  # b_soup_1.py
from bs4 import BeautifulSoup

# 2a
html = urlopen('https://home.treasury.gov/'
               'resource-center/data-chart-center/'
               'interest-rates/TextView?type=daily_treasury'
               '_yield_curve&field_tdr_date_value=2021')
bsyc = BeautifulSoup(html.read(), "lxml")

table_list = bsyc.findAll('table')
table = table_list[0]

rows = table.findAll('tr')
headers = rows[0].findAll('th')

Headers = [headers[0].contents[0]]
for h in headers[8:]:
    Headers.append(h.contents[0].lower())
daily_yield_curves = [Headers]

for row in rows[1:]:
    data = []
    row_data = row.findAll('td')
    data.append(row_data[0].contents[0].contents[0])
    for d in row_data[8:]:
        data.append(float(d.contents[0]))
    daily_yield_curves.append(data)

with open('daily_yield_curves.txt', 'wt') as fout:
    fout.write('   ' + daily_yield_curves[0][0] + '    ')
    fout.write(' '.join(daily_yield_curves[0][1:]))
    fout.write('\n')
    for line in daily_yield_curves[1:]:
        for data in line[:-3]:
            if type(data) == float:
                fout.write('{:.2f} '.format(data))
            else:
                fout.write(data + ' ')
        for data in line[-3:]:
            fout.write('{:.2f}  '.format(data))
        fout.write('\n')


# 2b
X, Y = np.meshgrid(range(len(daily_yield_curves) - 1),
                   [1, 2, 3, 6, 12, 24, 36, 60, 84, 120, 240, 360])
Z = np.array(np.array(daily_yield_curves).T[1:, 1:], dtype=float)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.set_xlabel('trading days since 01/04/21')
ax.set_ylabel('months to maturity')
ax.set_zlabel('rate')
price = ax.plot_surface(X, Y, Z, cmap='coolwarm')
fig.colorbar(price, shrink=0.5, aspect=5, pad=0.15)
plt.show()

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.set_xlabel('trading days since 01/04/21')
ax.set_ylabel('months to maturity')
ax.set_zlabel('rate')
price = ax.plot_wireframe(X, Y, Z, cmap='coolwarm')
plt.show()

# 2c
yield_curve_df = pd.DataFrame(daily_yield_curves[1:],
                              columns=daily_yield_curves[0])
yield_curve_df = yield_curve_df.set_index(['Date'])
yield_curve_df.plot()
plt.show()

by_day_yield_curve_df = yield_curve_df.T
by_day_yield_curve_df = by_day_yield_curve_df.iloc[:, 0::20]
by_day_yield_curve_df.index = [1, 2, 3, 6, 12, 24, 36, 60, 84, 120, 240, 360]
by_day_yield_curve_df.plot()
plt.show()