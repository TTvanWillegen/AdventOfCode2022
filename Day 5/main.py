import re

from pull import AocInteraction


#  https://adventofcode.com/2022/day/5
#  --- Day 5: Supply Stacks ---
#  The expedition can depart as soon as the final supplies have been unloaded from the ships. Supplies are stored in stacks of marked crates, but because the needed supplies are buried under many other crates, the crates need to be rearranged.
#  The ship has a giant cargo crane capable of moving crates between stacks. To ensure none of the crates get crushed or fall over, the crane operator will rearrange them in a series of carefully-planned steps. After the crates are rearranged, the desired crates will be at the top of each stack.
#  The Elves don't want to interrupt the crane operator during this delicate procedure, but they forgot to ask her which crate will end up where, and they want to be ready to unload them as soon as possible so they can embark.
#  They do, however, have a drawing of the starting stacks of crates and the rearrangement procedure (your puzzle input). For example:
#      [D]    
#  [N] [C]    
#  [Z] [M] [P]
#   1   2   3 
#  move 1 from 2 to 1
#  move 3 from 1 to 3
#  move 2 from 2 to 1
#  move 1 from 1 to 2
#  In this example, there are three stacks of crates. Stack 1 contains two crates: crate Z is on the bottom, and crate N is on top. Stack 2 contains three crates; from bottom to top, they are crates M, C, and D. Finally, stack 3 contains a single crate, P.
#  Then, the rearrangement procedure is given. In each step of the procedure, a quantity of crates is moved from one stack to a different stack. In the first step of the above rearrangement procedure, one crate is moved from stack 2 to stack 1, resulting in this configuration:
#  [D]        
#  [N] [C]    
#  [Z] [M] [P]
#   1   2   3 
#  In the second step, three crates are moved from stack 1 to stack 3. Crates are moved one at a time, so the first crate to be moved (D) ends up below the second and third crates:
#          [Z]
#          [N]
#      [C] [D]
#      [M] [P]
#   1   2   3
#  Then, both crates are moved from stack 2 to stack 1. Again, because crates are moved one at a time, crate C ends up below crate M:
#          [Z]
#          [N]
#  [M]     [D]
#  [C]     [P]
#   1   2   3
#  Finally, one crate is moved from stack 1 to stack 2:
#          [Z]
#          [N]
#          [D]
#  [C] [M] [P]
#   1   2   3
#  The Elves just need to know which crate will end up on top of each stack; in this example, the top crates are C in stack 1, M in stack 2, and Z in stack 3, so you should combine these together and give the Elves the message CMZ.
#  After the rearrangement procedure completes, what crate ends up on top of each stack?
def part_1(advent_of_code):
    with open('input.txt', 'r') as input_file:
        starting_position = None
        actions = []
        starting = True
        for line in input_file:
            if starting:
                if line == '\n':
                    starting = False
                    continue
                if line.startswith(' 1 '):
                    continue
                split_line = split_starting_line(line, 3)
                if starting_position is None:
                    starting_position = [[] for _ in split_line]
                for idx, val in enumerate(split_line):
                    if val == '   ':
                        continue
                    a = starting_position[idx]
                    a.append(val)
                    starting_position[idx] = a
            else:
                groups = re.search("move (\d+) from (\d+) to (\d+)", line)
                n, f, t = int(groups.group(1)), int(groups.group(2)), int(groups.group(3))
                actions.append([n, f, t])

        for action in actions:
            n, f, t = action
            for i in range(n):
                starting_position[t-1] = [starting_position[f-1][0]] + starting_position[t-1]
                starting_position[f-1] = starting_position[f-1][1:]
        print(starting_position)
        final_string = ''
        for pos in starting_position:
            final_string += pos[0].replace("[", "").replace("]", "")
        print(final_string)
        
        advent_of_code.answer(1, final_string)


def split_starting_line(input, n):
    input = input.replace("\n", "").replace("     ", "   ").replace("    ", "   ").replace("] [", "][")
    return [(input[i:i + n]) for i in range(0, len(input), n)]



#  --- Part Two ---
#  As you watch the crane operator expertly rearrange the crates, you notice the process isn't following your prediction.
#  Some mud was covering the writing on the side of the crane, and you quickly wipe it away. The crane isn't a CrateMover 9000 - it's a CrateMover 9001.
#  The CrateMover 9001 is notable for many new and exciting features: air conditioning, leather seats, an extra cup holder, and the ability to pick up and move multiple crates at once.
#  Again considering the example above, the crates begin in the same configuration:
#      [D]    
#  [N] [C]    
#  [Z] [M] [P]
#   1   2   3 
#  Moving a single crate from stack 2 to stack 1 behaves the same as before:
#  [D]        
#  [N] [C]    
#  [Z] [M] [P]
#   1   2   3 
#  However, the action of moving three crates from stack 1 to stack 3 means that those three moved crates stay in the same order, resulting in this new configuration:
#          [D]
#          [N]
#      [C] [Z]
#      [M] [P]
#   1   2   3
#  Next, as both crates are moved from stack 2 to stack 1, they retain their order as well:
#          [D]
#          [N]
#  [C]     [Z]
#  [M]     [P]
#   1   2   3
#  Finally, a single crate is still moved from stack 1 to stack 2, but now it's crate C that gets moved:
#          [D]
#          [N]
#          [Z]
#  [M] [C] [P]
#   1   2   3
#  In this example, the CrateMover 9001 has put the crates in a totally different order: MCD.
#  Before the rearrangement process finishes, update your simulation so that the Elves know where they should stand to be ready to unload the final supplies. After the rearrangement procedure completes, what crate ends up on top of each stack?
def part_2(advent_of_code):
    with open('input.txt', 'r') as input_file:
        starting_position = None
        actions = []
        starting = True
        for line in input_file:
            if starting:
                if line == '\n':
                    starting = False
                    continue
                if line.startswith(' 1 '):
                    continue
                split_line = split_starting_line(line, 3)
                if starting_position is None:
                    starting_position = [[] for _ in split_line]
                for idx, val in enumerate(split_line):
                    if val == '   ':
                        continue
                    a = starting_position[idx]
                    a.append(val)
                    starting_position[idx] = a
            else:
                groups = re.search("move (\d+) from (\d+) to (\d+)", line)
                n, f, t = int(groups.group(1)), int(groups.group(2)), int(groups.group(3))
                actions.append([n, f, t])

        for action in actions:
            n, f, t = action
            starting_position[t-1] = starting_position[f-1][0:n] + starting_position[t-1]
            starting_position[f-1] = starting_position[f-1][n:]
        print(starting_position)
        final_string = ''
        for pos in starting_position:
            final_string += pos[0].replace("[", "").replace("]", "")
        print(final_string)

        advent_of_code.answer(2, final_string)


if __name__ == "__main__":
    aoc_interaction = AocInteraction()
    part_1(aoc_interaction)
    part_2(aoc_interaction)
