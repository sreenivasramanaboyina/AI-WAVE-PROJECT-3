import heapq
import sys

# Read maze from file and return it as a list of lists
def read_maze(filename):
    maze = []
    with open(filename, 'r') as file:
        for line in file:
            maze.append(list(line.strip()))
    return maze

# Find the start position in the maze and return it as a tuple
def find_start_position(maze):
        for j in range(len(maze[i])):
            if maze[i][j] == 'P':
                return (i, j)

# Find all the goals in the maze and return them as a list of tuples
def find_goal_positions(maze):
    goals = []
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == '.':
    return goals

# Calculate Manhattan distance between two positions
def calculate_manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Get all the valid neighboring positions of a given position in the maze
def get_valid_neighbors(maze, position):
    neighbors = []
    for delta in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_position = (position[0] + delta[0], position[1] + delta[1])
        if (0 <= new_position[0] < len(maze) and
            0 <= new_position[1] < len(maze[new_position[0]]) and
            maze[new_position[0]][new_position[1]] != '%'):
            neighbors.append(new_position)
    return neighbors

# Find the shortest path from the start position to all the goals using the A* algorithm
def find_shortest_paths(maze):
    start_position = find_start_position(maze)
    goal_positions = find_goal_positions(maze)
    total_path = []
    total_path_cost = 0
    while goal_positions:
        min_goal = None
        min_path_cost = float('inf')
        for goal in goal_positions:
            path, path_cost, nodes_expanded, max_depth, max_fringe = a_star_search(maze, start_position, goal)
            if path_cost < min_path_cost:
                min_goal = goal
                min_path = path
                min_path_cost = path_cost
        total_path += min_path[:-1]
        total_path_cost += min_path_cost
        goal_positions.remove(min_goal)
        start_position = min_goal
    return (total_path, total_path_cost, nodes_expanded, max_depth, max_fringe)

# A* search algorithm to find the shortest path from start to goal position in the maze
def a_star_search(maze, start, goal):
    frontier = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}
    max_depth = 0
    max_fringe = 0
    nodes_expanded = 0
    while frontier:
        max_fringe = max(max_fringe, len(frontier))
        depth, current = heapq.heappop(frontier)
        if current == goal:
            path = []
            while current != start:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return (path, cost_so_far[goal], nodes_expanded, max_depth, max_fringe)
        if depth > max_depth:
            max_depth = depth
        for neighbor in get_valid_neighbors(maze, current):
            new_cost = cost_so_far[current] + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                nodes_expanded += 1
                cost_so_far[neighbor] = new_cost
                priority = new_cost + calculate_manhattan_distance(neighbor, goal)
                heapq.heappush(frontier, (priority, neighbor))
                came_from[neighbor] = current
    return None

def main():
    maze = read_maze(sys.argv[1])
    result = find_shortest_paths(maze)

    if result:
        print("\na. Solution and its path cost:\n")
        path, path_cost, nodes_expanded, max_depth, max_fringe = result
        for pos in path:
            maze[pos[0]][pos[1]] = '.'
        for row in maze:
            print(''.join(row))
        print("\nPath cost:", path_cost)

        print("\nb. Number of nodes expanded:", nodes_expanded)
        print("c. Maximum tree depth searched:", max_depth)
        print("d. Maximum size of the fringe:", max_fringe)
    else:
        print("No path found")

if __name__ == "__main__":
    main()
