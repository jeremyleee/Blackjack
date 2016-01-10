import random

NUMBER_OF_DECKS = 1

deck_of_cards = []
user_cards = []
dealer_cards = []


def setup_game():
    print('Welcome to Blackjack!')
    money = 0

    while True:
        money = input('How much money would you like to bring to the table? ')
        valid_dollar_amount, money = is_valid_dollar_amount(money)
        if valid_dollar_amount:
            break
        else:
            print('Please enter valid amount.')

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


def get_random_card():
    random_int = random.randint(0, len(deck_of_cards) - 1)
    return deck_of_cards.pop(random_int)


def initial_deal():
    user_cards.append(get_random_card())
    user_cards.append(get_random_card())

    dealer_cards.append(get_random_card())
    dealer_cards.append(get_random_card())


def print_game_status():
    # Dealer status
    dealer_cards_string = 'Dealer cards: %s, X' % dealer_cards[0]
    dealer_total = get_card_value(dealer_cards[0])

    print(dealer_cards_string)
    print('Total: %d' % dealer_total)

    # User status
    user_cards_string = 'Your cards: ' + get_card_string(user_cards)
    user_total = get_total_value(user_cards)
    if user_total <= 21:
        user_total_string = 'Total: ' + str(user_total)
    else:
        user_total_string = 'Total: ' + str(user_total) + ' (BUST)'

    print(user_cards_string)
    print(user_total_string)


def get_card_string(cards):
    card_string = ''

    for card in cards:
        card_string += card + ', '

    return card_string[:-2]


def get_total_value(cards):
    total = 0

    for card in cards:
        total += get_card_value(card)

    return total


def get_card_value(card):
    try:
        value = int(card)
    except:
        value = 10

    return value


def is_user_bust():
    return get_total_value(user_cards) > 21


total_money = setup_game()

while True:
    reset_game()
    wager = 0

    while True:
        wager = input('How much would you like to wager? ')

        valid_wager, wager = is_valid_dollar_amount(wager)
        if valid_wager and wager <= total_money:
            total_money -= wager
            break
        else:
            print('Please enter valid amount.')

    print('Dealing cards...')
    initial_deal()

    user_still_playing = True;
    # User's turn
    while user_still_playing:
        print_game_status()

        if is_user_bust():
            print("You lose $%d." % wager)
            break

        while True:
            user_choice = input('Hit (h) or stand (s)? ')
            if user_choice == 'h':
                user_cards.append(get_random_card())
                break
            elif user_choice == 's':
                user_still_playing = False
                break
            else:
                print("Please enter valid input.")

    if is_user_bust():
        continue

    # Dealer's turn
    while True:
        print_game_status()
        break
