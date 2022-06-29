def message():
    print(f"Output plugin loaded: ")


def output_from_main(value, **kwargs):
    print(f"Set the system to: {value}\n")


def current_value(**kwargs):
    print(f"System already at: {tmp}")

    return tmp

