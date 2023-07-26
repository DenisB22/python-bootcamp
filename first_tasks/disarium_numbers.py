
disarium_numbers_between_1_and_200 = []

for i in range(1, 201):

    nums = [int(x) for x in list(str(i))]

    is_disarium = False

    sum_nums = 0

    for j in range(len(nums)):
        sum_nums += nums[j] ** (j + 1)

    if sum_nums == int(''.join([str(x) for x in nums])):
        is_disarium = True

        disarium_numbers_between_1_and_200.append(i)

print(f"The Disarium Numbers between 1 and 200 are: {', '.join([str(x) for x in disarium_numbers_between_1_and_200])}")
