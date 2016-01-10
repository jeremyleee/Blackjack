NUMBER_OF_DECKS = 1


def setup_game():
    print("Welcome to Blackjack!")
    money = 0

    while True:
        money = input("How much money would you like to bring to the table? ")
        valid_dollar_amount, money = is_valid_dollar_amount(money)
        if valid_dollar_amount:
            break
        else:
            print("Please enter valid amount.")

    return money


def reset_game():
    single_suit = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    deck_of_cards = []

    for i in range(NUMBER_OF_DECKS):
        deck_of_cards.extend(single_suit)
        deck_of_cards.extend(single_suit)
        deck_of_cards.extend(single_suit)
        deck_of_cards.extend(single_suit)


def is_valid_dollar_amount(user_input):
    # remove any dollar signs
    if user_input[0] == '$':
        user_input = user_input[1:]

    # tests whether input is a number
    try:
        user_input = int(user_input)
        return True, user_input
    except:
        return False, user_input


total_money = setup_game()

while True:
    reset_game()

    while True:
        wager = input("How much would you like to wager? ")

        valid_wager, wager = is_valid_dollar_amount(wager)
        if valid_wager and wager <= total_money:
            break
        else:
            print("Please enter valid amount.")

    # begin game
