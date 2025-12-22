# "Rock, Paper, Scissors" game implementation in Python


import random

def getChoices():
    playerChoice = input("\n\nEnter a choice ('rock', 'paper', 'scissors') or ('r', 'p', 's'): ").lower()
    
    options = ["rock", "paper", "scissors"]

    computerChoice = random.choice(options)

    choices = {"player": playerChoice, "computer": computerChoice}

    return choices


def checkWin(player, computer):
    print( f"You chose: '{player}'... Computer chose: '{computer}' \n" )

    if (player == computer):
        return "It's a tie!"

    elif (player in ["rock", "r"]):
        if (computer == "scissors"):
            return "Rock smashes scissors! You win!"
        else:
            return "Paper covers rock! You lose..."
    
    elif (player in ["paper", "p"]):
        if (computer == "rock"):
            return "Paper covers rock! You win!"
        else:
            return "Scissors cuts paper! You lose..."

    elif (player in ["scissors", "s"]):
        if (computer == "paper"):
            return "Scissors cuts paper! You win!"
        else:
            return "Rock smashes scissors! You lose..."

    else:
        return "Invalid choice! Please choose 'rock', 'paper', or 'scissors'."

gameOver = False
while (gameOver != True):
    choices = getChoices()
    playerChoice = choices["player"]
    computerChoice = choices["computer"]
    result = checkWin(playerChoice, computerChoice)
    print(result)

    playAgain = input("\nDo you want to play again? (yes/no): ").lower()
    if (playAgain not in ['yes', 'y']):
        gameOver = True
        print("\nThanks for playing! Goodbye!")