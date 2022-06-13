# Arta_Tic

## Introduction
Arta_Tic is a glue program between ARTA and Tic. http://nicholasmart.in/measurement_platform/ mentions a program with the name Arta_Tic, but does not provide it. 
The code in this repo tries to provide similar functionality.

ARTA calls Arta_tic with either -r or _angle_. _angle_ is a number representing the angle to be rotated.

The program was developed without direct access to a tic and motor, but in co-operation with people
who did have one. This lead to a bit more flexible program than strictly necessary:
- The sequence of ticcmd commands can be configured in the config file
- A fully custom py script can be called. The executable (created by auto-py-to-exe) can stay the same, while the behaviour can be changed.

## Configuration
Here is the example config.cfg that should move the motor:

```
[SETTINGS]
gear_ratio = 1
delay = 0.5
mode = MOVE
logging_enabled = yes
;logging_location = ./Arta_tic.log
custom_script = no
custom_script_name = custom.py

[RESET]
command0 = --resume
command1 = --reset-command-timeout
command2 = --reset

[ANGLE]
command1 = --reset-command-timeout
command2 = --position,NUM
```

### SETTINGS
- gear_ratio : The name is still under discussion, but it currenly is a simple factor between the degrees from ARTA and the steps to ticcmd
- delay : Consecutive commands are delays (value in seconds)
- mode : MOVE -> is selection, the motor is actually move; PRINT-ONLY -> motor is not move, but commands can be printed to log file. Handy for testing when you don' t have a tic.
- logging_enabled : Enables logging to a log file (which can be viewed real-time by e.g. BareTail). We encountered problems with (log) file properties and this is an easy way to work around that.
- logging_location : You can select a custom location for the log file if the default ./Arta_tic.log is not what you want.
- custom_script : script name of your custom script. Usefull when you want full freedom of what happens when ARTA calls Arta_tic with either the -r or angle argument.

### RESET
This lists the arguments to consecutive ticcmd commands. Whenever multiple arguments are required
a comma separated list has to be provided. NUM has a special meaning. It will be replaced by the 
number of steps the program has calculated to turn _angle_ degrees.

### ANGLE
Same as RESET, but now for the _angle_ case.