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