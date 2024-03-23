from collections import deque
from itertools import permutations
import sys

# Read the maze from the file and return it as a list of lists
def load_maze(filename):
    with open(filename, 'r') as file:
        maze = [list(line.strip()) for line in file]
    return maze

# Find the positions of specified characters in the maze
def find_character_positions(maze, characters):
    positions = {char: [] for char in characters}
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] in characters:
                positions[maze[row][col]].append((row, col))
    return positions

# Return a list of neighboring cells that are not walls
def get_valid_neighbors(maze, row, col):
    neighbors = []
    for dr, dc in directions:
            neighbors.append((new_row, new_col))
    return neighbors

# Run Breadth-First Search (BFS) from the start cell to the goal cell, with a limit on the number of nodes expanded
def breadth_first_search(maze, start, goal):
    visited = set()
    queue = deque([(start, [], 0)])  # [current cell, path to current cell, current depth]
    max_depth = 0
    max_fringe = 0
    nodes_expanded = 0

    while queue:
        max_fringe = max(max_fringe, len(queue))
        current, path, depth = queue.popleft()
        if current == goal:
            return path + [current], depth, len(visited), max_depth, max_fringe

        if current not in visited:
            visited.add(current)
            max_depth = max(max_depth, depth)
            nodes_expanded += 1
            for neighbor in get_valid_neighbors(maze, *current):
                if neighbor not in visited:
                    queue.append((neighbor, path + [current], depth + 1))

    return None, 0, len(visited), max_depth, max_fringe

# Print the maze with the path to the goal highlighted
def display_solution(maze, path):
    for row, col in path[1:-1]:
        maze[row][col] = '.'
    for row in maze:
        print(''.join(row))

# Main function
def main():
    # Load the maze from the file and find start and goal positions
    maze = load_maze(sys.argv[1])
    positions = find_character_positions(maze, 'P.')
    start = positions['P'][0]
    goals = positions['.']

    # Initialize variables for statistics
    min_cost = float('inf')
    min_path = []
    total_nodes_expanded = 0
    max_tree_depth = 0
    max_fringe_size = 0

    # Set a limit on the number of nodes to be expanded
    node_limit = len(maze) * len(maze[0]) * 10
    print("\nNode limit set to", node_limit)

    # Try all permutations of goals and find the shortest path
    for goal_order in permutations(goals):
        current_start = start
        current_cost = 0
        current_path = []

        # Find the path to each goal in order and update variables
        for goal in goal_order:
            path, cost, nodes_expanded, max_depth, max_fringe = breadth_first_search(maze, current_start, goal)
            if path is None or total_nodes_expanded >= node_limit:
                print("\na. Solution NOT found")
                print("b. Number of nodes expanded:", total_nodes_expanded)
                print("c. Maximum tree depth searched:", max_tree_depth)
                print("d. Maximum size of the fringe:", max_fringe_size)
                return -1

            current_path += path[:-1]
            current_cost += cost
            current_start = goal

            total_nodes_expanded += nodes_expanded
            max_tree_depth = max(max_tree_depth, max_depth)
            max_fringe_size = max(max_fringe_size, max_fringe)

        if path is not None and current_cost < min_cost:
            min_cost = current_cost
            min_path = current_path

    print("\na. Solution and its path cost:\n")
    display_solution(maze, min_path)
    print("\nPath cost:", min_cost)

    print("\nb. Number of nodes expanded:", total_nodes_expanded)
    print("c. Maximum tree depth searched:", max_tree_depth)
    print("d. Maximum size of the fringe:", max_fringe_size)

if __name__ == "__main__":
    main()
