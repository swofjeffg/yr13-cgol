from random import randrange
import pathlib  # pip install pathlib
import json
import csv


PATH = str(pathlib.Path(__file__).parent.resolve()) + \
    '/'  # get the path of this exact python file


class Data_Collector:
    """Collects and validates data from other files"""

    def __init__(self):
        self.settings = self.get_settings()
        self.check_settings()

    def get_settings(self):
        """Attempts to locate 'settings.json', errors if not found"""
        try:
            with open(PATH+'settings.json') as json_file:
                return(json.load(json_file))
        except:
            raise Exception(f"'settings.json' file is missing!\n\
                    Make sure files are placed in the same folder")

    def check_settings(self):
        """Makes sure 'settings.json' has all keys required"""
        expected_settings = [
            'max_columns',
            'max_rows',
            'minimum_columns',
            'minimum_rows',
            'desired_width',
            'seed',
            'primary_color',
            'secondary_color',
            'tertiary_color',
            'alive_color',
            'play_button_image']

        try:    # checking that each setting is present
            for setting in expected_settings:
                self.settings['settings'][setting]
                if setting == 'play_button_image':
                    self.settings['settings'][setting] = PATH + \
                        self.settings['settings'][setting]
        except:
            raise KeyError(f"'{setting}' is missing in 'settings.json'")


class Data_Seed(Data_Collector):
    """Collects seeds from seeds folder"""

    def __init__(self):
        self.settings = super().get_settings()['settings']
        self.seed = self.settings['seed']

        if self.seed == 'from_random' or self.seed == 'random':
            self.seed = self.random_seed()
        else:
            self.seed = self.file_seed(self.seed)

    def random_seed(self):
        """Makes a matrix based on columns and rows in 'settings.json'"""
        matrix = []
        for _ in range(self.settings['max_rows']):
            row = []
            for _ in range(self.settings['max_columns']):
                row.append(randrange(0, 2))
            matrix.append(row)
        return(matrix)

    def file_seed(self, file):
        """Makes a matrix based on the provided csv file"""
        if file[-4:] == '.csv':
            file = file[:-4]
        try:
            with open(PATH+f'seeds/{file}.csv') as csv_seed:
                csv_reader = csv.reader(csv_seed)
                matrix = []
                for row in csv_reader:
                    matrix.append(row)
                    for cell in row:
                        if int(cell) not in range(2):
                            raise ValueError    # if cell is something other than 1 or 0

            if len(matrix[0]) < self.settings['max_columns']:   # cleaning up the seed
                print('Grid doesnt have enough columns! Adding more to the right!')
                missing_columns = self.settings['max_columns'] - len(matrix[0])
                for _ in range(missing_columns):
                    for row in matrix:
                        row.append(0)
            if len(matrix) < self.settings['max_rows']:
                print('Grid doesnt have enough rows! Adding more to the bottom!')
                missing_rows = self.settings['max_rows'] - len(matrix)
                for _ in range(missing_rows):
                    row = [0] * len(matrix[0])
                    matrix.append(row)

            if len(matrix[0]) > self.settings['max_columns']:
                print(
                    'Grid has too many columns! Columns from the right will be removed!')
                for row in matrix:
                    row = row[self.settings['max_columns']:]
            if len(matrix) > self.settings['max_rows']:
                print('Grid has too many rows! Rows from the bottom will be removed!')
                matrix = matrix[self.settings['max_rows']:]

            for y in range(self.settings['max_rows']):
                for x in range(self.settings['max_columns']):
                    matrix[y][x] = int(matrix[y][x])

            return(matrix)
        except:
            raise Exception(
                f"{file} not located or it isn't using accepted format or doesn't exist")

    def save_seed(self, file, matrix):
        """Requires a '.csv' file to store seed information in"""
        if file[-4:] == '.csv':
            file = file[:-4]
        try:
            with open(PATH+f'seeds/{file}.csv', 'w', newline="") as outfile:
                csv_writer = csv.writer(outfile)
                for row in matrix:
                    csv_writer.writerow(row)
        except:
            raise Exception(f"Couldn't create {file}")


if __name__ == '__main__':
    print('Wrong file selected, please run "main.py" instead')
