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


def print_game_status(dealers_turn):
    # Dealer status
    if dealers_turn:
        dealer_cards_string = 'Dealer cards: ' + get_card_string(dealer_cards)
        dealer_total = get_total_value(dealer_cards)
    else:
        dealer_cards_string = 'Dealer cards: %s, X' % dealer_cards[0]
        dealer_total = get_total_value([dealer_cards[0]])

    # hard and soft totals equal
    if dealer_total[0] == dealer_total[1] or dealer_total[1] > 21:
        dealer_total = dealer_total[0]

        if dealer_total <= 21:
            dealer_total_string = 'Total: %d' % dealer_total
        else:
            dealer_total_string = 'Total: %d (BUST)' % dealer_total

    else:
        dealer_total_string = 'Total: %d (hard), %d (soft)' % dealer_total

    print(dealer_cards_string)
    print(dealer_total_string)

    # User status
    user_cards_string = 'Your cards: ' + get_card_string(user_cards)
    user_total = get_total_value(user_cards)

    # hard and soft totals equal
    if user_total[0] == user_total[1] or user_total[1] > 21:
        user_total = user_total[0]

        if user_total <= 21:
            user_total_string = 'Total: %d' % user_total
        else:
            user_total_string = 'Total: %d (BUST)' % user_total

    else:
        user_total_string = 'Total: %d (hard), %d (soft)' % user_total

    print(user_cards_string)
    print(user_total_string)


def get_card_string(cards):
    card_string = ''

    for card in cards:
        card_string += card + ', '

    return card_string[:-2]


def get_total_value(cards):
    hard_total = 0

    for card in cards:
        hard_total += get_card_value(card)

    soft_total = hard_total
    if 'A' in cards:
        soft_total += 10

    return hard_total, soft_total


def get_card_value(card):
    try:
        value = int(card)
    except:
        if card == 'A':
            value = 1
        else:
            value = 10

    return value


def is_user_bust():
    total = highest_valid_total(*get_total_value(user_cards))
    return total > 21


def is_dealer_bust():
    total = highest_valid_total(*get_total_value(dealer_cards))
    return total > 21


def dealer_must_stand():
    total = highest_valid_total(*get_total_value(dealer_cards))
    return total >= 17


def user_has_won():
    user_total = highest_valid_total(*get_total_value(user_cards))
    dealer_total = highest_valid_total(*get_total_value(dealer_cards))

    return user_total > dealer_total


def game_is_tied():
    user_total = highest_valid_total(*get_total_value(user_cards))
    dealer_total = highest_valid_total(*get_total_value(dealer_cards))

    return user_total == dealer_total


def highest_valid_total(hard, soft):
    if hard > 21:
        return soft
    else:
        return hard


def keep_playing_prompt():
    print('Game end. Remaining money: $%s' % total_money)
    if total_money > 0:
        user_input = input('Keep playing? (y/n) ')
    else:
        print('Out of money. Game over!')
        return False

    if user_input == 'y':
        return True
    else:
        print('Thanks for playing!')
        return False


total_money = setup_game()

while True:
    reset_game()
    wager = 0

    while True:
        wager = input('How much would you like to wager? ')

        valid_wager, wager = is_valid_dollar_amount(wager)
        if valid_wager and 0 <= wager <= total_money:
            total_money -= wager
            break
        else:
            print('Please enter valid amount.')

    print('Dealing cards...')
    initial_deal()

    # User's turn
    user_still_playing = True;

    while user_still_playing:
        print_game_status(False)

        if is_user_bust():
            print('You lose $%d.' % wager)
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
                print('Please enter valid input.')

    if is_user_bust():
        if keep_playing_prompt():
            continue
        else:
            break

    # Dealer's turn
    while True:
        print_game_status(True)

        if is_dealer_bust():
            print('Dealer is bust.')
            winnings = wager * 2
            print('You win $%d.' % wager)
            total_money += winnings
            break

        if dealer_must_stand():
            print('Dealer stands.')
            if user_has_won():
                winnings = wager * 2
                print('You win $%d.' % wager)
                total_money += winnings
            elif game_is_tied():
                print('Game tied.')
                total_money += wager
            else:
                print('You lose $%d.' % wager)
            break

        print('Dealer hits.')
        dealer_cards.append(get_random_card())

    if not keep_playing_prompt():
        break
