import pickle

from globals_vars import VARIABLES_FILE_NAME


def open_and_deserialize_variables_list() -> list:
    try:
        with open(VARIABLES_FILE_NAME, "rb") as file:
            unpickler = pickle.Unpickler(file)
            variables_list = unpickler.load()
    except OSError as err:
        variables_list = []
    except EOFError:
        variables_list = []
    return variables_list


def serialize_and_save_variables_list(variables_list: list):
    with open(VARIABLES_FILE_NAME, "wb") as file:
        pickler = pickle.Pickler(file, pickle.HIGHEST_PROTOCOL)
        pickler.dump(variables_list)


def clear_variables_file():
    open(VARIABLES_FILE_NAME, "w").close()


def list_variables_file():
    variables_list = open_and_deserialize_variables_list()
    if len(variables_list) == 0:
        print("no stored variable yet.")
    else:
        for variable in variables_list:
            print(str(variable))
