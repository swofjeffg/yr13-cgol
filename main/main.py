'''
Conway's game of life! Written for a school project :)

Conway's game of life is populated by cells on a matrix that follow these rules:

1. If the cell is alive, then it stays alive if it has either 2 or 3 live neighbors
2. If the cell is dead, then it springs to life only in the case that it has 3 live neighbors
'''

import data
import widgets

if __name__ == '__main__':
    """Main routine"""
    data_seed_obj = data.Data_Seed()
    widgets.Window_Manager(data.Data_Collector( # opening up window manager with cleaned up data from data
    ).settings, data_seed_obj.seed, data_seed_obj.file_seed, data_seed_obj.save_seed)
