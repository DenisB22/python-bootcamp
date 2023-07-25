from unittest import TestCase

from tic_tac_toe.tic_tac_toe import choose_first, player_input, space_check, player_choice, place_marker, \
    full_board_check, win_check, replay, renew_board


class TicTacToeTests(TestCase):

    def test_choose_first_correct_range(self):
        number_in_range = choose_first()
        self.assertTrue(number_in_range in [1, 2])

    def test_player_input_correct_value(self):
        symbol = player_input()
        self.assertTrue(symbol in ['X', 'O'])

    def test_player_input_str_type(self):
        symbol = player_input()
        self.assertTrue(type(symbol) == str)

    def test_space_check_small_x_and_o_incorrect_values(self):
        board = ['x', 'o', 'x', 'o']
        result = space_check(board, 0)
        self.assertEqual(True, result)

    def test_player_chooses_free_position_return_correct_position(self):
        board = ['', 'O', 'X', 'O']
        position = player_choice(board)
        self.assertEqual(0, position)

    def test_place_marker_tests_marker_on_free_position(self):
        board = [
            ' ', 'O', 'X',
            'O', ' ', ' ',
            ' ', ' ', ' '
        ]
        marker = 'X'
        position = 0
        place_marker(board, marker, position)
        self.assertEqual(['X', 'O', 'X', 'O', ' ', ' ', ' ', ' ', ' '], board)

    def test_full_board_check_returns_true_when_full_board(self):
        board = [
            'X', 'O', 'X',
            'O', 'X', 'O',
            'O', 'X', 'O'
        ]

        result = full_board_check(board)
        self.assertTrue(result)

    def test_full_board_check_returns_false_when_not_full_board(self):
        board = [
            ' ', 'O', 'X',
            ' ', 'X', 'O',
            'O', ' ', 'O'
        ]

        result = full_board_check(board)
        self.assertFalse(result)

    def test_win_check_when_there_is_winner(self):
        board = [
            ' ', 'O', 'X',
            ' ', 'X', 'O',
            'X', ' ', 'O'
        ]

        symbol = 'X'

        result = win_check(board, symbol)

        self.assertTrue(result)

    def test_replay_return_correct(self):
        result = replay()

        self.assertTrue(result in ['Y', 'N'])

    def test_renew_board_returns_new_empty_board(self):
        board = renew_board([])

        self.assertEqual(['1', '2', '3', '4', '5', '6', '7', '8', '9'], board)


