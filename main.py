import random

MAX_LINES = 3
MAX_BET = 10000000000
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
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else: 
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)

    return winnings, winning_lines

def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)

        columns.append(column)

    return columns

def print_slot_machine(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=' | ')
            else:
                print(column[row], end='')

        print()

def deposit():
    while True:
        amount = input('What would you like to deposit? $')
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print('Amount must be greater than 0.')
        else:
            print('Please enter a number.')

    return amount

def get_number_of_lines():
    while True:
        lines = input('Enter the number of lines to bet on (1-' + str(MAX_LINES) + ')? ')
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print('Enter a valid number of lines')
        else:
            print('Please enter a number.')

    return lines

def get_bet():
    while True:
        amount = input('What would you like to bet on each line? $')
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(F'Amount must be between ${MIN_BET} - ${MAX_BET}')
        else:
            print('Please enter a number.')

    return amount

def spin(balance, lines, bet):
    total_bet = bet * lines
    if total_bet > balance:
        print(F'You do not have enough to bet that amount, your current balance is: ${balance}')
        return 0  # No change in balance

    print(
        F'You are betting ${bet} on {lines} lines. Total bet is equal to: ${total_bet}')
    
    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(F'YOU WON ${winnings}!')
    print(F'You won on lines:', *winning_lines)
    return winnings - total_bet

def main():
    balance = deposit()
    while True:
        print(F'Current Balance is ${balance}')
        lines = get_number_of_lines()
        bet = get_bet()

        while True:
            balance += spin(balance, lines, bet)
            if balance <= 0:
                print('You have run out of money!')
                return

            repeat = input('Would you like to repeat your bet? (y/n): ')
            if repeat.lower() != 'y':
                break

    print(F'You left with ${balance}')

main()
