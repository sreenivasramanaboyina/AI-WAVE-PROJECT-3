import heapq
import sys

# Read the maze from the file
def load_maze(file_name):
    maze = []
    with open(file_name, 'r') as file:
        for line in file:
            maze.append(list(line.strip()))
    return maze

# Find the starting position in the maze
def find_start_position(maze):
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 'P':
                return (i, j)

# Find the goal position in the maze
def find_goal_position(maze):
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == '.':
                return (i, j)

# Calculate the Manhattan distance heuristic
def calculate_manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Get the neighbors of a given position in the maze
def get_valid_neighbors(maze, pos):
    neighbors = []
    for delta in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_pos = (pos[0] + delta[0], pos[1] + delta[1])
            maze[new_pos[0]][new_pos[1]] != '%'):
            neighbors.append(new_pos)
    return neighbors

# Run the A* algorithm to find the shortest path in the maze
def find_shortest_path(maze):
    start = find_start_position(maze)
    goal = find_goal_position(maze)
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
    # Load the maze from the file
    maze = load_maze(sys.argv[1])

    # Find the shortest path in the maze
    result = find_shortest_path(maze)

    # Print the solution and its path cost
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
