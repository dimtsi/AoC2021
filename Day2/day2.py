with open("input.txt", "r") as f:
    commands = f.read().strip().split("\n")

horiz, depth = 0, 0

for command in commands:
    dir, val = command.split()
    val = int(val)
    if dir == "forward":
        horiz += val
    if dir == "up":
        depth -= val
    if dir == "down":
        depth += val

print(f"p1: {horiz * depth}")

# p2
horiz, depth, aim = 0, 0, 0

for command in commands:
    dir, val = command.split()
    val = int(val)
    if dir == "forward":
        horiz += val
        depth += aim * val
    elif dir == "up":
        aim -= val
    else:
        aim += val

print(f"p2: {horiz * depth}")
