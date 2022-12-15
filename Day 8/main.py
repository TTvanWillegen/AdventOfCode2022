from pull import AocInteraction


#  https://adventofcode.com/2022/day/8
#  --- Day 8: Treetop Tree House ---
#  The expedition comes across a peculiar patch of tall trees all planted carefully in a grid. The Elves explain that a previous expedition planted these trees as a reforestation effort. Now, they're curious if this would be a good location for a tree house.
#  First, determine whether there is enough tree cover here to keep a tree house hidden. To do this, you need to count the number of trees that are visible from outside the grid when looking directly along a row or column.
#  The Elves have already launched a quadcopter to generate a map with the height of each tree (your puzzle input). For example:
#  30373 vvvvv
#  25512 vvviv
#  65332 vvvvv
#  33549 vvvvv
#  35390 vvvvv
#  Each tree is represented as a single digit whose value is its height, where 0 is the shortest and 9 is the tallest.
#  A tree is visible if all of the other trees between it and an edge of the grid are shorter than it. Only consider trees in the same row or column; that is, only look up, down, left, or right from any given tree.
#  All of the trees around the edge of the grid are visible - since they are already on the edge, there are no trees to block the view. In this example, that only leaves the interior nine trees to consider:
#  The top-left 5 is visible from the left and top. (It isn't visible from the right or bottom since other trees of height 5 are in the way.)
#  The top-middle 5 is visible from the top and right.
#  The top-right 1 is not visible from any direction; for it to be visible, there would need to only be trees of height 0 between it and an edge.
#  The left-middle 5 is visible, but only from the right.
#  The center 3 is not visible from any direction; for it to be visible, there would need to be only trees of at most height 2 between it and an edge.
#  The right-middle 3 is visible from the right.
#  In the bottom row, the middle 5 is visible, but the 3 and 4 are not.
#  With 16 trees visible on the edge and another 5 visible in the interior, a total of 21 trees are visible in this arrangement.
#  Consider your map; how many trees are visible from outside the grid?
def part_1(advent_of_code):
    with open('input.txt', 'r') as input_file:
        heightmap = []
        for line in input_file:
            line = line.replace("\n", '')
            ns = list(map(lambda x: int(x), [*line]))
            heightmap.append(ns)
        print(heightmap)
        shadowmap = [[None for _y in range(len(heightmap[0]))] for _x in range(len(heightmap))]
        for x in range(len(heightmap)):
            for y in range(len(heightmap[x])):
                vis = is_visible(heightmap, x, y)
                shadowmap[x][y] = 'v' if vis else 'i'
        print(shadowmap)
        vs = count(shadowmap)
        print(vs)
        advent_of_code.answer(1, vs)


def count(shadowmap):
    vis = 0
    for x in range(len(shadowmap)):
        for y in range(len(shadowmap[x])):
            if shadowmap[x][y] == 'v':
                vis += 1
    return vis


def is_visible(heightmap, x, y):
    return is_visible_left(heightmap, x, y) \
           or is_visible_right(heightmap, x, y) \
           or is_visible_top(heightmap, x, y) \
           or is_visible_bottom(heightmap, x, y)


def is_visible_left(heightmap, x, y):
    height = heightmap[x][y]
    for x_i in range(x, -1, -1):
        if x != x_i and heightmap[x_i][y] >= height:
            return False
    return True


def is_visible_right(heightmap, x, y):
    height = heightmap[x][y]
    for x_i in range(x, len(heightmap)):
        if x != x_i and heightmap[x_i][y] >= height:
            return False
    return True


def is_visible_top(heightmap, x, y):
    height = heightmap[x][y]
    for y_i in range(y, -1, -1):
        if y != y_i and heightmap[x][y_i] >= height:
            return False
    return True


def is_visible_bottom(heightmap, x, y):
    height = heightmap[x][y]
    for y_i in range(y + 1, len(heightmap[x])):
        if y != y_i and heightmap[x][y_i] >= height:
            return False
    return True


#  --- Part Two ---
#  Content with the amount of tree cover available, the Elves just need to know the best spot to build their tree house: they would like to be able to see a lot of trees.
#  To measure the viewing distance from a given tree, look up, down, left, and right from that tree; stop if you reach an edge or at the first tree that is the same height or taller than the tree under consideration. (If a tree is right on the edge, at least one of its viewing distances will be zero.)
#  The Elves don't care about distant trees taller than those found by the rules above; the proposed tree house has large eaves to keep it dry, so they wouldn't be able to see higher than the tree house anyway.
#  In the example above, consider the middle 5 in the second row:
#  30373
#  25512
#  65332
#  33549
#  35390
#  Looking up, its view is not blocked; it can see 1 tree (of height 3).
#  Looking left, its view is blocked immediately; it can see only 1 tree (of height 5, right next to it).
#  Looking right, its view is not blocked; it can see 2 trees.
#  Looking down, its view is blocked eventually; it can see 2 trees (one of height 3, then the tree of height 5 that blocks its view).
#  A tree's scenic score is found by multiplying together its viewing distance in each of the four directions. For this tree, this is 4 (found by multiplying 1 * 1 * 2 * 2).
#  However, you can do even better: consider the tree of height 5 in the middle of the fourth row:
#  30373
#  25512
#  65332
#  33549
#  35390
#  Looking up, its view is blocked at 2 trees (by another tree with a height of 5).
#  Looking left, its view is not blocked; it can see 2 trees.
#  Looking down, its view is also not blocked; it can see 1 tree.
#  Looking right, its view is blocked at 2 trees (by a massive tree of height 9).
#  This tree's scenic score is 8 (2 * 2 * 1 * 2); this is the ideal spot for the tree house.
#  Consider each tree on your map. What is the highest scenic score possible for any tree?
def part_2(advent_of_code):
    with open('input.txt', 'r') as input_file:
        heightmap = []
        for line in input_file:
            line = line.replace("\n", '')
            ns = list(map(lambda x: int(x), [*line]))
            heightmap.append(ns)
        print(heightmap)
        shadowmap = [[None for _y in range(len(heightmap[0]))] for _x in range(len(heightmap))]
        for x in range(len(heightmap)):
            for y in range(len(heightmap[x])):
                score = scenic_score(heightmap, x, y)
                shadowmap[x][y] = score
        print(shadowmap)
        vs = count_max(shadowmap)
        print(vs)
        advent_of_code.answer(2, vs)


def count_max(shadowmap):
    vis = 0
    for x in range(len(shadowmap)):
        for y in range(len(shadowmap[x])):
            if shadowmap[x][y] > vis:
                vis = shadowmap[x][y]
    return vis


def scenic_score(heightmap, x, y):
    c = count_top(heightmap, x, y)
    if c != 0:
        c *= count_left(heightmap, x, y)
    if c != 0:
        c *= count_bottom(heightmap, x, y)
    if c != 0:
        c *= count_right(heightmap, x, y)
    return c


def count_left(heightmap, x, y):
    height = heightmap[x][y]
    score = 0
    for x_i in range(x, -1, -1):
        if x != x_i and heightmap[x_i][y] < height:
            score += 1
        if x != x_i and heightmap[x_i][y] >= height:
            return score + 1
    return score


def count_right(heightmap, x, y):
    height = heightmap[x][y]
    score = 0
    for x_i in range(x, len(heightmap)):
        if x != x_i and heightmap[x_i][y] < height:
            score += 1
        if x != x_i and heightmap[x_i][y] >= height:
            return score + 1
    return score


def count_top(heightmap, x, y):
    height = heightmap[x][y]
    score = 0
    for y_i in range(y, -1, -1):
        if y != y_i and heightmap[x][y_i] < height:
            score += 1
        if y != y_i and heightmap[x][y_i] >= height:
            return score + 1
    return score


def count_bottom(heightmap, x, y):
    height = heightmap[x][y]
    score = 0
    for y_i in range(y + 1, len(heightmap[x])):
        if y != y_i and heightmap[x][y_i] < height:
            score += 1
        if y != y_i and heightmap[x][y_i] >= height:
            return score + 1
    return score


if __name__ == "__main__":
    aoc_interaction = AocInteraction()
    part_1(aoc_interaction)
    part_2(aoc_interaction)
