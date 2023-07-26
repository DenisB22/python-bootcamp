import string
import secrets

"""
1. Password must be between 8 and 12 characters
2. Password should contain AT LEAST: 
    - one capital letter 
    - three number
    - three special symbols from the following - !, @, #, $, %, ^, &, *, <, >, ?, {, }
"""


def validate_password(rand_pass: str) -> bool:
    allowed_symbols = ["!", "@", "#", "$", "%", "^", "&", "*", "<", ">", "?", "{", "}"]

    min_length = 8
    max_length = 12
    at_least_allowed_symbols = 3
    at_least_numbers = 3
    at_least_capitals = 1

    is_length_valid = False
    is_allowed_symbols_valid = False
    is_at_least_numbers_valid = False
    is_at_least_capitals_valid = False

    if min_length <= len(rand_pass) <= max_length:
        is_length_valid = True

    symbols_found_in_allowed_symbols = [x for x in rand_pass if x in allowed_symbols]
    if len(symbols_found_in_allowed_symbols) >= at_least_allowed_symbols:
        is_allowed_symbols_valid = True

    numbers_count = len([x for x in rand_pass if x in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']])
    if numbers_count >= at_least_numbers:
        is_at_least_numbers_valid = True

    capitals_count = len([x for x in rand_pass if x.isupper()])
    if capitals_count >= at_least_capitals:
        is_at_least_capitals_valid = True

    if is_length_valid and is_allowed_symbols_valid and is_at_least_numbers_valid and is_at_least_capitals_valid:
        return True
    else:
        return False


def generate_password() -> str:

    at_least_allowed_symbols = 3
    at_least_numbers = 3
    at_least_capitals = 1

    pswrd = ''
    pswrd_length = secrets.choice([8, 12])

    allowed_symbols = ["!", "@", "#", "$", "%", "^", "&", "*", "<", ">", "?", "{", "}"]
    count_symbols = secrets.choice([at_least_allowed_symbols, pswrd_length - (at_least_numbers + at_least_capitals)])

    count_numbers = secrets.choice([at_least_numbers, pswrd_length - (count_symbols + at_least_capitals)])

    count_capitals = secrets.choice([at_least_capitals, pswrd_length - (count_numbers + count_symbols)])

    for _ in range(count_symbols):
        symbol = secrets.choice(allowed_symbols)
        pswrd += symbol

    for _ in range(count_numbers):
        number = secrets.choice([0, 9])
        pswrd += str(number)

    for _ in range(count_capitals):
        alphabet = list(string.ascii_uppercase)
        capitalized_char = secrets.choice(alphabet)
        pswrd += capitalized_char

    char_list = list(pswrd)
    secrets.SystemRandom().shuffle(char_list)
    pswrd_final = "".join(char_list)

    return pswrd_final


if __name__ == '__main__':
    password = generate_password()
    print(f"The password is: {password}")
    print(f"The password is valid - {validate_password(password)}")