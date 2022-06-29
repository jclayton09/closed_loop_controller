from closed_loop_controller import limit_or_constant


def message():  # Just a quick message for the program to recognise it has loaded in
    print(f"Output plugin loaded: ")


def return_to_main(**kwargs):  # return to main function
    limorconst, constant_variable = limit_or_constant(kwargs)

    if limorconst:
        return tmp
    elif limorconst is False:
        return tmp