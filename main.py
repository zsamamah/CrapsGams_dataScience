import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

rolls = 0

wins={}
losses={}

def add_win(key):
    if key in wins:
        wins[key] += 1
    else:
        wins[key] = 1

def add_lose(key):
    if key in losses:
        losses[key] += 1
    else:
        losses[key] = 1

def roll_dice():
    """Roll two dice and return their face values as a tuple."""
    global rolls
    rolls+=1
    die1 = random.randrange(1, 7)
    die2 = random.randrange(1, 7)
    return (die1, die2) # pack die face values into a tuple

def display_dice(dice):
    """Display one roll of the two dice."""
    die1, die2 = dice # unpack the tuple into variables die1 and die2
    #print(f'Player rolled {die1} + {die2} = {sum(dice)}')
    

def play_game():
    die_values = roll_dice() # first roll
    display_dice(die_values)

    # determine game status and point, based on first roll
    sum_of_dice = sum(die_values)
    if sum_of_dice in (7, 11): # win
        game_status = 'WON'
    elif sum_of_dice in (2, 3, 12): # lose
        game_status = 'LOST'
    else: # remember point
        game_status = 'CONTINUE'
        my_point = sum_of_dice
        #print('Point is', my_point)
        
    # continue rolling until player wins or loses
    while game_status == 'CONTINUE':
        die_values = roll_dice()
        display_dice(die_values)
        sum_of_dice = sum(die_values)
        if sum_of_dice == my_point: # win by making point
            game_status = 'WON'
        elif sum_of_dice == 7: # lose by rolling 7
            game_status = 'LOST'
            
    # display "wins" or "loses" message
    if game_status == 'WON':
        #print('Player wins')
        add_win(rolls)
    else:
        #print('Player loses')
        add_lose(rolls)
        
    # print('{} - rolls = {}'.format(game_status, rolls))

def main():
    global rolls
    for i in range(1, 1000001):
        play_game()
        rolls=0
    
    #percentage of won games
    wins_percentage = (sum(wins.values())/1000000)*100
    wins_percentage = round(wins_percentage,2)
    print("Percentage of wins: {}%".format(wins_percentage))

    #percentage of loss games
    losses_percentage = (sum(losses.values())/1000000)*100
    losses_percentage = round(losses_percentage,2)
    print("Percentage of losses: {}%".format(losses_percentage))

    #percentage of total games on given roll
    wins_rolls = list(wins.keys())
    # wins_rolls = [int(x) for x in wins_rolls] #convert elements from str to int
    wins_rolls = sorted(wins_rolls) #sort the array

    wins_total_rolls = sum(wins.values())

    #percentage of wins based on rolls
    resolved = []
    cumulative = []
    for i in wins_rolls:
        avg = (wins[i]/wins_total_rolls)*100
        resolved.append(avg)

    cumulative = np.cumsum(resolved)

    count=0
    print("Rolls   Resolved   Cumulative")
    for i in wins_rolls:
        print("{}   {}%   {}%".format(wins_rolls[count], resolved[count], cumulative[count]))
        count+=1
    
def visualisation():
    #define the data frames
    wins_df = pd.DataFrame(list(wins.items()), columns=['Rolls', 'Wins'])
    losses_df = pd.DataFrame(list(losses.items()), columns=['Rolls', 'Losses'])
    
    #visualize wins/losses vs rolls using matplotlib
    #wins
    plt.bar(wins_df['Rolls'], wins_df['Wins'])
    plt.title("Wins vs Rolls")
    plt.xlabel('Rolls')
    plt.ylabel('Wins')
    plt.show()
    plt.savefig('wins_vs_rolls.png')
    #losses
    plt.bar(losses_df['Rolls'], losses_df['Losses'])
    plt.title("Losses vs Rolls")
    plt.xlabel('Rolls')
    plt.ylabel('Losses')
    plt.show()
    plt.savefig('losses_vs_rolls.png')
    
    #visualize wins/losses vs rolls using seaborn
    sns.lineplot(x='Rolls', y='Wins', data=wins_df, color='blue')
    sns.lineplot(x='Rolls', y='Losses', data=losses_df, color='red')
    
    #scatter wins/losses vs rolls using seaborn
    #wins
    sns.scatterplot(x='Rolls',y='Wins',data=wins_df)
    plt.show()
    plt.savefig('scatter_wins_vs_rolls.png')
    #losses
    sns.scatterplot(x='Rolls',y='Losses',data=losses_df)
    plt.show()
    plt.savefig('scatter_losses_vs_rolls.png')

if __name__ == "__main__":
    main()
    visualisation()