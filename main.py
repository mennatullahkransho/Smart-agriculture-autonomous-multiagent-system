import tkinter as tk



class AnimationGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.canvas = None
        self.ball = None
        self.direction_x = 1
        self.direction_y = 1
        self.positions = [(50, 50, 100, 100, 'red'),
                          (150, 100, 200, 150, 'blue'),
                          (250, 50, 300, 100, 'green'),
                          (150, 0, 200, 50, 'yellow'),
                          (100, 75, 150, 125, 'orange')]
        self.current_position = 0
        self.master = master
        self.grid()
        self.create_widgets()
        self.animate()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=400, height=300)
        self.canvas.grid(row=0, column=0)
        self.ball = self.canvas.create_oval(*self.positions[self.current_position][0:4], fill=self.positions[self.current_position][4])

    def animate(self):
        if not self.canvas:
            return

        x1, y1, x2, y2 = self.canvas.coords(self.ball)
        if x2 >= self.canvas.winfo_width():
            self.direction_x = -1
        elif x1 <= 0:
            self.direction_x = 1
        if y2 >= self.canvas.winfo_height():
            self.direction_y = -1
        elif y1 <= 0:
            self.direction_y = 1

        self.current_position += 1
        if self.current_position >= len(self.positions):
            self.current_position = 0

        self.canvas.delete(self.ball)
        self.ball = self.canvas.create_oval(*self.positions[self.current_position][0:4], fill=self.positions[self.current_position][4])

        x_move = 10 * self.direction_x
        y_move = 10 * self.direction_y
        self.canvas.move(self.ball, x_move, y_move)

        self.after(100, self.animate)


root = tk.Tk()
root.title("Animation Example")
animation_gui = AnimationGUI(master=root)
animation_gui.mainloop()
class NodeGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.l1_water_level = None
        self.l2_water_level = None
        self.l3_water_level = None
        self.l4_water_level = None
        self.l2_entry = None
        self.l3_entry = None
        self.l1_entry = None
        self.master = master
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Smart Agriculture ", font=("Arial", 14), width=20, height=2).grid(row=0, column=0)
        tk.Label(self, text="L1 water level: ", font=("Arial", 13), width=15, height=2).grid(row=1, column=0)
        tk.Label(self, text="L2 water level: ", font=("Arial", 13), width=15, height=2).grid(row=2, column=0)
        tk.Label(self, text="L3 water level: ", font=("Arial", 13), width=15, height=2).grid(row=3, column=0)
        tk.Label(self, text="L4 water level: ", font=("Arial", 13), width=15, height=2).grid(row=4, column=0)

        self.l1_entry = tk.Entry(self, width=50)
        self.l1_entry.grid(row=1, column=1)

        self.l2_entry = tk.Entry(self, width=50)
        self.l2_entry.grid(row=2, column=1)

        self.l3_entry = tk.Entry(self, width=50)
        self.l3_entry.grid(row=3, column=1)

        self.l4_entry = tk.Entry(self, width=50)
        self.l4_entry.grid(row=4, column=1)

        self.submit_button = tk.Button(self, text="Submit", command=self.submit, width=10, height=2)
        self.submit_button.grid(row=5, column=1)

    def submit(self):
        self.l1_water_level = int(self.l1_entry.get())
        self.l2_water_level = int(self.l2_entry.get())
        self.l3_water_level = int(self.l3_entry.get())
        self.l4_water_level = int(self.l4_entry.get())
        self.master.quit()


class OutputGUI(tk.Frame):
    def __init__(self, master=None, cost=None, path=None):
        super().__init__(master)
        self.cost = cost
        self.path = path
        self.master = master
        self.grid()
        self.create_widgets()

    def create_widgets(self):

        tk.Label(self, text="Total minimum cost: {}".format(self.cost), font=("Arial", 14), width=20).grid(row=0,
                                                                                                           column=0)

        tk.Label(self, text="Path:", font=("Arial", 14), width=20).grid(row=1, column=0)

        for i, node in enumerate(self.path):
            tk.Label(self, text=node.name, font=("Arial", 12), width=15).grid(row=i + 2, column=0)

        tk.Button(self, text="Close", command=self.master.destroy, width=10).grid(row=len(self.path) + 2, column=0)


root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.title("Smart Agriculture")
window_width = 800
window_height = 600
x_coordinate = (screen_width / 2) - (window_width / 2)
y_coordinate = (screen_height / 2) - (window_height / 2)
root.geometry('%dx%d+%d+%d' % (window_width, window_height, x_coordinate, y_coordinate))

node_gui = NodeGUI(master=root)
node_gui.mainloop()


class Node:
    def __init__(self, x, y, name, water_level, id):
        self.x = x
        self.y = y
        self.water_level = water_level
        self.name = name
        self.id = id
        self.neighbors = []

    def add_edge(self, neighbor, cost):
        self.neighbors.append((neighbor, cost))

    def heuristic(self, goal_node):
        return abs(self.x - goal_node.x) + abs(self.y - goal_node.y)

    def f_n(self, cost, goal_node):
        return cost + self.heuristic(goal_node)


class Graph:
    def __init__(self):
        self.nodes = []
        self.start_node = None
        self.goal_node = None

    def add_node(self, node):
        self.nodes.append(node)


def a_star_search(goal_node, unvisited, node, count):
    path = []
    cost = 0
    epochs = 1000
    node = None
    size = len(unvisited)
    for I in range(epochs):
        min = 10000
        inc = 0
        if unvisited[0].id == '0':  # L0 doesn't want to be irrigated or not then I add it directly in the path
            path.append(unvisited[0])
            node = unvisited[0]
            del unvisited[0]
        else:
            for neighbor, neighbor_cost in node.neighbors:
                if path.count(neighbor) > 0:
                    continue
                else:
                    cost += neighbor_cost
                    if neighbor.f_n(cost, goal_node) < min and neighbor.id != '5' and count < 4:
                        min = neighbor.f_n(cost, goal_node)
                        node2 = neighbor
                        cost -= neighbor_cost
                        inc = neighbor_cost
                    elif neighbor.f_n(cost, goal_node) >= min and count < 4:
                        cost -= neighbor_cost

            node = node2
            if node.water_level < irrigation_threshold and path.count(node.name) == 0 and count < 4:
                cost += inc
                count += 1
                print('Visiting Node: ', node.name)
                path.append(node2)
                print('irrigating node: ', node.name)
                node.water_level += (irrigation_threshold - node.water_level)
            elif path.count(node) == 0 and count < 4:
                count += 1
                print('Visiting Node: ', node.name)
                cost += inc
                path.append(node2)
                print('No need to irrigate node: ', node.name)
            elif count == 4:
                path.append(goal_node)
                break
            for I in range(0, len(unvisited)):
                if unvisited[I] == node2:
                    size -= 1
                    del unvisited[I]
                    break
        if size == 1:
            del unvisited[0]
            break
    return path


irrigation_threshold = 60  # reference for the water level of the node
# input the water levels of the nodes
# create nodes using the input values
i = Node(0, 0, 'Initial Node', 0, '0')
L1 = Node(1, 1, 'L1', node_gui.l1_water_level, '1')
L2 = Node(1, 2, 'L2', node_gui.l2_water_level, '2')
L3 = Node(2, 2, 'L3', node_gui.l3_water_level, '3')
L4 = Node(2, 1, 'L4', node_gui.l4_water_level, '4')
goal_node = Node(3, 3, 'goal Node', 0, '5')

# adding the edges between nodes
i.add_edge(L1, 1)
i.add_edge(L2, 4)
i.add_edge(L3, 7)
i.add_edge(L4, 2)

L1.add_edge(L2, 2)
L1.add_edge(L3, 8)
L1.add_edge(L4, 7)
L1.add_edge(goal_node, 1)

L2.add_edge(L1, 2)
L2.add_edge(L3, 5)
L2.add_edge(L4, 6)
L2.add_edge(goal_node, 4)

L3.add_edge(L1, 8)
L3.add_edge(L2, 5)
L3.add_edge(L4, 3)
L3.add_edge(goal_node, 7)

L4.add_edge(L1, 7)
L4.add_edge(L2, 6)
L4.add_edge(L3, 3)
L4.add_edge(goal_node, 2)

# create graph and add nodes
graph = Graph()
graph.add_node(i)
graph.add_node(L1)
graph.add_node(L2)
graph.add_node(L3)
graph.add_node(L4)
graph.add_node(goal_node)

# define starting node and unvisited nodes
graph.nodes = [i, L1, L2, L3, L4, goal_node]
start_node = i
unvisited_nodes = [i, L1, L2, L3, L4, goal_node]
path = a_star_search(goal_node=goal_node, unvisited=unvisited_nodes, node=start_node, count=0)

print('path: ')
for node in path:
    print(node.name)


def cal_cost(path, cost=0):
    for i in range(len(path) - 1):
        for neighbor, neighbor_cost in path[i].neighbors:
            if neighbor == path[i + 1]:
                cost += neighbor_cost
                break

    return cost


cost = cal_cost(path=path)
print('total minimum cost= ', cost)

output_gui = OutputGUI(master=root, cost=cost, path=path)
output_gui.mainloop()
# -------------------------------------------------------------------------------------------
# Define the path
path = [(50, 50), (100, 50), (150, 100), (100, 150), (50, 150)]


# Define the function to move the robot through the path
def move_robot(canvas, path):
    for i in range(len(path)):
        if i == 0:
            x1, y1 = path[i]
        else:
            x1, y1 = path[i - 1]
        x2, y2 = path[i]
        canvas.create_line(x1, y1, x2, y2, fill='red', width=3)
        canvas.create_oval(x2 - 5, y2 - 5, x2 + 5, y2 + 5, fill='blue')
        canvas.update()
        canvas.after(1000)

    # Return the robot to the initial node
    x1, y1 = path[-1]
    x2, y2 = path[0]
    canvas.create_line(x1, y1, x2, y2, fill='red', width=3)
    canvas.create_oval(x2 - 5, y2 - 5, x2 + 5, y2 + 5, fill='blue')
    canvas.update()
    canvas.after(1000)

# Define the GUI function
def gui_function():
    # Create the main window
    root = tk.Tk()
    root.title('Robot Movement')
    # Create the canvas for drawing the path and the robot
    canvas = tk.Canvas(root, width=400, height=300)
    canvas.pack()
    # Call the function to move the robot through the path
    move_robot(canvas, path)
    # Start the main event loop
    root.mainloop()
# Call the GUI function
gui_function()
def animate_agent():
    # Define the locations of the room
    room = {
        'i': (50, 50), # initial location
        'L1': (150, 50),
        'L2': (150, 150),
        'L3': (50, 150),
        'L4': (100, 100) # central location
    }
    
    # Define the path for the agent to follow
    path = ['L1', 'L2', 'L3', 'L4', 'i']
    
    # Create a new GUI window
    root = tk.Tk()
    root.title("Garden Room Animation")
    
    # Set the canvas size
    canvas_width = 200
    canvas_height = 200
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()
    
    # Draw the room as a green house
    canvas.create_rectangle(0, 0, canvas_width, canvas_height, fill='green')
    canvas.create_oval(25, 25, 175, 175, outline='white', width=5)
    
    # Draw the locations as circles
    for loc, pos in room.items():
        x, y = pos
        canvas.create_oval(x-10, y-10, x+10, y+10, fill='white', outline='black', width=2)
        canvas.create_text(x, y-20, text=loc)
    
    # Draw the agent as a red dot
    agent = canvas.create_oval(room['i'][0]-5, room['i'][1]-5, room['i'][0]+5, room['i'][1]+5, fill='red')
    
    # Define a function to move the agent to a new location
    def move_agent(loc):
        x, y = room[loc]
        canvas.coords(agent, x-5, y-5, x+5, y+5)
        canvas.update()
    
    # Move the agent along the path
    for loc in path:
        move_agent(loc)
        root.after(1000) # pause for 1 second between movements
    
    # Close the GUI window when finished
    root.mainloop()
print(animate_agent())
