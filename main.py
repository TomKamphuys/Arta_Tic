# Uses ticcmd to send and receive data from the Tic over USB.
# Works with either Python 2 or Python 3.
#
# NOTE: The Tic's control mode must be "Serial / I2C / USB".

# import subprocess
import yaml


def ticcmd(*args):
    return " DHJDHJDHDHLD"
    # return subprocess.check_output(['ticcmd'] + list(args))


# status = yaml.load(ticcmd('-s', '--full'))
status = " unknown"

# position = status['Current position']
position = 123
print("Current position is {}.".format(position))

new_target = -200 if position > 0 else 200
print("Setting target position to {}.".format(new_target))
ticcmd('--exit-safe-start', '--position', str(new_target))


