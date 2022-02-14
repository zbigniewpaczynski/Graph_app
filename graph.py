import tkinter as tk 
 
cnt = 0
 
class Dot: 
    def __init__(self, graph, x, y): 
        global cnt
        cnt += 1 
        self.x = x 
        self.y = y
        self.id = cnt
        self.oval_id = graph.canvas.create_oval(x + 25, y + 25, x - 25, y - 25, fill = 'blue', tags = ("clickable",))
        self.text_id = graph.canvas.create_text(x, y, text = cnt, fill = 'white')
        graph.canvas.update()

 
class Graph:
    def __init__(self): 
        self.window = tk.Tk() 

        self.canvas = tk.Canvas(self.window, bg = 'white', highlightthickness = 0) 
        self.canvas.pack(fill = tk.BOTH, expand = True) 

        self.prev_dot = 0
        self.matrix = []
        self.dots = [] 
 
        self.canvas.bind("<Button-1>", self.click_action) 

        self.button = tk.Button(self.canvas, text = "Save matrix", command = self.matrix_drop)
        self.button.pack()
        self.window.mainloop() 


    def matrix_drop(self):
        file = open('graph.txt', 'w')
        for i in self.matrix:
            file.writelines(' '.join(list(map(str, i))) + '\n')


    def find_coords(self, item):
        coords = ()
        if item:
            coords = self.canvas.coords(item)
            coords = (coords[0] + 25, coords[1] + 25)
        return coords


    def dot_find(self, id):
        for i in self.dots:
            if i.oval_id == id:
                return i.id


    def click_action(self, event): 
        x, y = event.x, event.y
        items = list(self.canvas.find_overlapping(event.x + 1, event.y + 1, event.x - 1, event.y - 1))
        if items:
            item = int(items[0])
            coords_1 = self.find_coords(item)
            tags = self.canvas.itemcget(item, "tags")
            current_color = self.canvas.itemcget(item, 'fill')
            if "clickable" in tags:
                if self.prev_dot == 0:
                    if current_color == 'blue':
                        self.canvas.itemconfig(item, fill = 'green')
                        self.prev_dot = item
                elif item != self.prev_dot:
                    first = self.dot_find(item) - 1
                    second = self.dot_find(self.prev_dot) - 1
                    self.canvas.itemconfig(self.prev_dot, fill = 'blue')
                    coords_2 = self.find_coords(self.prev_dot)
                    tag = self.canvas.create_line(coords_1[0], coords_1[1], coords_2[0], coords_2[1], width = 5)
                    self.canvas.tag_lower(tag)
                    self.matrix[first][second] = self.matrix[second][first] = 1
                    self.prev_dot = 0
                else:
                    self.canvas.itemconfig(item, fill = 'blue')
                    self.prev_dot = 0
        else:
            self.dots.append(Dot(self, x, y))
            self.matrix.append([])
            for i in range(len(self.matrix)):
                while len(self.matrix[i]) != cnt:
                    self.matrix[i].append(0)

app = Graph()
