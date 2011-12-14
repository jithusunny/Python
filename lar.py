#Determines the sub-sequence with largest sum

list = [-2, 9, 7, -1, 8, 0, -3, 6, 7, 0, 8, -6, -1, 9, -9, 0, -7, 8, 3, -1, 9, 7, 4]

sum = 0
max_sum = 0
start_pos = 0
sub_len = 0

len = len(list)

for i in range(0, len):
    for j in range(1, len - i + 1):
        sum = 0
        for k in range(0, j):
            sum += list[i + k]
        if sum > max_sum:
            max_sum = sum
            start_pos = i
            sub_len = j

print 'Maximum sum is:', max_sum

print 'Largest sub array:'

for i in range(start_pos, start_pos + sub_len):
    print list[i],
print
