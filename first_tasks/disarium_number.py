nums = [int(x) for x in list(input())]

is_disarium = False

sum_nums = 0

for i in range(len(nums)):
    sum_nums += nums[i] ** (i + 1)

if sum_nums == int(''.join([str(x) for x in nums])):
    is_disarium = True

print(f"The given number is{'' if is_disarium else ' not'} a Disarium Number")