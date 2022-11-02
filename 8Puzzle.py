import copy as cp
import time
class nPuzzle:
    def __init__(self):
        self.visited = []
        enter = int(input(
            "Welcome to my 8-Puzzle Solver. Type '1' to use a default puzzle, or '2' to create your own: "))
        self.puzzle = []
    # if the user has selected 1 then puzzle will be default puzzle
        if enter == 1:
            self.puzzle = [  # initial state of the puzzle
                [4, 1, 2],
                [5, 3, 0],
                [7, 8, 6]
            ]
            self.rows = 3
            self.columns = 3
            self.goal_state = [  # goal state of the puzzle
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 0]
            ]
    #allow user to create own puzzle
        elif enter == 2:
            self.columns = self.rows = int(
                input("Enter number of rows and columns: "))
            for i in range(self.rows):  # iterate over number of rows
                print("Enter number and press enter after each number" +
                      str(i + 1)+":", end=" ")
                # appending empty list to the list initialized above
                self.puzzle.append([])
                for j in range(self.columns):  # iterating over number of columns
                    num = int(input())
                    self.puzzle[i].append(num)
            self.goal_state = []  # initializing empty list
            num = 1  # initializing num variable = 1 for the goal state
            for i in range(self.rows):
                self.goal_state.append([])
                for j in range(self.columns):  # iterating column number of times
                    # base condition if we are at last index then just place 0
                    if (i + 1) == self.rows and (j + 1) == self.columns:
                        self.goal_state[i].append(0)
                    else:
                        self.goal_state[i].append(num)
                    num += 1  # incrementing number by 1
        print(self.goal_state)
        print("Select algorithm.")
        print("(1) for Uniform Cost Search,")
        print("(2) for the Misplaced Tile Heuristic")
        print("(3) the Manhattan Distance Heuristic.")
        algo = int(input())
        if algo == 1:
            self.result, self.d_p = self.search(0)
        elif algo == 2:
            self.result, self.d_p = self.search(1)
        elif algo == 3:
            self.result, self.d_p = self.search(2)

    def get_initial_state(self):
        """function that returns the initial state of the puzzle"""
        return self.puzzle

    def get_goal_state(self):
        """function that returns the goal state of the puzzle"""
        return self.goal_state

    def possible_actions(self, puzzle):
        """a function that returns all possible actions of the given state"""
        possible_actions = []
        # getting the initial state of the puzzle
        i, j = self.get_initial_position(puzzle)
        visited = []
        # marking the position of initial state as visited
        visited.append((i, j))
        if (i - 1) >= 0:  # up move
            if ((i-1), j) not in visited:  # if the action is not visited already
                temp = self.copy(puzzle)  # copying the entries of the puzzle
                # swapping the entries
                temp[(i-1)][j], temp[i][j] = puzzle[i][j], puzzle[(i-1)][j]
                possible_actions.append(temp)  # appending possible action

        if (j - 1) >= 0:  # left move
            if (i, (j-1)) not in visited:  # if the action is not visited already
                temp = self.copy(puzzle)  # copying the entries of the puzzle
                # swapping the entries
                temp[i][(j - 1)], temp[i][j] = puzzle[i][j], puzzle[i][(j - 1)]
                possible_actions.append(temp)  # appending possible action

        if (i + 1) < self.rows:  # down move
            if ((i+1), j) not in visited:  # if the action is not visited already
                temp = self.copy(puzzle)  # copying the entries of the puzzle
                # swapping the entries
                temp[(i+1)][j], temp[i][j] = puzzle[i][j], puzzle[(i+1)][j]
                possible_actions.append(temp)  # appending possible action

        if (j + 1) < self.columns:  # right move
            if (i, (j+1)) not in visited:  # if the action is not visited already
                temp = self.copy(puzzle)  # copying the entries of the puzzle
                # swapping the entries
                temp[i][(j + 1)], temp[i][j] = puzzle[i][j], puzzle[i][(j + 1)]
                possible_actions.append(temp)  # appending possible action

        return possible_actions

    def copy(self, puzzle):
        """ a function that copies the puzzle"""
        temp = list()
        for i in range(len(puzzle)):
            temp.append([])
            for j in range(len(puzzle[i])):
                temp[i].append(puzzle[i][j])
        return temp

    def get_initial_position(self, puzzle, val=0):
        """ a function that returns the initial state of the puzzle"""
        for i in range(self.rows):
            for j in range(self.columns):
                if puzzle[i][j] == val:
                    return (i, j)

    def is_goal(self, puzzle):
        " a function that returns True if the given state is goal otherwise False"
        goal = self.get_goal_state()  # taking the goal state of the puzzle
        for i in range(len(puzzle)):  # iterating row number of times
            for j in range(len(puzzle[i])):  # iterating column number of times
                # checking if any entry is misplaced then return False without checking further
                if puzzle[i][j] != goal[i][j]:
                    return False
        return True

    def heuristic(self, current, goal):
        """a function that calculates the hueristic value of the passed two states"""
        cost = 0
        for i in range(len(current)):
            for j in range(len(current[i])):
                if current[i][j] != goal[i][j]:
                    cost += 1
        return cost

    def manhattan(self, node, goal):
        """ function that calculates the manhattan heuristic of the given states"""
        cost = 0  # initalizing the cost to zero
        for i in range(len(goal)):  # iterating row number of times
            for j in range(len(goal[i])):  # iterating column number of times
                if goal[i][j] == 0:  # if the entry is space then ignore it
                    continue
                if node[i][j] != goal[i][j]:  # if the entries mismatched
                    misplaced_val = node[i][j]
                    wrong_pos = self.get_initial_position(
                        node, misplaced_val)  # taking position of the entry
                    correct_pos = self.get_initial_position(
                        goal, misplaced_val)
                    x = abs(wrong_pos[0] - correct_pos[0])
                    y = abs(wrong_pos[1] - correct_pos[1])

                    distance = x + y  # calculating distance
                    cost += distance
        return cost

    def search(self, algo=0):
        """Search algorithm"""
        start = time.time()
        initial = self.get_initial_state()
        queue = [(0, ([], initial))]
        visited_nodes = []
        depth = -1
        max_queue_size = 0
        d_p = []  # creating it for the graph
        while queue:  # iterating until there is something in the queue
            if len(queue) > max_queue_size:  # calculating the max queue size
                max_queue_size = len(queue)
            cost, (parent, current) = queue.pop(0)
            if current in visited_nodes:  # if the node is already visited
                continue
            # to get the graph depth and nodes
            d_p.append((len(parent), len(visited_nodes)))
            depth += 1
            visited_nodes.append(current)
        # checking if the state is goal or not
            if self.is_goal(current):
                print("Goal state!")
                print("Depth: ", len(parent))
                print("Max Queue Size:", max_queue_size)
                print("Expanded Nodes: ", len(visited_nodes))
                print("Result: ", current)
                print("Time to finish: {}".format(end-start))
                return current, d_p
            end = time.time()
        # taking all possible actions of the state
            possible_nodes = self.possible_actions(current)
            temp = []
            parent = parent + [current]
            for node in possible_nodes:
                if algo == 0:  # checking if the algo is ucs
                    h_n = 0  # hardcoded h(n) to zero
                    g_n = self.manhattan(node, self.get_initial_state())
                    print("Expanding: ", current, "g_n:", g_n)
                    temp.append((g_n, node))
                elif algo == 1:  # misplaced A*
                    h_n = self.heuristic(self.get_initial_state(), node)
                    g_n = self.heuristic(node, self.get_goal_state())
                    total = h_n + g_n
                    print("Expanding: ", current,
                          " h(n) = :", h_n, "g(n) = ", g_n)
                    temp.append((total, node))
                elif algo == 2:  # manhattan
                    h_n = self.manhattan(node, self.get_initial_state())
                    g_n = self.manhattan(node, self.get_goal_state())
                    total = h_n + g_n
                    print("Expanding: ", current,
                          " h(n) = :", h_n, "g(n) = ", g_n)
                    temp.append((total, node))
        # all posible actions of the current node
            if temp:
                for i in temp:
                    if i[1] in visited_nodes:  # checking the node is already visited or not
                        continue
                    # keeping the cost, parent, and node itself
                    queue = [(i[0], (parent, i[1]))] + queue
            queue = sorted(queue)  # sorting to take the node with minimum cost
                
if __name__ == '__main__':
    nPuzzle()
