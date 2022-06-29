import sys
import importlib
import yaml
import time
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # src folder
config_location = rf"{BASE_DIR}\config.yaml"  # config file location
plugin_location = rf"{BASE_DIR}\plugins"  # plugin location


def run():
    yaml_data = yaml_read(config_location)

    limorconst, constant_name = limit_or_constant(yaml_data['input'])  # checks if using limit or constant

    input_plugin = yaml_data['input']['data_format'].lower()  # loading of the yaml input data
    changing_name = yaml_data['input']['changing_variable']
    interval = yaml_data['input']['interval']

    output_plugin = yaml_data['output']['output_format'].lower()  # loading of the yaml output
    step = yaml_data['output']['minimum_step']
    minimum = yaml_data['output']['constant_variable_lower_limit']
    maximum = yaml_data['output']['constant_variable_upper_limit']

    input_module = module_loader(True, input_plugin)  # initializes the plugins and corrects the time
    output_module = module_loader(False, output_plugin)
    interval_seconds = convert_to_seconds(interval)

    if limorconst:
        print(f"Comparing variable ({changing_name}) to variable ({constant_name})")
        name = constant_name
    elif limorconst is False:
        print(f"Comparing variable ({changing_name}) to variable ({constant_name})")
        name = 'limit'

    # print(f"src:  {BASE_DIR}\nconfig:  {config_location}\nplugins:  {plugin_location}")
    print(f"Interval: {interval_seconds} s")  # lets the user know information while init
    print("Initialisation Finished\n")

    while True:

        time.sleep(interval_seconds)  # interval waiting

        # evaluates the input data
        tmp = values_check(input_module.return_to_main(**yaml_data['input']),
                           constant_name,
                           changing_name,
                           limorconst)

        # checks what value to change the output to
        value = change_value(output_module.current_value(**yaml_data['output']), tmp[0], step, minimum, maximum)

        if tmp[0] == "same":
            print(f"changing ({changing_name}: {tmp[1]:.4g}) is the same as constant ({name}: {tmp[2]:.4g})\n")
        elif tmp[0] == "greater_than":
            print(f"changing ({changing_name}: {tmp[1]:.4g}) is greater than constant ({name}: {tmp[2]:.4g})")
            if isinstance(value, str):
                print(f"ERROR: {value}\n")
            elif not isinstance(value, str):
                output_module.output_from_main(value, **yaml_data['output'])  # calls the output with change value
        elif tmp[0] == "less_than":
            print(f"changing ({changing_name}: {tmp[1]:.4g}) is less than constant ({name}: {tmp[2]:.4g})")
            if isinstance(value, str):
                print(f"ERROR: {value}\n")
            elif not isinstance(value, str):
                output_module.output_from_main(value, **yaml_data['output'])
        else:
            print(f"ERROR: {tmp[0]}")


# reads the yaml file and loads it
def yaml_read(config_file_location):
    with open(config_file_location, 'r') as file:
        yaml_data = yaml.safe_load(file)
    return yaml_data


# imports the module and returns the module
def module_loader(ioro, name):  # ioro = input or output. True being input and False being output
    if ioro:
        MODULE_PATH = f"{plugin_location}/input/{name}/__init__.py"
    elif ioro is False:
        MODULE_PATH = f"{plugin_location}/output/{name}/__init__.py"
    MODULE_NAME = "message"
    spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    module.message()
    return module


# evaluates the input values
def values_check(input_values, constant_name, changing_name, limorconst):
    if limorconst:
        # add logic to check there are both values and not nulls
        if input_values[constant_name] is None and input_values[changing_name] is None:
            return ["Both Values are Null\n", input_values[changing_name], input_values[constant_name]]
        elif input_values[constant_name] is None:
            return [f"{constant_name} is Null", input_values[changing_name], input_values[constant_name]]
        elif input_values[changing_name] is None:
            return [f"{changing_name} is Null", input_values[changing_name], input_values[constant_name]]

        if input_values[constant_name] == input_values[changing_name]:
            return ["same", input_values[changing_name], input_values[constant_name]]
        elif input_values[constant_name] < input_values[changing_name]:
            return ["greater_than", input_values[changing_name], input_values[constant_name]]
        elif input_values[constant_name] > input_values[changing_name]:
            return ["less_than", input_values[changing_name], input_values[constant_name]]

    elif limorconst is False:

        input_values['limit'] = constant_name

        if input_values[changing_name] is None:
            return [f"{changing_name} is Null", input_values[changing_name], input_values['limit']]

        if input_values['limit'] == input_values[changing_name]:
            return ["same", input_values[changing_name], input_values['limit']]
        elif input_values['limit'] < input_values[changing_name]:
            return ["greater_than", input_values[changing_name], input_values['limit']]
        elif input_values['limit'] > input_values[changing_name]:
            return ["less_than", input_values[changing_name], input_values['limit']]


def convert_to_seconds(s):
    seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
    tmp = int(s[:-1]) * seconds_per_unit[s[-1]]
    return tmp


def change_value(value, flag, step, mini, maxi):
    if step is None:  # if step not defined then it sets a default
        step = 0.5

    possible_values = np.arange(mini, maxi + step, step).tolist()  # create a dict of the possible values

    if value not in possible_values:  # checks if value is either in range or the set values
        compare = {}
        for x, y in enumerate(possible_values):
            compare[x] = abs(value - y)
        closest_value = int(sorted(compare.items(), key=lambda kv: (kv[1], kv[0]))[0][0])
        # gets the closest value to the one read by the outputs plugin

    elif value in possible_values:  # returns the index of the value
        for x, y in enumerate(possible_values):
            if y == value:
                # print(x, y)  # TESTING
                closest_value = int(x)
        # print(f"closest index is: {closest_value}\ttranslated: {possible_values[closest_value]}")  # TESTING

    if flag == "greater_than" and closest_value != 0:
        return possible_values[closest_value - 1]
    elif flag == "less_than" and closest_value + 1 != len(possible_values):
        return possible_values[closest_value + 1]
    elif flag == "same":
        return possible_values[closest_value]
    elif closest_value + 1 == len(possible_values):
        return f"Reached maximum possible value of {maxi}"
    elif closest_value == 0:
        return f"Reached minimum possible value of {mini}"
    else:
        return f"Change_value {flag}"


def limit_or_constant(yaml_data_input):
    flag = 0
    tmp = None

    try:
        tmp = yaml_data_input['limit']
        flag = False
    except Exception as E:
        pass

    try:
        tmp = yaml_data_input['constant_variable']
        flag = True
    except Exception as E:
        pass

    if tmp is None:
        raise ValueError('Config file could not find either a limit or a constant_variable')

    return flag, tmp