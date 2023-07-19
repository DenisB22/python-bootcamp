nums_list = [int(x) for x in input().split(', ')]
duplicate_nums_list = []

for i in range(len(nums_list)):
    first_num = nums_list[i]

    for j in range(i + 1, len(nums_list)):
        second_num = nums_list[j]

        if first_num == second_num:
            if first_num not in duplicate_nums_list:
                duplicate_nums_list.append(first_num)

print(f"The duplicate elements in the given array are: {', '.join([str(x) for x in duplicate_nums_list])}")