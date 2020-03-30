from random import *
import copy


class Queue:
    """Queue used for breadth-first search."""

    def __init__(self):
        """Attributes for the queue."""
        self.queue = []
        self.length = 0

    def is_empty(self):
        """Check if the Queue is empty."""
        if self.length == 0:
            return True
        else:
            return False

    def push(self, x):
        """Place item at the end of the queue."""
        self.queue.insert(0, x)
        self.length += 1

    def pop(self):
        """Remove item in the front of the queue."""
        if not self.is_empty():
            self.queue.pop()
            self.length -= 1

    def length(self):
        """Return the length of the queue."""
        return self.length

    def peak(self):
        """Returns the item at the front of the queue if not empty."""
        if self.is_empty():
            return None
        else:
            return self.queue[self.length - 1]

    def clear(self):
        """Removes all the items from the queue."""
        self.queue.clear()

    def print_queue(self):
        """Displays queue."""
        for i in self.queue:
            print(i, end="")
        print()


class Matrix:
    """ Used to create a maze in the form of a Matrix. """

    def __init__(self, size, obs):
        """Attributes of a Matrix."""
        self.size = size
        self.start = 1
        self.end = size ** 2
        self.matrix = self.create()
        self.width_of_matrix = len(self.matrix[0])  # Width of matrix.
        self.height_of_matrix = len(self.matrix)  # Height of matrix.
        self.generate_obstacles(obs)

    def create(self):
        """Creates matrix with a given size with each row containing
        elements in ascending order.

        Example:                size = 3

                                [[1, 2, 3],
        Resulting Matrix:        [4, 5, 6],
                                 [7, 8, 9]]"""

        maze_matrix = []
        inner = []
        for i in range(self.start, self.start + self.end):
            inner.append(i)
            if i % self.size == 0:
                maze_matrix.append(inner)
                inner = []
        return copy.deepcopy(maze_matrix)

    def generate_obstacles(self, amount):
        """Calls two functions to generate walls and a border
        around the matrix. These are marked by a #."""
        self.add_walls(amount)
        self.add_border()

    def add_walls(self, quantity):
        """Replaces n number of elements with #."""
        numbers = [x for x in range(2, self.end)]
        for i in range(quantity):
            spot = choice(numbers)
            numbers.remove(spot)
            i = 0
            length = len(self.matrix)
            while i < length:
                if spot in self.matrix[i]:
                    j = self.matrix[i].index(spot)
                    self.matrix[i][j] = WALL
                    break
                i += 1

    def add_border(self):
        """Wraps the matrix with #s.

        Example:
                                [[#, #, #, #, #],
        [[1, 2, 3],              [#, 1, 2, 3, #],
         [4, 5, 6],     -->      [#, 4, 5, 6, #],
         [7, 8, 9]]              [#, 7, 8, 9, #],
                                 [#, #, #, #, #]]"""

        # Insert top and bottom row.
        top_wall = [WALL for _ in range(self.width_of_matrix)]
        bottom_wall = top_wall.copy()
        self.matrix.insert(0, top_wall)
        self.matrix.append(bottom_wall)

        # Insert left and right column.
        for row in self.matrix:
            row.insert(0, WALL)
            row.append(WALL)

        # Increase the height and width length of matrix.
        self.width_of_matrix += 2
        self.height_of_matrix += 2

    def display_maze(self):
        """Displays the maze line by line."""
        for i in self.matrix:
            print(i)


class Graph(Matrix):
    """The graph will be used for the DFS and BFS algorithm to find the path of the maze."""
    graph = {}

    def create_graph(self):
        """Scans through the matrix and places all the nodes and
           their adjacent neighbors in a graph."""
        for row in range(1, self.height_of_matrix - 1):
            for ele in range(1, self.width_of_matrix - 1):
                char = self.matrix[row][ele]
                if char != WALL:
                    right = self.matrix[row][ele + 1]
                    down = self.matrix[row + 1][ele]
                    up = self.matrix[row - 1][ele]
                    left = self.matrix[row][ele - 1]

                    # Remove WALL from list
                    nodes = list(filter(lambda x: x != WALL, [right, down, up, left]))
                    self.graph.update({char: nodes})


class Maze(Graph):
    def __init__(self, size_given, num_of_obs):
        # Size and number of obstacles are send to the Matrix class to design the maze.
        super(Graph, self).__init__(size_given, num_of_obs)
        # Attributes for DFS and DBS.
        self.__visited = []  # Stores the visited nodes of DFS and BDS.
        self.solvable = False  # Changes if the maze is solvable.

    def depth_first_search(self, node, end):
        """ Path finding algorithm implemented recursively with a stack."""
        if self.solvable or node in self.__visited:
            return
        if node == end:
            self.solvable = True
        self.__visited.append(node)
        for loc in self.graph[node]:
            self.depth_first_search(loc, end)

    def breadth_first_search(self, node, end):
        """ Path finding algorithm implemented iteratively using a queue."""
        q = Queue()
        q.push(node)
        self.__visited.append(node)
        for _ in range(len(self.graph)):
            next_node = q.peak()
            if next_node is not None:
                if self.graph[next_node] is not []:
                    for ele in self.graph[next_node]:
                        if ele not in self.__visited:
                            q.push(ele)
                            self.__visited.append(ele)
                            if ele == end:
                                self.solvable = True
                                del q
                                return
                    q.pop()
                else:
                    return
            else:
                return

    def dfs_call(self):
        """Reset solvable boolean, visited list and call DFS function."""
        self.solvable = False
        self.__visited.clear()
        self.depth_first_search(self.start, self.end)

    def bfs_call(self):
        """Reset solvable boolean, visited list and call BFS function."""
        self.solvable = False
        self.__visited.clear()
        self.breadth_first_search(self.start, self.end)

    def visits(self):
        """Returns nodes visited."""
        return self.__visited

    def visits_length(self):
        """Returns length of nodes visited."""
        return len(self.__visited)


WALL = 0
