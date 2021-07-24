import pickle

from computorv2.globals_vars import ASSIGNED_FILE_NAME


def open_and_deserialize_assigned_list() -> list:
    try:
        with open(ASSIGNED_FILE_NAME, "rb") as file:
            unpickler = pickle.Unpickler(file)
            assigned_list = unpickler.load()
    except OSError as err:
        assigned_list = []
    except EOFError:
        assigned_list = []
    return assigned_list


def serialize_and_save_assigned_list(assigned_list: list):
    with open(ASSIGNED_FILE_NAME, "wb") as file:
        pickler = pickle.Pickler(file, pickle.HIGHEST_PROTOCOL)
        pickler.dump(assigned_list)


def clear_assigned_file():
    open(ASSIGNED_FILE_NAME, "w").close()


def list_assigned_file():
    assigned_list = open_and_deserialize_assigned_list()
    if len(assigned_list) == 0:
        print("no stored data yet.")
    else:
        for elem in assigned_list:
            print(elem.__repr__())
