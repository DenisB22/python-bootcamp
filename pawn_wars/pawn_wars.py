def check_if_white_win(row, col, size):
    if 0 <= row < size and 0 <= col < size:
        if row - 1 == 0:
            return True
    return False


def white_wins_with_capture(row, col, matrix, size):
    if 0 <= row - 1 < size and 0 <= col - 1 < size:
        if matrix[row - 1][col - 1] == "b":
            return True
    if 0 <= row - 1 < size and 0 <= col + 1 < size:
        if matrix[row - 1][col + 1] == "b":
            return True
    return False


def check_if_black_win(row, col, size):
    if 0 <= row < size and 0 <= col < size:
        if row + 1 == size - 1:
            return True
    return False


def black_wins_with_capture(row, col, matrix, size):
    if 0 <= row + 1 < size and 0 <= col - 1 < size:
        if matrix[row + 1][col - 1] == "w":
            return True
    if 0 <= row + 1 < size and 0 <= col + 1 < size:
        if matrix[row + 1][col + 1] == "w":
            return True
    return False


def get_white_coordinates(row, col, matrix, size):
    if 0 <= row - 1 < size and 0 <= col - 1 < size:
        if matrix[row - 1][col - 1] == "b":
            return [row - 1, col - 1]
    if 0 <= row - 1 < size and 0 <= col + 1 < size:
        if matrix[row - 1][col + 1] == "b":
            return [row - 1, col + 1]
    if row - 1 == 0:
        return [row - 1, col]


def get_black_coordinates(row, col, matrix, size):
    if 0 <= row + 1 < size and 0 <= col - 1 < size:
        if matrix[row + 1][col - 1] == "w":
            return [row + 1, col - 1]
    if 0 <= row + 1 < size and 0 <= col + 1 < size:
        if matrix[row + 1][col + 1] == "w":
            return [row + 1, col + 1]
    if row + 1 == size - 1:
        return [row + 1, col]


def play():
    size = 8
    matrix = []
    winner = ""
    coords = []
    with_capture = False
    promoted_to_queen = False
    game_on = True

    for _ in range(size):
        matrix.append(input().split())

    white_current_row, white_current_col = 0, 0
    black_current_row, black_current_col = 0, 0

    for row in range(size):
        for col in range(size):
            if matrix[row][col] == "w":
                white_current_row, white_current_col = row, col
                break
            elif matrix[row][col] == "b":
                black_current_row, black_current_col = row, col
                break
    counter = 0

    while game_on:
        if counter % 2 == 0:
            # White player's turn

            if white_wins_with_capture(white_current_row, white_current_col, matrix, size):
                coords = get_white_coordinates(white_current_row, white_current_col, matrix, size)
                coords_row, coords_col = coords[0], coords[1]
                matrix[white_current_row][white_current_col] = "-"
                white_current_row, white_current_col = coords_row, coords_col
                matrix[white_current_row][white_current_col] = "w"
                winner = "White"
                with_capture = True
                break

            elif check_if_white_win(white_current_row, white_current_col, size):
                coords = get_white_coordinates(white_current_row, white_current_col, matrix, size)
                coords_row, coords_col = coords[0], coords[1]
                matrix[white_current_row][white_current_col] = "-"
                white_current_row, white_current_col = coords_row, coords_col
                matrix[white_current_row][white_current_col] = "w"
                winner = "White"
                promoted_to_queen = True
                break

            matrix[white_current_row][white_current_col] = "-"
            white_current_row, white_current_col = white_current_row - 1, white_current_col
            matrix[white_current_row][white_current_col] = "w"

        elif counter % 2 != 0:
            # Black player's turn

            if black_wins_with_capture(black_current_row, black_current_col, matrix, size):
                coords = get_black_coordinates(black_current_row, black_current_col, matrix, size)
                coords_row, coords_col = coords[0], coords[1]
                matrix[black_current_row][black_current_col] = "-"
                black_current_row, black_current_col = coords_row, coords_col
                matrix[black_current_row][black_current_col] = "b"
                winner = "Black"
                with_capture = True
                break

            elif check_if_black_win(black_current_row, black_current_col, size):
                coords = get_black_coordinates(black_current_row, black_current_col, matrix, size)
                coords_row, coords_col = coords[0], coords[1]
                matrix[black_current_row][black_current_col] = "-"
                black_current_row, black_current_col = coords_row, coords_col
                matrix[black_current_row][black_current_col] = "b"
                winner = "Black"
                promoted_to_queen = True
                break

            matrix[black_current_row][black_current_col] = "-"
            black_current_row, black_current_col = black_current_row + 1, black_current_col
            matrix[black_current_row][black_current_col] = "b"

        counter += 1

    for row_info in range(size):
        for col_info in range(size):
            characterized = f"{chr(97 + col_info)}{size - row_info}"
            matrix[row_info][col_info] = characterized

    winning_row = coords[0]
    winning_col = coords[1]

    if with_capture:
        print(f"Game over! {winner} win, capture on {matrix[winning_row][winning_col]}.")
    else:
        print(f"Game over! {winner} pawn is promoted to a queen at {matrix[winning_row][winning_col]}.")


if __name__ == "__main__":
    play()