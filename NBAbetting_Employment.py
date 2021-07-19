
import pandas as pd
import csv
import os
import math
import statistics

from NBAbetting_Function import betting_algorithm

# Running The Betting Algorithm over teams that hit at least 7 loses in first 10 games____________________________________________________________________________________________________

teams = ['Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets', 'Chicago Bulls', 'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets',
        'Detroit Pistons', 'Golden State Warriors', 'Houston Rockets', 'Indiana Pacers', 'Los Angeles Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies',
        'Miami Heat', 'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks', 'Oklahoma City Thunder', 'Orlando Magic',
        'Philadelphia 76ers', 'Phoenix Suns', 'Portland Trail Blazers', 'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors', 'Utah Jazz', 'Washington Wizards']

average = 0
samples = 0
year = 2010
listofBankchains = []
medianReturnsList = []

while year <= 2020:

    # Getting teams not in top 15 for current season
    path = r'C:\Users\61437\Documents\Data\NBA Data\NBA Standings Data'
    os.chdir(path)
    teams = []

    df = pd.read_csv('NBA ' + str(year) + ' Standings.csv')
    for index, row in df.iterrows():
        if int(row[0]) > 25: # Want teams not in top 10 for current year so choose > 15
            teams.append(str(row[1]))

    yearaverage = 0
    yearsamples = 0

    path = r'C:\Users\61437\Documents\Data\NBA Data\NBA Regular Season Data\NBA Regular Season ' + str(year - 1) + '-' + str(year)
    os.chdir(path)

    for team in teams:

        bracket = []
        teamgames = []

        # If data does not exist: skip team
        if os.path.exists('NBA ' + str(year - 1) + '-' + str(year) + ' regular season - ' + team + '.csv') == False:
            continue

        # If data does exist: continue
        else:
            df = pd.read_csv('NBA ' + str(year - 1) + '-' + str(year) + ' regular season - ' + team + '.csv')

            # Getting data for current season - team
            for index, row in df.iterrows():

                if int(row[3]) > int(row[4]):
                    bracket.append(1)

                if int(row[3]) < int(row[4]):
                    bracket.append(0)

                bracket.append(row[5])
                bracket.append(row[6])

                teamgames.append(bracket)
                bracket = []

            Returns = betting_algorithm(100, teamgames)[0]
            BankChain = betting_algorithm(100, teamgames)[1]

            print(str(year), str(team), Returns + '%')

            # Apending data to summary statistics
            listofBankchains.append(BankChain)
            medianReturnsList.append(float(Returns))

            yearsamples += 1
            yearaverage += float(Returns)
            samples += 1
            average += float(Returns)

    if yearsamples == 0:
        year += 1
        continue
    # Printing average return for current season
    print('')
    print(str(year) + ' Average return ' + str(round(yearaverage/yearsamples, 2)) + '%')
    print('')
    print('')
    year += 1



# Printing average return over entire historical data
print('NBA Average return over 10 years ' + str(round(average/samples, 2)) + '%')

# Printing median return over entire historical data
print('NBA Median return over 10 years ' + str(round(statistics.median(medianReturnsList), 2)) + '%')

# Plotting bank balance vs bets during season for all team-year pairs
longest = 0
for bank in listofBankchains:
    if len(bank) > longest:
        longest = len(bank)

for bank in listofBankchains:
    if len(bank) < longest:
        while len(bank) < longest:
            bank.append(bank[-1])

import matplotlib.pyplot as plt

for bankychain in listofBankchains:
    plt.plot(bankychain)

plt.xlabel('bet number')
plt.ylabel('bank balance')
plt.title('bank balance vs. bet number during season')
plt.show()
