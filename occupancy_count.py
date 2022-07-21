import logging
import string
from tkinter import *
from tkinter import ttk
import os
import json

global configuration_data
global log_filename


def enable_logging(log_filename='occupancy_count.log'):
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S', filename=log_filename,
                        level=logging.DEBUG)


def display_options():
    options = """
Occupancy Verification Script
[Enter] to accept
[x] to exit/quit
    """
    print(f'{options}')


def get_user_information():
    logging.debug('Get user information')
    display_options()
    all_inputs = [['Analyst'], ['Location'], ['Direction'], ['Lane']]

    for parameter in all_inputs:
        user_input = input(f'{parameter[0]}: ')
        if user_input.lower() == 'x':
            break
        else:
            parameter.append(user_input)
    for item in all_inputs:
        logging.info(f'{item[0]}: {item[1]}')


def start_collection_ui():
    root = Tk()
    root.title('Occupancy Count')

    content = ttk.Frame(root)
    content.grid(column=0, row=0)

    # create buttons
    car_one_occupant = ttk.Button(content, text='Car 1 Person', command=log_one_passenger_car)
    car_two_occupant = ttk.Button(content, text='Car 2 Person', command=log_two_passenger_car)
    car_three_occupant = ttk.Button(content, text='Car 3 Person', command=log_three_passenger_car)
    car_four_occupant = ttk.Button(content, text='Car 4 Person', command=log_four_passenger_car)
    motorcycle = ttk.Button(content, text='Motorcycle', command=log_motorcycle)
    van = ttk.Button(content, text='Van', command=log_van)
    transit = ttk.Button(content, text='Transit', command=log_transit)
    other_transit = ttk.Button(content, text='Other Transit', command=log_transit_other)
    truck = ttk.Button(content, text='Truck', command=log_two_axle_truck)
    truck_three = ttk.Button(content, text='Truck 3+', command=log_three_axle_truck)

    # add buttons to grid
    car_one_occupant.grid(column=0, row=0)
    car_two_occupant.grid(column=1, row=0)
    car_three_occupant.grid(column=2, row=0)
    car_four_occupant.grid(column=3, row=0)
    motorcycle.grid(column=4, row=0)
    van.grid(column=0, row=2)
    transit.grid(column=1, row=2)
    other_transit.grid(column=2, row=2)
    truck.grid(column=3, row=2)
    truck_three.grid(column=4, row=2)

    # create shortcut labels
    one_passenger_car_shortcut_text = '[' + configuration_data['keyboard_shortcuts']['one_passenger_car'] + ']'
    one_passenger_car_shortcut = ttk.Label(content, text=one_passenger_car_shortcut_text).grid(column=0, row=1)
    two_passenger_car_shortcut_text = '[' + configuration_data['keyboard_shortcuts']['two_passenger_car'] + ']'
    two_passenger_car_shortcut = ttk.Label(content, text=two_passenger_car_shortcut_text).grid(column=1, row=1)
    three_passenger_car_shortcut_text = '[' + configuration_data['keyboard_shortcuts']['three_passenger_car'] + ']'
    three_passenger_car_shortcut = ttk.Label(content, text=three_passenger_car_shortcut_text).grid(column=2, row=1)
    four_passenger_car_shortcut_text = '[' + configuration_data['keyboard_shortcuts']['four_passenger_car'] + ']'
    four_passenger_car_shortcut = ttk.Label(content, text=four_passenger_car_shortcut_text).grid(column=3, row=1)
    motorcycle_shortcut_text = '[' + configuration_data['keyboard_shortcuts']['motorcycle'] + ']'
    motorcycle_shortcut = ttk.Label(content, text=motorcycle_shortcut_text).grid(column=4, row=1)
    van_shortcut_text = '[' + configuration_data['keyboard_shortcuts']['van'] + ']'
    van_shortcut = ttk.Label(content, text=van_shortcut_text).grid(column=0, row=3)
    transit_shortcut_text = '[' + configuration_data['keyboard_shortcuts']['transit'] + ']'
    transit_shortcut = ttk.Label(content, text=transit_shortcut_text).grid(column=1, row=3)
    other_transit_shortcut_text = '[' + configuration_data['keyboard_shortcuts']['transit_other'] + ']'
    other_transit_shortcut = ttk.Label(content, text=other_transit_shortcut_text).grid(column=2, row=3)
    truck_shortcut_text = '[' + configuration_data['keyboard_shortcuts']['two_axle_truck'] + ']'
    truck_shortcut = ttk.Label(content, text=truck_shortcut_text).grid(column=3, row=3)
    truck_three_axle_shortcut_text = '[' + configuration_data['keyboard_shortcuts']['three_axle_truck'] + ']'
    truck_three_axle_shortcut = ttk.Label(content, text=truck_three_axle_shortcut_text).grid(column=4, row=3)

    undo_shortcut_text = '[' + configuration_data['keyboard_shortcuts']['undo'] + '] = Undo'
    undo_shortcut = ttk.Label(content, text=undo_shortcut_text).grid(column=0, row=4)

    # bind keyboard shortcuts
    root.bind(configuration_data['keyboard_shortcuts']['one_passenger_car'], log_one_passenger_car)
    root.bind(configuration_data['keyboard_shortcuts']['two_passenger_car'], log_two_passenger_car)
    root.bind(configuration_data['keyboard_shortcuts']['three_passenger_car'], log_three_passenger_car)
    root.bind(configuration_data['keyboard_shortcuts']['four_passenger_car'], log_four_passenger_car())
    root.bind(configuration_data['keyboard_shortcuts']['motorcycle'], log_motorcycle)
    root.bind(configuration_data['keyboard_shortcuts']['two_axle_truck'], log_two_axle_truck)
    root.bind(configuration_data['keyboard_shortcuts']['three_axle_truck'], log_three_axle_truck)
    root.bind(configuration_data['keyboard_shortcuts']['van'], log_van)
    root.bind(configuration_data['keyboard_shortcuts']['transit'], log_transit)
    root.bind(configuration_data['keyboard_shortcuts']['transit_other'], log_transit_other)
    root.bind(configuration_data['keyboard_shortcuts']['undo'], remove_last_line_in_file)

    root.mainloop()


def remove_last_line_in_file(args):
    print('Undo')
    global log_filename
    with open(log_filename, "r+") as file:

        # Move the pointer to the end of the file
        file.seek(0, os.SEEK_END)

        # This code means the following code skips the very last character in the file -
        # i.e. in the case the last line is null we delete the last line
        # and the penultimate one
        pos = file.tell() - 1

        # Read each character in the file one at a time from the penultimate
        # character going backwards, searching for a newline character
        # If we find a new line, exit the search
        while pos > 0 and file.read(1) != "\n":
            pos -= 1
            file.seek(pos, os.SEEK_SET)

        # So long as we're not at the start of the file, delete all the characters ahead
        # of this position
        if pos > 0:
            file.seek(pos, os.SEEK_SET)
            file.truncate()


def validate_keyboard_shortcuts(shortcuts: dict):
    for key in shortcuts:
        value = str(shortcuts[key])
        alphanumeric = string.ascii_uppercase + string.ascii_uppercase + string.digits
        if len(value) > 1:
            raise ValueError(f'Keyboard shortcut for {value} is too long')
        elif value not in alphanumeric:
            raise ValueError(f'{shortcuts[key]} is not a valid input')


def log_one_passenger_car(*args):
    print(f'one passenger car')
    log_parameter = configuration_data['data_parameters']['one_passenger_car']
    logging.info(f'{log_parameter}')


def log_two_passenger_car(*args):
    print(f'two passenger car')
    log_parameter = configuration_data['data_parameters']['two_passenger_car']
    logging.info(f'{log_parameter}')


def log_three_passenger_car(*args):
    print(f'three passenger car')
    log_parameter = configuration_data['data_parameters']['three_passenger_car']
    logging.info(f'{log_parameter}')


def log_four_passenger_car(*args):
    print(f'four passenger car')
    log_parameter = configuration_data['data_parameters']['four_passenger_car']
    logging.info(f'{log_parameter}')


def log_motorcycle(*args):
    print(f'motorcycle')
    log_parameter = configuration_data['data_parameters']['motorcycle']
    logging.info(f'{log_parameter}')


def log_two_axle_truck(*args):
    print(f'two axle truck')
    log_parameter = configuration_data['data_parameters']['two_axle_truck']
    logging.info(f'{log_parameter}')


def log_three_axle_truck(*args):
    print(f'three axle truck')
    log_parameter = configuration_data['data_parameters']['three_axle_truck']
    logging.info(f'{log_parameter}')


def log_van(*args):
    print(f'van')
    log_parameter = configuration_data['data_parameters']['van']
    logging.info(f'{log_parameter}')


def log_transit(*args):
    print(f'transit')
    log_parameter = configuration_data['data_parameters']['transit']
    logging.info(f'{log_parameter}')


def log_transit_other(*args):
    print(f'transit other')
    log_parameter = configuration_data['data_parameters']['transit_other']
    logging.info(f'{log_parameter}')


def read_configuration_file(filename):
    logging.debug(f'Read configuration file: {filename}')
    f = open(filename)
    global configuration_data
    configuration_data = json.load(f)
    validate_keyboard_shortcuts(configuration_data['keyboard_shortcuts'])


def main():
    global log_filename
    log_filename = 'occupancy_count.log'
    configuration_filename = 'configuration.json'
    enable_logging(log_filename)

    read_configuration_file(configuration_filename)
    # get_user_information(log_filename)
    start_collection_ui()
    # remove_last_line_in_file(log_filename)


if __name__ == '__main__':
    main()
