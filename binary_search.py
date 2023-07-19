def search(list_elements, n):
    lower = 0
    upper = len(list_elements) - 1

    while lower <= upper:
        middle = (lower + upper) // 2

        if list_elements[middle] == n:
            globals()['position'] = middle
            return True
        else:
            if list_elements[middle] < n:
                lower = middle + 1
            else:
                upper = middle - 1

    return False


position = -1

list_elements = [1, 5, 7, 11, 29, 49]

n = 10

if search(list_elements, n):
    print(f"Number found at {position + 1} position.")
else:
    print("Number not found.")