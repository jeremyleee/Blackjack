import random

NUMBER_OF_DECKS = 1

deck_of_cards = []
user_cards = []
dealer_cards = []


def setup_game():
    print('==================================')
    print('Welcome to Blackjack!')
    print('==================================')
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
    if not user_input:
        return False, user_input

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


def get_total_string(total_tuple):
    # hard and soft totals equal
    if total_tuple[0] == total_tuple[1] or total_tuple[1] > 21:
        total = total_tuple[0]

        if total <= 21:
            total_string = 'Total: %d' % total
        else:
            total_string = 'Total: %d (BUST)' % total

    else:
        total_string = 'Total: %d (hard), %d (soft)' % total_tuple

    return total_string


def print_game_status(dealers_turn):
    # Dealer status
    if dealers_turn:
        dealer_cards_string = 'Dealer cards: ' + get_card_string(dealer_cards)
        dealer_total = get_total_value(dealer_cards)
    else:
        dealer_cards_string = 'Dealer cards: %s, X' % dealer_cards[0]
        dealer_total = get_total_value([dealer_cards[0]])

    dealer_total_string = get_total_string(dealer_total)

    print(dealer_cards_string)
    print(dealer_total_string)

    # User status
    user_cards_string = 'Your cards: ' + get_card_string(user_cards)
    user_total = get_total_value(user_cards)

    user_total_string = get_total_string(user_total)

    print(user_cards_string)
    print(user_total_string)
    print('----------------------------------')


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
    if soft > 21:
        return hard
    else:
        return soft


def keep_playing_prompt():
    while True:
        if total_money > 0:
            user_input = input('Keep playing? (y/n) ')
        else:
            print('Out of money. Game over!')
            return False

        if user_input.lower() == 'y':
            return True
        elif user_input.lower() == 'n':
            print('Thanks for playing!')
            return False
        else:
            print('Invalid input. Please try again.')


total_money = setup_game()

while True:
    reset_game()
    wager = 0
    print('----------------------------------')

    while True:
        wager = input('How much would you like to wager? ')

        valid_wager, wager = is_valid_dollar_amount(wager)
        if valid_wager and 0 <= wager <= total_money:
            total_money -= wager
            break
        else:
            print('Please enter valid amount.')

    print('----------------------------------')
    print('Dealing cards...')
    print('----------------------------------')
    initial_deal()

    # User's turn
    user_still_playing = True;

    while user_still_playing:
        print_game_status(False)

        if is_user_bust():
            print('You lose $%d. Remaining money: $%d' % (wager, total_money))
            break

        while True:
            user_choice = input('Hit (h) or stand (s)? ')
            if user_choice.lower() == 'h':
                user_cards.append(get_random_card())
                print('----------------------------------')
                break
            elif user_choice.lower() == 's':
                user_still_playing = False
                print('----------------------------------')
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
            total_money += winnings
            print('You win $%d. Remaining money: $%d' % (wager, total_money))
            break

        if dealer_must_stand():
            print('Dealer stands.')
            print('----------------------------------')
            if user_has_won():
                winnings = wager * 2
                total_money += winnings
                print('You win $%d. Remaining money: $%d' % (wager, total_money))
            elif game_is_tied():
                total_money += wager
                print('Game tied. Remaining money: $%d' % total_money)
            else:
                print('You lose $%d. Remaining money: $%d' % (wager, total_money))

            break

        print('Dealer hits.')
        print('----------------------------------')
        dealer_cards.append(get_random_card())

    if not keep_playing_prompt():
        break
