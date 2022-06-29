import json
import subprocess

from closed_loop_controller import limit_or_constant


def message():  # Just a quick message for the program to recognise it has loaded in
    print(f"Input plugin loaded: exec")


def return_to_main(**kwargs):  # return to main function
    commands = kwargs['commands']
    changing_variable = kwargs['changing_variable']
    limorconst, constant_variable = limit_or_constant(kwargs)

    if limorconst:
        result = subprocess.run(commands, capture_output=True, text=True, shell=True)
        output = json.loads(result.stdout.replace("'", '"'))
        tmp = {
            changing_variable: output[changing_variable],
            constant_variable: output[constant_variable]
        }

    elif limorconst is False:
        result = subprocess.run(commands, capture_output=True, text=True, shell=True)
        output = json.loads(result.stdout.replace("'", '"'))
        tmp = {
            changing_variable: output[changing_variable],
        }

    return tmp
