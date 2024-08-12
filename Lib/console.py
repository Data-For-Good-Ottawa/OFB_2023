
class _Colours:
    # default
    RESET = '\033[0m'
    # warning
    YELLOW = '\033[93m'
    # error
    RED = '\033[91m'

    GREEN = '\033[92m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'


def print_warn(msg: str):
    print(_Colours.YELLOW + "Warning: " + msg + _Colours.RESET)


def print_error(msg: str):
    print(_Colours.RED + "Error: " + msg + _Colours.RESET)