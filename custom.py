# Uses ticcmd to send and receive data from the Tic over USB.
#
# NOTE: The Tic's control mode must be "Serial / I2C / USB".

import subprocess  # allows you to call another program, i.e. ticcmd
import sys
import configparser
import logging
import logging.handlers
import os
import time
from enum import Enum


# Enum indicating whether the move should actually happen or
# the actions should only print to terminal and log.
# This last option is usefull for testing without an actual motor,
# in which case actual commands will throw an exception
class Mode(Enum):
    MOVE = 1
    PRINT_ONLY = 2


# Call ticcmd with the arguments passed to this function
def ticcmd(*args):
    return subprocess.check_output(['ticcmd'] + list(args))


# Run the ticcmd commands as given in the config file under
# RESET or ANGLE respectively
def run(commands, mode, steps, delay):
    # loop over all commands
    for unused, command in commands:
        # split the string from the input file into several strings. delimiter is ','
        input_list = command.split(",")

        # replace NUM with a string representation of the nr of steps
        argument_list = [word if word != 'NUM' else str(steps) for word in input_list]

        print_and_log('ticcmd ' + ' '.join(argument_list))

        # Only actually move in MOVE mode
        if mode == Mode.MOVE:
            # execute the ticcmd and print whatever it returns.
            print_and_log(ticcmd(*argument_list).decode('UTF-8'))

        # Wait some time to give the tic time to process and execute commands
        time.sleep(delay)


def setup_logging(logging_enabled, logging_location):
    root = logging.getLogger()

    if logging_enabled:
        handler = logging.handlers.WatchedFileHandler(
            os.environ.get("LOGFILE", logging_location))
        formatter = logging.Formatter(logging.BASIC_FORMAT)
        handler.setFormatter(formatter)
        root.setLevel(os.environ.get("LOGLEVEL", "DEBUG"))
        root.addHandler(handler)


def read_config():
    config = configparser.ConfigParser()
    config.read('config.cfg')
    settings = 'SETTINGS'
    gear_ratio = float(config[settings]['gear_ratio'])
    mode = Mode[config[settings]['mode']]  # convert string to enum
    delay = float(config[settings]['delay'])
    logging_enabled = config.getboolean(settings, 'logging_enabled')
    logging_location = str(config.get(settings, 'logging_location', fallback='./Arta_tic.log'))

    return gear_ratio, mode, delay, logging_enabled, logging_location


def read_commands(section):
    config = configparser.ConfigParser()
    config.read('config.cfg')
    commands = config.items(section)

    return commands


def print_and_log(line):
    log = logging.getLogger('Arta_tic')

    print(line)
    log.debug(line)


def start():
    (gear_ratio, mode, delay, logging_enabled, logging_location) = read_config()

    setup_logging(logging_enabled, logging_location)

    print_and_log("gear_ratio : " + str(gear_ratio))

    # this gets a string representation of the argument passed to main.py/exe
    argument = str(sys.argv[1])

    # Here the two types of ARTA calls are handled.
    # Set current position as zero:
    if argument == '-r':
        print_and_log('Reset :')
        commands = read_commands("RESET")
        run(commands, mode, 0, delay)
    # and go to angle
    else:
        # convert the argument from a string to a floating point number
        angle = float(argument)

        # Calculate the amount of steps based on the angle and the gear_ratio and
        # convert to an integer
        steps = int(angle * gear_ratio)

        print_and_log('Angle : ' + str(angle))
        commands = read_commands("ANGLE")
        run(commands, mode, steps, delay)


# This is the entry point of main.py
if __name__ == '__main__':
    # check the amount of arguments passed to python.
    # Note that the first (with index 0) argument is main.py
    # The second argument is either '-r' or an angle
    assert len(sys.argv) == 2, "The number of arguments is wrong. Program needs to be called like this: [main.exe -r] or [python main.py 10]. "

    print_and_log('Custom script')

    # GO!
    # Having functions helps in having a clear scope of variables.
    # variables here are kinda global (according to the internet)
    start()

    sys.exit(0)