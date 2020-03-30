# AUTHOR: Alexander Joslin
# DATE: March 29th, 2020
# DESCRIPTION:  This is a graphical maze solver
# that uses the depth-first search and
# breadth-first search as its internal algorithms.

from time import sleep
from tkinter import*
import labyrinth


def display_path(color):
    """Draws the path of the maze on the canvas."""
    global x_pos, y_pos, path, path_length

    path = maze.visits()
    path_length = maze.visits_length()

    for step in path:
        x_pos = tracker[step][0]                                    # Retrieves corresponding x-coord of the element.
        y_pos = tracker[step][1]                                    # Retrieves corresponding y-coord of the element.
        can.create_rectangle(x_pos, y_pos,
                             x_pos + SIZE,
                             y_pos + SIZE,
                             fill=color)

        if not SPEED == 0:
            sleep(SPEED)                                            # Slow down the path drawing process.
            window.update()

    # Used to erase the solvable indicator.
    can.create_rectangle(175, 540, 175 + 200,
                         540 + 30, fill="black")
    if maze.solvable:
        can.create_text(285, 551, fill="white",                     # Create text on the canvas.
                        font=("Arial", 18, "normal"),
                        text="Solvable: " +
                        str(path_length) + " steps")
    else:
        can.create_text(285, 551, fill="white",                     # Create text on the canvas.
                        font=("Arial", 18, "normal"),
                        text="Not Solvable")


def make_dfs_path():
    """Called when the DFS button is clicked."""
    global path, path_length
    maze.dfs_call()
    display_path("blue")


def make_bfs_path():
    """Called when the BFS button is clicked."""
    global path, path_length
    maze.bfs_call()
    display_path("green")


def obstacle_options():
    """Returns a list of integers for the user
    to choose how many obstacles they want.
    The number of obstacles depends on maze size."""
    base = 5
    lower_limit = DIM_SQRD * 0.1
    upper_limit = DIM_SQRD * 0.35 + 1
    first = base * round(lower_limit/base)
    last = base * round(upper_limit/base)
    return range(first, last, base)


def dim_dropdown(*args):
    """Retrieves the dimension chosen."""
    global DIMENSION, OBSTACLES, DIM_SQRD, obs_drop
    DIMENSION = dim_var.get()                                       # Retrieves the dimension the user chose.
    DIM_SQRD = DIMENSION**2
    OBSTACLES = int(DIM_SQRD * 0.25)
    dim_drop.config(state=DISABLED)                                 # Disable the dropdown menu for dimension.
    obs_drop.config(state=NORMAL)                                   # Enable the dropdown menu for obstacles.
    obs_choices = obstacle_options()                                # Get List of obstacle choices.
    obs_drop = OptionMenu(left_frame, obs_var,
                          *obs_choices)
    obs_drop.grid(row=1, column=1)                                  # Create new option menu over old one.


def obs_dropdown(*args):
    """Retrieves the number of obstacles the user chose."""
    global OBSTACLES
    dim_drop.config(state=DISABLED)
    OBSTACLES = obs_var.get()


def spd_dropdown(*args):
    """Sets the speed of the maze according to user input."""
    global SPEED
    chosen = spd_var.get()                                          # Retrieves the user's chosen speed.
    if chosen == "Instant":
        SPEED = 0
    elif chosen == "Very Fast":
        SPEED = 0.01
    elif chosen == "Fast":
        SPEED = 0.02
    elif chosen == "Medium":
        SPEED = 0.1
    elif chosen == "Slow":
        SPEED = 0.2
    elif chosen == "Very Slow":
        SPEED = 0.5


def draw_entrance_exit():
    """Draws the entrance and exit of the maze."""
    maze_entrance = LOCATION + 30
    maze_exit = LOCATION + 12
    can.create_text(maze_entrance, maze_exit,                       # Draw the entrance of the maze.
                    fill="white",  text="Enter",
                    font=("Arial", 10, "normal"))

    maze_entrance = DIMENSION * SIZE + LOCATION + 12
    maze_exit = DIMENSION * SIZE + LOCATION + 30
    can.create_text(maze_entrance, maze_exit,                       # Draw the exit of the maze.
                    fill="white", text="Exit",
                    font=("Arial", 10, "normal"))


def center_maze():
    """Returns coordinate to center the maze."""
    global LOCATION
    if DIMENSION == 20:
        LOCATION = 66
    elif DIMENSION == 15:
        LOCATION = 115
    elif DIMENSION == 10:
        LOCATION = 164
    return LOCATION


def start():
    """Displays the graphical maze on the canvas."""
    global maze, x_pos, y_pos

    maze = labyrinth.Maze(DIMENSION, OBSTACLES)                     # Create the maze matrix.
    maze.create_graph()                                             # Create the maze graph.

    x_pos = center_maze()                                           # Retrieve location to center the maze.
    y_pos = x_pos

    # Draw the maze.
    # Black squares are obstacles (walls).
    # White squares are legal moves.
    for row in maze.matrix:
        for element in row:
            if element == labyrinth.WALL:                           # Draws a black square if the element is a wall.
                can.create_rectangle(x_pos, y_pos,
                                     x_pos + SIZE,
                                     y_pos + SIZE,
                                     fill="black")
            else:
                can.create_rectangle(x_pos, y_pos,                  # Draws a black square if the element is a wall.
                                     x_pos + SIZE,
                                     y_pos + SIZE,
                                     fill="white")
                tracker.update({element: (x_pos, y_pos)})
            x_pos += SIZE
        x_pos = LOCATION
        y_pos += SIZE
    start_button.config(state=DISABLED)                             # Disable the start button after it is pressed.
    dfs_button.config(state=NORMAL)                                 # Enable DFS button after the maze is displayed.
    bfs_button.config(state=NORMAL)                                 # Enable BFS button after the maze is displayed.

    draw_entrance_exit()                                            # Draw entrance and exit of the maze


def on_closing():
    """Called when user closes the app."""
    global SPEED
    SPEED = 0
    window.quit()


# Default values for the maze.
# Uppercase to indicate importance not immutability
DIMENSION = 25                                                      # Default dimension if non chosen.
DIM_SQRD = DIMENSION**2                                             # Number of square in matrix.
OBSTACLES = int(DIM_SQRD * 0.25)                                    # Default number of obstacles if non chosen.
SPEED = 0.01                                                        # Default speed if non chosen.
SIZE = 20                                                           # Default square size.
LOCATION = 15                                                       # Default location of the maze.
x_pos = LOCATION                                                    # Default x-coordinate.
y_pos = LOCATION                                                    # Default y-coordinate.

# Initialize values for the maze.
maze = None
path = None
path_length = None
tracker = {}                                                        # Keep track of x and y-coord for each node.


# APP SCREEN.
window = Tk()
window.geometry("570x670+325+0")                                    # Set the size of the app screen.
window.title("Maze Solver")                                         # Set the tittle of the app.


# FRAMES.
top_frame = Frame(window, relief=FLAT)                              # To contain frame1 and frame2.
top_frame.grid(row=0, column=0, pady=5)                             # Place at the top of the window.

left_frame = Frame(top_frame, relief=FLAT)                          # To contain labels and option menus.
left_frame.grid(row=0, column=0, pady=5)                            # Place on the left of the top frame.

center_frame = Frame(top_frame, relief=FLAT)                        # To contain the start button.
center_frame.grid(row=0, column=1, pady=5, padx=5)                  # Place in the center of the top frame.

right_frame = Frame(top_frame, relief=FLAT)                         # To contain DFS & BFS button.
right_frame.grid(row=0, column=2, pady=5, padx=5)                   # Place on the right of the top frame.


# LABELS.
dim_label = Label(left_frame, text="  Size")                        # Create dimension label.
dim_label.grid(row=0, column=0)                                     # Place on the left fo the left frame.

obs_label = Label(left_frame, text="Walls")                         # Create obstacle label.
obs_label.grid(row=1, column=0)                                     # Place on the left of the left frame.

spd_label = Label(left_frame, text="Speed")                         # Create speed label.
spd_label.grid(row=2, column=0)                                     # Place on the left of the left frame.


# OPTION MENUS.
dim_var = IntVar(left_frame)                                        # Declare dimension variable as an integer.
dim_var.set(DIMENSION)                                              # Set the default value.
dim_choices = range(10, 26, 5)
dim_drop = OptionMenu(left_frame, dim_var, *dim_choices)            # Create dimension option menu.
dim_drop.grid(row=0, column=1)                                      # Place on the right of the left frame.
dim_var.trace('r', dim_dropdown)                                    # Link function to change dropdown.

obs_var = IntVar(left_frame)                                        # Declare obstacle variable as an integer.
obs_choices_default = obstacle_options()
obs_drop = OptionMenu(left_frame, obs_var, *obs_choices_default)    # Create obstacle option menu.
obs_drop.grid(row=1, column=1)                                      # Place on the right side of the left frame.
obs_var.trace('w', obs_dropdown)                                    # link function to change dropdown.

spd_var = StringVar(left_frame)                                     # Declare speed variable as an integer.
spd_var.set("Very Fast")                                            # Set the default value.
spd_choice = ["Instant", "Very Fast", "Fast",
              "Medium", "Slow", "Very Slow"]
spd_drop = OptionMenu(left_frame, spd_var, *spd_choice)             # Create speed option menu.
spd_drop.grid(row=2, column=1)                                      # Place on the right side of the left frame.
spd_var.trace('w', spd_dropdown)                                    # link function to change dropdown.


# BUTTONS.
start_button = Button(center_frame, text="Start", command=start,    # Create start button.
                      padx=7, pady=2, fg="green")
start_button.grid(row=0, column=0, padx=10)                         # Place in the center frame.

dfs_button = Button(right_frame, text="Depth-first search",         # Create DFS button.
                    font=("Arial", 14, "normal"), fg="blue",
                    command=make_dfs_path, padx=11, pady=5,
                    state=DISABLED)
dfs_button.grid(row=0, column=0)                                    # Place in the right frame.

bfs_button = Button(right_frame, text="Breadth-first search",       # Create BFS button.
                    font=("Arial", 14, "normal"), fg="green",
                    command=make_bfs_path,
                    padx=5, pady=5, state=DISABLED)
bfs_button.grid(row=1, column=0)                                    # Place in the right frame.


can = Canvas(window, width=565, height=565, bg="black")             # Create canvas.
can.grid(row=1, column=0, pady=5)


window.protocol("WM_DELETE_WINDOW", on_closing)                     # Closing window.
window.mainloop()
