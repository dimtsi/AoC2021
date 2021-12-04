with open("input.txt", "r") as f:
    meas = f.read().strip().split("\n")
meas = list(map(int, meas))

inc = 0
for i in range(1, len(meas)):
    if meas[i] > meas[i - 1]:
        inc += 1
print(f"p1: {inc}")


# p2

prev_sum = sum(meas[:3])
inc = 0

for i in range(3, len(meas)):
    curr_sum = prev_sum - meas[i - 3] + meas[i]

    if curr_sum > prev_sum:
        inc += 1
    prev_sum = curr_sum

print(f"p2: {inc}")
