# Making frequency graph of win streaks of teams not in top 10 for years 2010 to 2020

import pandas as pd
import csv
import os
import math

year = 2010

winStreakFrequency = {'0' : 0, '1' : 0, '2' : 0, '3' : 0, '4' : 0, '5' : 0, '6' : 0, '7' : 0, '8' : 0, '9' : 0, '10' : 0,
                      '11' : 0, '12' : 0, '13' : 0, '14' : 0, '15' : 0, '16' : 0, '17' : 0, '18' : 0, '19' : 0, '20' : 0,
                      '21' : 0, '22' : 0, '23' : 0, '24' : 0, '25' : 0, '26' : 0, '27' : 0, '28' : 0, '29' : 0, '30' : 0}

while year <= 2020:
    print(year)
    path = r'C:\Users\61437\Documents\Data\NBA Data\NBA Standings Data'
    os.chdir(path)

    # Getting teams not in top 15 for current season
    teams = []
    df = pd.read_csv('NBA ' + str(year) + ' Standings.csv')
    for index, row in df.iterrows():
        if int(row[0]) > 15: # Want teams not in top 10 for current year so choose > 15
            teams.append(str(row[1]))

    path = r'C:\Users\61437\Documents\Data\NBA Data\NBA Regular Season Data\NBA Regular Season ' + str(year - 1) + '-' + str(year)
    os.chdir(path)

    # Getting win streak data for each team in teams
    for team in teams:
        # If data does not exist: skip team
        if os.path.exists('NBA ' + str(year - 1) + '-' + str(year) + ' regular season - ' + team + '.csv') == False:
            continue

        # If data does exist: continue
        else:
            # Finding longest win streak for current team - year
            df = pd.read_csv('NBA ' + str(year - 1) + '-' + str(year) + ' regular season - ' + team + '.csv')
            currentWinStreak = 0
            longestWinStreak = 0
            for index, row in df.iterrows():

                if int(row[3]) > int(row[4]):
                    currentWinStreak += 1
                if int(row[3]) < int(row[4]):
                    if currentWinStreak > longestWinStreak:
                        longestWinStreak = currentWinStreak
                    currentWinStreak = 0

            # Finding average odds payout for current team - year if team loses
            odds = 0
            samples = 0
            for index, row in df.iterrows():
                odds += row[6]
                samples += 1

            averageOdds = round(odds/samples, 2)

            # Printing team - year - win streak
            print(str(year), team, 'Longest Win Streak =', str(longestWinStreak), 'Average payout for team lose is', str(averageOdds))

            # Updating current win streak frequency in dictionary
            currentFrequency = winStreakFrequency[str(longestWinStreak)]
            newFrequency = currentFrequency + 1
            winStreakFrequency.update({str(longestWinStreak) : newFrequency})

    year += 1
    print('')

# Printing average longest win streak over team-season
mean = 0
samples = 0
for key, value in winStreakFrequency.items():
    mean += int(key)*value
    samples += value
mean /= samples

print('Expected longest win streak for teams not in top 15 between 2010 and 2020 is', str(mean))


# Plotting win streak frequency
import matplotlib.pyplot as plt
keys = list(winStreakFrequency.keys())
values = list(winStreakFrequency.values())

plt.bar(range(len(winStreakFrequency)), values, tick_label = keys)
plt.show()
