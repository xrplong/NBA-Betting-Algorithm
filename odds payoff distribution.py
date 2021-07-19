
import pandas as pd
import csv
import os
import math
import statistics
import matplotlib.pyplot as plt

teams = ['Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets', 'Chicago Bulls', 'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets',
        'Detroit Pistons', 'Golden State Warriors', 'Houston Rockets', 'Indiana Pacers', 'Los Angeles Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies',
        'Miami Heat', 'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks', 'Oklahoma City Thunder', 'Orlando Magic',
        'Philadelphia 76ers', 'Phoenix Suns', 'Portland Trail Blazers', 'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors', 'Utah Jazz', 'Washington Wizards']

payoffbrackets = [[2.0, 2.5], [2.5, 3.0], [3.0, 3.5], [3.5, 4.0], [4.0, 4.5], [4.5, 5.0], [5.0, 100.0]]
payoffcounters = [0, 0, 0, 0, 0, 0, 0]

year = 2010

while year <= 2021:

    path = r'C:\Users\61437\Documents\Data\NBA Data\NBA Regular Season Data\NBA Regular Season ' + str(year - 1) + '-' + str(year)
    os.chdir(path)

    for team in teams:

        # If data does not exist: skip team
        if os.path.exists('NBA ' + str(year - 1) + '-' + str(year) + ' regular season - ' + team + '.csv') == False:
            continue

        # If data does exist: continue
        else:
            df = pd.read_csv('NBA ' + str(year - 1) + '-' + str(year) + ' regular season - ' + team + '.csv')

            # Getting data for current season - team
            for index, row in df.iterrows():

                if (int(row[3]) > int(row[4])) and (row[5] >= 2):
                    for bracket in payoffbrackets:
                        if bracket[0] <= row[5] <= bracket[1]:
                            payoffcounters[payoffbrackets.index(bracket)] += 1

                if (int(row[3]) < int(row[4])) and (row[6] >= 2):
                    for bracket in payoffbrackets:
                        if bracket[0] <= row[6] <= bracket[1]:
                            payoffcounters[payoffbrackets.index(bracket)] += 1
    year += 1

plt.plot(payoffcounters)
plt.xticks([2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0])
plt.show()
