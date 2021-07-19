import pandas as pd
import csv
import os
import math

# The Betting Algorithm ____________________________________________________________________________________________________________________________________________________________________

# We are betting that the team will lose a game after reaching win streak threshold

# dataset has form: [game1, game2, ..., gameN]
# where gamei = [1/0, oddswin, oddslose] win = 1 lose = 0

# betting_algorithm returns [return%, list of bank balance during season betting]

def betting_algorithm(InitialBalance, dataset):

    defaultbet = 2
    BankBalance = InitialBalance
    losingbank = 0
    oddsThreshold = 2
    loses = 0

    WinStreak_Current = 0
    WinStreak_Threshold = 1

    BankBalance_Chain = []
    BankBalance_Chain.append(InitialBalance)

    for game in dataset:

        # Determine if we bet on this game
        if (WinStreak_Current >= WinStreak_Threshold):

            # Determine bet sizing for this game
            if losingbank > 0:
                bet = min(BankBalance*0.1, losingbank/(game[2] - 1))

            else:
                bet = defaultbet

            if WinStreak_Current >= 3:
                bet *= 1.2
                if BankBalance > 103:
                    bet *= 1.2
                    if WinStreak_Current >= 4:
                        bet *= 1.2

            if bet >= 10:
                BankBalance_Chain.append(BankBalance)
                continue


            # Stopping betting if bet is too large
            if bet >= 0.3*InitialBalance:
                BankBalance_Chain.append(BankBalance)
                break

            # Betting outcome
            if game[0] == 1: # Team won this game so we lose our bet
                BankBalance -= bet
                losingbank += bet
                WinStreak_Current += 1

            if game[0] == 0: # Team lost this game so we win our bet
                BankBalance += bet*(game[2] - 1)
                losingbank = 0
                WinStreak_Current = 0

        else:
            if game[0] == 1:
                WinStreak_Current += 1
            if game[0] == 0:
                WinStreak_Current = 0

        BankBalance_Chain.append(BankBalance)

    return [str(round(((BankBalance/InitialBalance)-1)*100, 2)), BankBalance_Chain]
