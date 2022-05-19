# Uses ticcmd to send and receive data from the Tic over USB.
# Works with either Python 2 or Python 3.
#
# NOTE: The Tic's control mode must be "Serial / I2C / USB".

import subprocess
import sys
import configparser
# import yaml

def ticcmd(*args):
    return subprocess.check_output(['ticcmd'] + list(args))


if __name__ == '__main__':
    assert len(sys.argv) == 2

    config = configparser.ConfigParser()
    config.read('config.cfg')
    gearRatio = float(config['DEFAULT']['gear_ratio'])
    motorDegrees = float(config['DEFAULT']['motor_degrees'])

    print("gearRatio : " + str(gearRatio))
    print("multiplied : " + str(gearRatio * motorDegrees))

    argument = str(sys.argv[1])
    if argument == '-r':
        print(ticcmd().decode('UTF-8'))
        print('-r')
    else:
        print(ticcmd().decode('UTF-8'))
        print('angle')
