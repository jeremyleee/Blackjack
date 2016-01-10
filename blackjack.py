import random

NUMBER_OF_DECKS = 1

deck_of_cards = []
user_cards = []
dealer_cards = []


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
    deck_of_cards.clear()
    user_cards.clear()
    dealer_cards.clear()

    single_suit = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

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


def initial_deal():
    for i in range(2):
        random_int = random.randint(0, len(deck_of_cards) - 1)
        random_card = deck_of_cards.pop(random_int)

        user_cards.append(random_card)

    for i in range(2):
        random_int = random.randint(0, len(deck_of_cards) - 1)
        random_card = deck_of_cards.pop(random_int)

        dealer_cards.append(random_card)


def print_game_status():
    print("User cards: " + str(user_cards))
    print("Dealer cards: " + str(dealer_cards))

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

    print("Dealing cards...")
    initial_deal()
    while True:
        print_game_status()
        break

    break
