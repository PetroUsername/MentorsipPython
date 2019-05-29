import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def get_high_values (file):
    with open(file, newline='', encoding="utf8") as csvfile:
        val_list = []
        reader = csv.DictReader(csvfile)
        for row in reader:
            val_list.insert(0, float(row['high']))
        return val_list

def get_low_values (file):
    with open(file, newline='', encoding="utf8") as csvfile:
        val_list = []
        reader = csv.DictReader(csvfile)
        for row in reader:
            val_list.insert(0, float(row['low']))
        return val_list


def get_dates (file):
    with open(file, newline='', encoding="utf8") as csvfile:
        dateslist = []
        reader = csv.DictReader(csvfile)
        for row in reader:
            dateslist= [row['date'].replace('/', '-')] + dateslist
        return dateslist

inp_file = 'EPAM_10years_nasdaq.csv'

years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
years_fmt = mdates.DateFormatter('%Y')

fig, ax = plt.subplots()
ax.plot(get_dates (inp_file), get_high_values (inp_file), color='green')
ax.plot(get_dates (inp_file), get_low_values (inp_file), color='orange')

# add axis labels and title
ax.set_xlabel('Date')
ax.set_ylabel('Price in USD')
ax.set_title('EPAM Stock')

# format the ticks
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(years_fmt)
ax.xaxis.set_minor_locator(months)

# format the coords message box
ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
ax.format_ydata = lambda x: '$%1.2f' % x  # format the price.
ax.grid(True)

# rotates and right aligns the x labels, and moves the bottom of the
# axes up to make room for them
fig.autofmt_xdate()

plt.show()