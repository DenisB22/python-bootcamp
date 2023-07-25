import random


def display_board(board: list):
    print(board[0] + '|' + board[1] + '|' + board[2])
    print(board[3] + '|' + board[4] + '|' + board[5])
    print(board[6] + '|' + board[7] + '|' + board[8])


def choose_first() -> int:
    player_goes_first = random.randint(1, 2)

    return player_goes_first


def player_input() -> str:
    is_correct_symbol = False
    symbol = ''

    while not is_correct_symbol:
        symbol = input('Please enter a symbol: (O, X)\n')

        if symbol in ['O', 'X']:
            is_correct_symbol = True

    return symbol


def space_check(board: list, position: int) -> bool:
    if board[position] != 'X' and board[position] != 'O':
        return True


def player_choice(board: list) -> int:
    position = ''

    is_position_valid = False
    is_free = False

    while is_position_valid is False or is_free is False:
        try:
            position = int(input("Please enter the desired position (1 - 9): \n"))
            position -= 1

            if position in range(0, 9):
                is_position_valid = True
            else:
                print('Position not in range (1 - 9). Please try again.')
                continue

            if space_check(board, position):
                is_free = True
            else:
                print("This position is already taken. Please try again")

        except ValueError:
            print("Wrong position type. Please try again.")

    return position


def place_marker(board: list, marker: str, position: int) -> None:
    if space_check(board, position):

        board[position] = marker
        display_board(board)


def full_board_check(board: list) -> bool:

    return all([True if x in ['X', 'O'] else False for x in board])


def win_check(board: list, symbol: str) -> bool:

    all_directions = {
        'right_down_diagonal': False,
        'left_down_diagonal': False,
        'right': False,
        'down': False,
    }

    for index, element in enumerate(board):
        if element == symbol:

            if index == 0 or index == 3 or index == 6:
                if board[index + 1] == symbol:
                    if board[index + 2] == symbol:
                        all_directions['right'] = True
                        break

            if index == 0 or index == 1 or index == 2:
                if board[index + 3] == symbol:
                    if board[index + 6] == symbol:
                        all_directions['down'] = True
                        break

            if index == 0:
                if board[index + 4] == symbol:
                    if board[index + 8] == symbol:
                        all_directions['right_down_diagonal'] = True

            if index == 2:
                if board[index + 2] == symbol:
                    if board[index + 4] == symbol:
                        all_directions['left_down_diagonal'] = True

    if any(all_directions.values()):
        return True


def replay() -> str:
    correct_input = False
    player_input = ''

    while correct_input is not True:
        player_input = input("Do you want to play one more game? (Y/N): \n")

        if player_input in ['Y', 'N']:
            correct_input = True

    return player_input


def renew_board(board: list) -> list:
    return [str(x) for x in range(1, 10)]


def game() -> None:
    board = [str(x) for x in range(1, 10)]
    players_inputs = []

    player_one = player_input()
    player_two = ''

    if player_one == 'X':
        player_two = 'O'
    else:
        player_two = 'X'

    player_first = choose_first()
    if player_first == 1:
        player_first = player_one
    else:
        player_first = player_two

    collection = [player_one, player_two]
    (collection.remove(player_first))
    player_second = collection[0]

    is_full = full_board_check(board)
    is_won = False
    replay_game = True

    counter = 0
    winner = ''

    while replay_game:

        if full_board_check(board):
            print('Game over. Nobody winds.')

            replay_game = replay()
            if replay_game:
                replay_game = True
                board = renew_board(board)
            else:
                break

        position = player_choice(board)

        if counter % 2 == 0:
            place_marker(board, player_first, position)
            is_won = win_check(board, player_first)
            winner = player_first
        else:
            place_marker(board, player_second, position)
            is_won = win_check(board, player_second)
            winner = player_second

        if is_won:
            print(f'Congratulations. Player "{winner}" won the game.')
            replay_response = replay()

            if replay_response == 'N':
                replay_game = False
            else:
                board = renew_board(board)

        counter += 1


if __name__ == '__main__':
    game()



