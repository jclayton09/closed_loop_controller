import json
import subprocess


def message():
    print(f"Output plugin loaded: exec")


def output_from_main(value, **kwargs):
    output_command = kwargs['output_command']

    output_command.append(str(value))

    result = subprocess.run(output_command, capture_output=True, text=True, shell=True)
    output_command.pop()

    output = result.stdout

    print(f"Set the system to: {float(value):.3g}, Response: {output}")


def current_value(**kwargs):
    current_value_command = kwargs['current_value_command']
    current_value_name = kwargs['current_value']

    result = subprocess.run(current_value_command, capture_output=True, text=True, shell=True)
    output = json.loads(result.stdout.replace("'", '"'))
    tmp = output[current_value_name]

    print(f"System already at: {tmp:.3g}")

    return tmp

