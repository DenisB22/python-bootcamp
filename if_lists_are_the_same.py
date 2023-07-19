list_one = [1, 2, 3]
list_two = [1, 3, 2]

contains_all_elements = True

# print(sorted(list_one) == sorted(list_two))

for element in list_one:
    if element not in list_two or len(list_one) != len(list_two):
        contains_all_elements = False
        break

print(f"The two lists are the same: {contains_all_elements}")