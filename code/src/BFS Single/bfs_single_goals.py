# Import deque from the collections module
from collections import deque
import sys

# Read the maze from a file
def load_maze(filename):
    with open(filename, 'r') as file:
        # Convert each line in the file to a list of characters and remove whitespace
        maze = [list(line.strip()) for line in file]
    return maze

# Find the position of a character in the maze
def find_character_position(maze, char):
    # Loop through the rows and columns of the maze
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            # If the current position contains the given character, return its row and column
            if maze[row][col] == char:
                return row, col
    # If the character is not found, return None
    return None

# Get valid neighboring cells for a given cell in the maze
def get_valid_neighbors(maze, row, col):
    # Define possible movement directions: up, left, down, right
    directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    neighbors = []
    for dr, dc in directions:
        # Calculate the new row and column indices for the given direction
        new_row, new_col = row + dr, col + dc
        # If the new position is inside the maze and not a wall, add it to the list of neighbors
        if 0 <= new_row < len(maze) and 0 <= new_col < len(maze[0]) and maze[new_row][new_col] != '%':
            neighbors.append((new_row, new_col))
    return neighbors

# Breadth-First Search algorithm to find the shortest path from the start to the goal in a maze
def bfs(maze, start, goal):
    # Create an empty set of visited positions, a queue with the starting position, and a list to store the path to the goal
    visited = set()
    queue = deque([(start, [], 0)])
    max_depth = 0
    max_fringe = 0

        # Update the maximum fringe size
        max_fringe = max(max_fringe, len(queue))
        # Get the current position, path, and depth from the front of the queue
        current, path, depth = queue.popleft()
        # If the current position is the goal, return the path and its cost
        if current == goal:
            return path + [current], depth, len(visited), max_depth, max_fringe

        # If the current position has not been visited yet
        if current not in visited:
            # Add it to the visited set, update the maximum depth, and expand its neighbors
            visited.add(current)
            max_depth = max(max_depth, depth)
            for neighbor in get_valid_neighbors(maze, *current):
                queue.append((neighbor, path + [current], depth + 1))

    # If the goal is not found, return None and the number of visited nodes, maximum depth, and maximum fringe size
    return None, 0, len(visited), max_depth, max_fringe

# Print the maze with the path to the goal marked by dots
def display_solution(maze, path):
    for row, col in path[1:-1]:
        maze[row][col] = '.'
    for row in maze:
        print(''.join(row))

# Main function to read the maze, find the start and goal positions, and run the BFS algorithm
def main():
    maze = load_maze(sys.argv[1])
    start = find_character_position(maze, 'P')
    goal = find_character_position(maze, '.')

    path, cost, nodes_expanded, max_depth, max_fringe = bfs(maze, start, goal)

    print("\na. Solution and its path cost:\n")
    display_solution(maze, path)
    print("\nPath cost:", cost)

    print("\nb. Number of nodes expanded:", nodes_expanded)
    print("c. Maximum tree depth searched:", max_depth)
    print("d. Maximum size of the fringe:", max_fringe)

if __name__ == "__main__":
    main()
