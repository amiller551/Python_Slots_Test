#Diagonal winning added. Need to see if Christian has optimization advice


import random

MAX_LINES = 3
MAX_BET = 1000
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    'A': 4,
    'K': 8,
    'Q': 12,
    'J': 16
}

symbol_value = {
    'A': 5,
    'K': 4,
    'Q': 3,
    'J': 2
}

def check_winnings(columns, lines, bet, values):
    #Check winnings based on the symbols in the columns.
    winnings = 0
    winning_lines = []
    
    # Check horizontal and diagonal wins
    for line in range(lines):
        symbol = columns[0][line]
        
        # Horizontal check
        if all(column[line] == symbol for column in columns):
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)

        # Diagonal checks
        if line == 0:  # Top-left to bottom-right
            if all(columns[i][i] == symbol for i in range(min(ROWS, COLS))):
                winnings += values[symbol] * bet
                winning_lines.append('D1')  # Diagonal 1
        if line == 0:  # Top-right to bottom-left
            if all(columns[i][COLS - 1 - i] == symbol for i in range(min(ROWS, COLS))):
                winnings += values[symbol] * bet
                winning_lines.append('D2')  # Diagonal 2

    return winnings, winning_lines

def get_slot_machine_spin(rows, cols, symbols):
    #Generate a random spin for the slot machine.
    all_symbols = [symbol for symbol, count in symbols.items() for _ in range(count)]
    columns = []
    for _ in range(cols):
        column = random.sample(all_symbols, rows)
        columns.append(column)
    return columns

def print_slot_machine(columns):
    #Print the slot machine output.#
    for row in range(ROWS):
        print(" | ".join(column[row] for column in columns))

def deposit():
    #Handle depositing money into the balance.
    while True:
        try:
            amount = int(input('What would you like to deposit? $'))
            if amount > 0:
                return amount
            else:
                print('Amount must be greater than 0.')
        except ValueError:
            print('Please enter a valid number.')

def get_number_of_lines():
    #Get the number of lines to bet on from the user.
    while True:
        try:
            lines = int(input(f'Enter the number of lines to bet on (1-{MAX_LINES}): '))
            if 1 <= lines <= MAX_LINES:
                return lines
            else:
                print(f'Enter a valid number of lines (1-{MAX_LINES}).')
        except ValueError:
            print('Please enter a valid number.')

def get_bet():
    #Get the bet amount from the user.
    while True:
        try:
            amount = int(input(f'What would you like to bet on each line? (${MIN_BET} - ${MAX_BET}): '))
            if MIN_BET <= amount <= MAX_BET:
                return amount
            else:
                print(f'Amount must be between ${MIN_BET} and ${MAX_BET}.')
        except ValueError:
            print('Please enter a valid number.')

def spin(balance, lines, bet):
    #Spin the slot machine and calculate winnings.
    total_bet = bet * lines
    if total_bet > balance:
        print(f'You do not have enough to bet that amount, your current balance is: ${balance}')
        return 0  # No change in balance

    print(f'You are betting ${bet} on {lines} lines. Total bet is: ${total_bet}')
    
    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f'YOU WON ${winnings}!')
    if winning_lines:
        print(f'You won on lines: {", ".join(map(str, winning_lines))}')
    else:
        print('No winning lines this time.')

    return winnings - total_bet

def main():
    #Main function to run the slot machine game.
    balance = deposit()
    while True:
        print(f'Current Balance: ${balance}')
        lines = get_number_of_lines()
        bet = get_bet()

        while True:
            balance_change = spin(balance, lines, bet)
            balance += balance_change
            
            print(f'Your current balance is: ${balance}')  # Display current balance after each spin
            
            if balance <= 0:
                print('You have run out of money!')
                return

            # Check if the player can repeat the bet
            if balance < bet * lines:
                print("You don't have enough money to repeat the bet.")
                choice = input("Would you like to set a new bet (n) or quit (q)? ")
                if choice.lower() == 'n':
                    lines = get_number_of_lines()
                    bet = get_bet()
                elif choice.lower() == 'q':
                    print("Thank you for playing!")
                    return
            else:
                repeat = input('Would you like to repeat your bet? (y to repeat, any other key to set new bet): ')
                if repeat.lower() != 'y':
                    break

        # Ask if the user wants to play again or quit
        play_again = input('Would you like to play again? (y/n): ')
        if play_again.lower() != 'y':
            break

    print(f'You left with ${balance}')

if __name__ == "__main__":
    main()
