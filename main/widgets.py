from tkinter import *
from tkinter import filedialog as fd
import customtkinter    # pip install customtkinter
import math
import time
from PIL import Image, ImageTk  # pip install pillow


class Window_Manager:
    """Main class/window of the app. Handles data and how to update certain widgets"""

    def __init__(self, settings, matrix, load_seed_func, save_seed_func):
        self.settings = settings['settings']
        self.seed = matrix
        self.generations = 0
        self.time_played = 0
        self.time_paused = 0
        self.starting_time = time.time()
        self.load_seed_func = load_seed_func
        self.save_seed_func = save_seed_func
        self.desired_width = self.settings['desired_width']/100

        self.root = Tk()    # main window
        self.scale = int(round(
            self.desired_width*self.root.winfo_screenwidth()/self.settings['max_columns']))
        true_width = self.settings['max_columns']*self.scale

        fonts = [   # making universal font styles that scales with desired width
            (f'Arial {int(32*self.desired_width)} bold'),
            (f'Arial {int(32*self.desired_width)}'),
            (f'Arial {int(20*self.desired_width)}'),
            (f'Arial {int(16*self.desired_width)}')
        ]

        colors = [
            self.settings['primary_color'],
            self.settings['secondary_color'],
            self.settings['tertiary_color'],
            self.settings['alive_color']
        ]

        parent = Frame(self.root, bg=colors[0])
        child = Frame(parent, bg=colors[0])
        parent.pack(expand=True)
        child.place(relx=.5, rely=.5, anchor=CENTER)
        
        self.grid_matrix = Grid(
            parent, self.settings['max_rows'], self.settings['max_columns'], matrix, colors, self.scale)
        self.grid_matrix.canvas.grid(columnspan=2)

        self.controls = Controls(parent, true_width, self.settings['play_button_image'], self.save_load_seed, self.settings['max_rows'],
                                 self.settings['max_columns'], self.settings['minimum_rows'], self.settings['minimum_columns'], fonts, colors)
        self.controls.parent_frame.grid(row=1, column=0, sticky='nsw')
        self.controls.parent_frame.grid_propagate(0)

        self.stats = Stats(parent, true_width, fonts, colors)
        self.stats.parent_frame.grid(row=1, column=1, sticky='nse')
        self.stats.parent_frame.grid_propagate(0)

        self.root.title("Conway's game of life in Python!")
        self.root.configure(bg=colors[0])
        self.root.update()
        self.root.minsize(self.root.winfo_width(), self.root.winfo_height())

        self.tick() # start tick function that will check relevant controls

        self.root.mainloop()

    def save_load_seed(self, answer):
        """Function that can communicate to data.py and save/load matrix's"""
        if answer == True:
            self.controls.play == False
            file = str(fd.asksaveasfilename(title="Create a save", defaultextension='.csv', filetypes=[
                       ('CSV Files', '*.csv')])).split('/')
            self.save_seed_func(
                file=file[-1], matrix=self.grid_matrix.display_matrix)

        elif answer == False:
            self.controls.play == False
            file = fd.askopenfilename(title="Load a save", defaultextension='.csv', filetypes=[
                                      ('CSV Files', '*.csv')]).split('/')
            seed = self.load_seed_func(file=file[-1])
            rows, columns = len(seed), len(seed[0])

            self.controls.row_controls.interger_var.set(rows)
            self.controls.column_controls.interger_var.set(columns)
            self.grid_matrix.new_sizes = [rows, columns]

            self.grid_matrix.display_matrix = seed
            self.generations = 0
            self.time_played = 0
            self.time_paused = 0
            self.starting_time = time.time()

    def tick(self):
        """Function that goes over every control and updates the grid/stats accordinly"""
        self.grid_matrix.new_sizes = [int(self.controls.row_controls.interger_var.get(
                            )), int(self.controls.column_controls.interger_var.get())]
        self.grid_matrix.draw = self.controls.draw

        if self.controls.play == True:
            self.time_played = (
                time.time() - self.starting_time) - self.time_paused
            self.generations += 1
            self.grid_matrix.update_grid(self.grid_matrix.display_matrix)
        else:
            self.time_paused = (
                time.time() - self.starting_time) - self.time_played
            self.grid_matrix.update_display(self.grid_matrix.display_matrix)

        self.stats.tiles_alive_box.update_value(self.grid_matrix.alive)
        self.stats.tile_number_box.update_value(int(self.controls.row_controls.interger_var.get(
                                        ))*int(self.controls.column_controls.interger_var.get()))
        self.stats.generations_box.update_value(self.generations)
        self.stats.time_simulated_box.update_value(self.time_played)

        self.root.after(
            1+(self.controls.speed_controls.interger_var.get()*1000), self.tick)


class Grid:
    """Canvas where the grid sits"""

    def __init__(self, root, rows, columns, matrix, colors, scale):
        self.rows = rows
        self.root = root
        self.columns = columns
        self.colors = colors
        self.scale = scale
        self.new_scale = scale
        self.draw = True
        self.x_offset = 0
        self.y_offset = 0
        self.new_sizes = [rows, columns]
        self.canvas = Canvas(root, width=self.scale*self.columns, height=self.scale*self.rows,
                             bg='#111111', highlightbackground='#111111', borderwidth=0, highlightthickness=0)
        self.canvas.bind('<Button-1>', self.canvas_on_click)
        self.canvas.bind('<B1-Motion>', self.canvas_on_click_hold)
        self.previous_id = -1
        self.alive = 0
        self.display_matrix = self.build_display(matrix)    # build the initial matrix
        self.neighbours = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1)
        ]

    def build_display(self, data_matrix):
        """Constructs the initial grid"""
        matrix = []
        self.alive = 0
        for y in range(self.new_sizes[0]):
            row = []
            for x in range(self.new_sizes[1]):
                top_left_x = x * self.scale  # create 4 points in which the rectangle sits in
                bottom_right_x = x * self.scale + self.scale
                top_left_y = y * self.scale
                bottom_right_y = y * self.scale + self.scale
                if int(data_matrix[y][x]) == 0:
                    self.canvas.create_rectangle(
                        top_left_x, top_left_y, bottom_right_x, bottom_right_y, fill='#141414', width=1, outline='#111111')
                    row.append(0)
                else:
                    self.canvas.create_rectangle(
                        top_left_x, top_left_y, bottom_right_x, bottom_right_y, fill='#099B4F', width=1, outline='#111111')
                    row.append(1)
                    self.alive += 1
            matrix.append(row)
        return matrix

    def on_click_calculations(self, coordinates):
        """Finds out which tile the user has clicked on"""
        clicked_box = ((math.ceil((coordinates.x-self.x_offset)/self.new_scale)),
                       math.ceil(((coordinates.y-self.y_offset)/self.new_scale)))
        id = ((clicked_box[1]-1)*self.columns) + clicked_box[0]
        if clicked_box[0] > self.new_sizes[1] or clicked_box[1] > self.new_sizes[0]:
            id = 0  # change nothing if the clicked box is out of set bounds
        return[clicked_box, id]

    def canvas_on_click(self, event):
        """If the user clicks a box, change it's state"""
        if self.draw == True:
            event_info = self.on_click_calculations(event)
            if self.display_matrix[event_info[0][1]-1][event_info[0][0]-1] == 0:
                self.canvas.itemconfigure(event_info[1], fill=self.colors[3])
                self.display_matrix[event_info[0][1]-1][event_info[0][0]-1] = 1
                self.alive += 1
            elif self.display_matrix[event_info[0][1]-1][event_info[0][0]-1] == 1:
                self.canvas.itemconfigure(event_info[1], fill=self.colors[1])
                self.display_matrix[event_info[0][1]-1][event_info[0][0]-1] = 0
                self.alive -= 1
            self.previous_id = event_info[1]

    def canvas_on_click_hold(self, event):
        """If the user clicks and holds and box, change corresponding tile states"""
        if self.draw == True:
            event_info = self.on_click_calculations(event)
            if self.display_matrix[event_info[0][1]-1][event_info[0][0]-1] == 0 and self.previous_id != event_info[1]:
                # if the box is not the same as the one being clicked and held on
                self.canvas.itemconfigure(event_info[1], fill=self.colors[3])
                self.display_matrix[event_info[0][1]-1][event_info[0][0]-1] = 1
                self.alive += 1
            elif self.display_matrix[event_info[0][1]-1][event_info[0][0]-1] == 1 and self.previous_id != event_info[1]:
                self.canvas.itemconfigure(event_info[1], fill=self.colors[1])
                self.display_matrix[event_info[0][1]-1][event_info[0][0]-1] = 0
                self.alive -= 1
            self.previous_id = event_info[1]

    def update_grid(self, old_matrix):
        """Changes the displayed grid visuals and data matrix"""
        new_matrix = []
        id = 0
        self.alive = 0

        x_percent = self.columns / self.new_sizes[1]
        y_percent = self.rows / self.new_sizes[0]

        if y_percent < x_percent:   # if there is less rows missing than columns...
            self.new_scale = self.scale * y_percent
        else:
            self.new_scale = self.scale * x_percent

        self.x_offset = ((self.columns*self.scale) -
                         (self.new_sizes[1]*self.new_scale))/2
        self.y_offset = ((self.rows*self.scale) -
                         (self.new_sizes[0]*self.new_scale))/2

        if x_percent > y_percent:
            self.y_offset = 0
        elif y_percent > x_percent:
            self.x_offset = 0
        else:
            self.x_offset = 0
            self.y_offset = 0

        for y in range(self.rows):
            row = []
            for x in range(self.columns):
                id += 1

                top_left_x = (x * self.new_scale) + self.x_offset
                bottom_right_x = (x * self.new_scale +
                                  self.new_scale) + self.x_offset
                top_left_y = (y * self.new_scale) + self.y_offset
                bottom_right_y = (y * self.new_scale +
                                  self.new_scale) + self.y_offset

                if y < self.new_sizes[0] and x < self.new_sizes[1]:
                    neighbours = self.neighbour_count(x, y)
                    if old_matrix[y][x] == 1:
                            self.alive += 1
                    if old_matrix[y][x] == 1 and (neighbours < 2 or neighbours > 3):
                        self.canvas.itemconfigure(id, fill=self.colors[1])
                        row.append(0)
                    elif old_matrix[y][x] == 0 and neighbours == 3:
                        self.canvas.itemconfigure(id, fill=self.colors[3])
                        row.append(1)
                    else:
                        row.append(old_matrix[y][x])
                    self.canvas.coords(
                        id, top_left_x, top_left_y, bottom_right_x, bottom_right_y)
                else:
                    self.canvas.coords(id, 0, 0, 0, 0)  # hide the box
                    self.canvas.itemconfigure(id, fill=self.colors[1])
                    row.append(0)
            new_matrix.append(row)
        self.display_matrix = new_matrix

    def update_display(self, matrix):
        """Changes the grid without changing the matrix (used for when simulation is paused)"""
        id = 0

        x_percent = self.columns / self.new_sizes[1]
        y_percent = self.rows / self.new_sizes[0]

        if y_percent < x_percent:
            self.new_scale = self.scale * y_percent
        else:
            self.new_scale = self.scale * x_percent

        self.x_offset = ((self.columns*self.scale) -
                         (self.new_sizes[1]*self.new_scale))/2
        self.y_offset = ((self.rows*self.scale) -
                         (self.new_sizes[0]*self.new_scale))/2

        if x_percent > y_percent:
            self.y_offset = 0
        elif y_percent > x_percent:
            self.x_offset = 0
        else:
            self.x_offset = 0
            self.y_offset = 0

        for y in range(self.rows):
            for x in range(self.columns):
                id += 1

                top_left_x = (x * self.new_scale) + self.x_offset
                bottom_right_x = (x * self.new_scale +
                                  self.new_scale) + self.x_offset
                top_left_y = (y * self.new_scale) + self.y_offset
                bottom_right_y = (y * self.new_scale +
                                  self.new_scale) + self.y_offset

                if y < self.new_sizes[0] and x < self.new_sizes[1]:
                    if matrix[y][x] == 1:
                        self.canvas.itemconfigure(id, fill=self.colors[3])
                    else:
                        self.canvas.itemconfigure(id, fill=self.colors[1])
                    self.canvas.coords(
                        id, top_left_x, top_left_y, bottom_right_x, bottom_right_y)
                else:
                    self.canvas.coords(id, 0, 0, 0, 0)  # hide the box
                    self.canvas.itemconfigure(id, fill=self.colors[1])

    def neighbour_count(self, x, y):
        """Counts how many neighbours each tile has"""
        return sum(self.display_matrix[(y+j) % self.new_sizes[0]][(x+i)\
            % self.new_sizes[1]] for (i, j) in self.neighbours) # looks at every adjacent tile and returns their sum


class Controls:
    """Frame where all controls sit inside"""

    def __init__(self, root, true_width, image_directory, file_callback, max_rows, max_columns, minimum_columns, minimum_rows, fonts, colors):
        self.parent_frame = LabelFrame(root, text='Controls', font=fonts[0], bg=colors[0], fg=colors[2], width=int(
            round(true_width*0.69)), height=int(round(true_width*0.12)))
        paddings = {'padx': 15, 'pady': 15}
        self.play = False
        self.draw = True
        play_image = Image.open(image_directory)    # opens play image
        play_image = ImageTk.PhotoImage(play_image.resize((50, 50)))    # resizes play image to put in button

        buttons_frame = Frame(self.parent_frame, bg=colors[0])
        customtkinter.CTkButton(buttons_frame, text='Load seed',
                                text_font=fonts[3], command=lambda: file_callback(False)).grid(**paddings)
        customtkinter.CTkButton(buttons_frame, text='Save seed', text_font=fonts[3], command=lambda: file_callback(
            True)).grid(row=0, column=1, **paddings)
        customtkinter.CTkButton(buttons_frame, text='Draw mode', text_font=fonts[3], command=lambda: self.toggle_draw(
        )).grid(row=0, column=2, **paddings)
        customtkinter.CTkButton(buttons_frame, text='Help!', text_font=fonts[3], command=lambda: Help_Popup(
            width=true_width, fonts=fonts, primary_color=colors[0], secondary_color=colors[2])).grid(row=0, column=3, **paddings)
        buttons_frame.grid(row=0)

        slider_frame = Frame(self.parent_frame, bg=colors[0])

        # makes slider groups using template
        self.row_controls = Sliders(root=slider_frame, text='Rows', fonts=fonts, from_=minimum_rows, to=max_rows,
                                    steps=max_rows-minimum_rows, primary_color=colors[0], secondary_color=colors[2], default=max_rows)
        self.column_controls = Sliders(root=slider_frame, text='Columns', fonts=fonts, from_=minimum_columns, to=max_columns, steps=max_columns -
                                       minimum_columns, primary_color=colors[0], secondary_color=colors[2], default=max_columns, custom_grid={'row': 0, 'column': 1})
        self.speed_controls = Sliders(root=slider_frame, text='Delay (s)', fonts=fonts, from_=0, to=5, steps=5,
                                      primary_color=colors[0], secondary_color=colors[2], default=0, custom_grid={'row': 0, 'column': 2})

        play_button = customtkinter.CTkButton(
            self.parent_frame, text='', bg=colors[0], image=play_image, width=100, height=100, command=lambda: self.set_play())
        play_button.grid(row=0, column=1, rowspan=2, sticky='e')

        slider_frame.grid(row=1)

    def set_play(self):
        """Changes the play variable when the play button is pressed"""
        self.play ^= True   # toggles between true/false

    def toggle_draw(self):
        """Changes the draw variable when the draw mode button is pressed"""
        self.draw ^= True


class Stats(Window_Manager):
    """Frame where all stats sit inside"""

    def __init__(self, root, true_width, fonts, colors):
        self.parent_frame = LabelFrame(root, text='Stats', font=fonts[0], bg=colors[0], fg=colors[2], width=int(
            round(true_width*0.29)), height=int(round(true_width*0.12)))
        
        # makes stat boxes using templates
        self.tiles_alive_box = Stat_Display(self.parent_frame, stat='Tiles alive:', stat_value=0, fonts=fonts,
                                            primary_color=colors[0], secondary_color=colors[2], custom_grid={'row': 0, 'column': 0}, width=(true_width*0.29)*0.4)
        self.tile_number_box = Stat_Display(self.parent_frame, stat='Number of tiles:', stat_value=0, fonts=fonts,
                                            primary_color=colors[0], secondary_color=colors[2], custom_grid={'row': 0, 'column': 1}, width=(true_width*0.29)*0.4)
        self.time_simulated_box = Stat_Display(self.parent_frame, stat='Time simulated (s):', stat_value=0, fonts=fonts,
                                               primary_color=colors[0], secondary_color=colors[2], custom_grid={'row': 1, 'column': 0}, width=(true_width*0.29)*0.4)
        self.generations_box = Stat_Display(self.parent_frame, stat='Generations:', stat_value=0, fonts=fonts,
                                            primary_color=colors[0], secondary_color=colors[2], custom_grid={'row': 1, 'column': 1}, width=(true_width*0.29)*0.4)


class Help_Popup:
    """Popup that appears when the help button appears"""

    root = None

    def __init__(self, fonts, width, primary_color=None, secondary_color=None):
        self.top = Toplevel(Help_Popup.root)
        self.top.title('Help guide')    # puts popup ontop of main window
        self.top.maxsize(round(width*.4), round(width*.5))
        self.top.minsize(round(width*.4), round(width*.5))
        self.top.configure(bg=primary_color)

        Label(self.top, bg=primary_color, fg=secondary_color, text='Help guide',
              font=fonts[1]).grid(row=0, column=0, pady=7, padx=15, sticky='w')
        Label(self.top, bg=primary_color, fg=secondary_color, text="Hello and welcome to the help guide!\n\nConway's game of life is populated by cells on a matrix that follow these rules:\n1. If the cell is alive, then it stays alive if it has either 2 or 3 live neighbor\n2. If the cell is dead, then it springs to life only in the case that it has 3 live neighbors\n\nCheck out settings.json to see changeable settings!",
              font=fonts[2], justify='left', wraplength=width*.35).grid(row=1, column=0, pady=15, padx=15, sticky='w')

        Label(self.top, bg=primary_color, fg=secondary_color, text='FAQ',
              font=fonts[1]).grid(row=2, column=0, pady=7, padx=15, sticky='w')
        Label(self.top, bg=primary_color, fg=secondary_color, text="Q: I tried entering in a big number into an entry box, and it turned into a diffrent number, why?\nA: Since the program has it's limits, it'll detect when you're trying to go over the limit and deny your input, and change it to the limit/maximum value.\n\nQ: Same as before but with smaller numbers, or when you delete all numbers '4' is still there or the minimum number.\nA: Again, the program notices you're entering a number smaller than the minimum and automatically corrects this. If you would like to enter a doubled igit number, please use the slider to get within a close range of the desired number and tune from there.\n\nQ: What is the purpose of this program?\nA: This program was made for a school project which is meant to target teenagers interested in math or games. It's goal is to entertain people with interesting patterns and changing tiles. The bigger goal is to get people into tech so that they can build an app like this :)",
              font=fonts[2], justify='left', wraplength=width*.35).grid(row=3, column=0, pady=15, padx=15, sticky='w')

        customtkinter.CTkButton(self.top, text='Close', text_font=fonts[2], command=lambda: self.top.destroy(
        )).grid(row=4, column=0, pady=15, sticky='e')


class Sliders:
    """Slider template with all nessecary widgets and variables"""

    def __init__(self, root, text=None, fonts=None, from_=None, to=None, steps=None, primary_color=None, secondary_color=None, custom_grid=None, default=None):
        self.interger_var = IntVar()
        self.interger_var.set(default)
        paddings = {'padx': 15, 'pady': 15}
        self.to = to

        frame = customtkinter.CTkFrame(root, fg_color=primary_color)
        Label(frame, text=text, font=fonts[3], bg=primary_color, fg=secondary_color).grid(
            sticky='nsw')

        self.entry = customtkinter.CTkEntry(frame, width=40, textvariable=self.interger_var,
                                            text_font=fonts[3], bg_color=primary_color, text_color=secondary_color)
        self.entry.grid(row=0, column=1, sticky='nse')

        customtkinter.CTkSlider(frame, from_=from_, to=to, number_of_steps=steps, bg_color=primary_color,
                                command=lambda x: self.command(x), variable=self.interger_var).grid(row=1, column=0, columnspan=2)

        self.interger_var.trace("w", lambda x, y, z, entry=self.entry,
                                sv=self.interger_var: self.callback(entry, sv))

        try:    # if custom_grid is inputted properly then use it otherwise ignore
            frame.grid(**custom_grid, **paddings)
        except:
            frame.grid(**paddings)

    def command(self, value):
        """Command to change the interger variable"""
        self.interger_var.set(int(value))
        self.entry.configure()

    def callback(self, entry, sv):
        """Callback function for the entry box"""
        if len(entry.get()) >= 1:
            if entry.get()[-1].isnumeric() == False:
                entry.delete((len(entry.get())-1), END)
        else:   # don't want to leave the IntVar() as blank as it will cause an error with the slider
            entry.insert(0, 0)
        if len(entry.get()) >= 2:
            if entry.get()[0] == '0':
                entry.delete(0, 1)
        if int(sv.get()) >= self.to:    # if greater than maximum set to maximum
            entry.delete(0, END)
            entry.insert(0, str(self.to))


class Stat_Display:
    """Box template that shows a variable and then it's value"""

    def __init__(self, root, stat=None, stat_value=None, fonts=None, primary_color=None, secondary_color=None, custom_grid=None, width=None):
        frame_paddings = {'padx': 15, 'pady': 15}
        label_paddings = {'padx': 5, 'pady': 5}

        frame = customtkinter.CTkFrame(root, fg_color=primary_color, height=width/4,
                                       width=width, border_width=2, border_color=secondary_color, corner_radius=1)
        frame.pack_propagate(0)

        Label(frame, text=stat, font=fonts[3], bg=primary_color, fg=secondary_color).pack(
            **label_paddings, side='left')
        self.stat_value = Label(frame, text=str(
            round(stat_value)), font=fonts[3], bg=primary_color, fg=secondary_color)
        self.stat_value.pack(**label_paddings, side='right')

        try:    # if custom_grid is inputted properly then use it otherwise ignore
            frame.grid(**custom_grid, **frame_paddings)
        except:
            frame.grid(**frame_paddings)

    def update_value(self, new_value):
        """Function that gets the new value ready to be displayed on the stat label"""
        self.stat_value.configure(text=str(round(new_value)))


if __name__ == '__main__':
    print('Wrong file selected, please run "main.py" instead')
