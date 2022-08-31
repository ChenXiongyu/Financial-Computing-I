
from urllib.request import urlopen  # b_soup_1.py
from bs4 import BeautifulSoup

html = urlopen('https://home.treasury.gov/'
  'resource-center/data-chart-center/'
  'interest-rates/TextView?type=daily_treasury'
  '_yield_curve&field_tdr_date_value=2019')

bsyc = BeautifulSoup(html.read(), "lxml")

fout = open('bsyc_temp.txt', 'wt',
		encoding='utf-8')

fout.write(str(bsyc))

fout.close()

# get a list of all table tags
table_list = bsyc.findAll('table')

# how many are there?
print('there are', len(table_list), 'tables')

# there is only one table, so get it
table = table_list[0]

# ... and get a list of all the rows
rows = table.findAll('tr')

# how many rows are there?
print('there are', len(rows), 'table rows')

# first row (sub-0 row) contains column headers
headers = rows[0].findAll('th')

# how many columns are there?
print('there are', len(headers), 'columns')

# get the contents of each header
for h in headers:
    print(h.contents)

# remaining rows contain data for trading days
for row in rows[1:]:
    row_data = row.findAll('td')
    # first row_data is the trading day
    print(row_data[0].contents[0].contents)
    for d in row_data[1:]:
        print(d.contents)

        
