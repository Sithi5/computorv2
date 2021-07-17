from variables_file import (
    serialize_and_save_variables_list,
    open_and_deserialize_variables_list,
)
from variables_types import *
from utils import (
    convert_to_tokens,
)


def resolve_variable_value(variable_to_resolve: BaseType, variables_list: list):
    resolved_value = variable_to_resolve.value
    if variable_to_resolve._lock is True:
        return variable_to_resolve.value
    else:
        for index, token in enumerate(variable_to_resolve.value):
            if str(token).isalpha:
                for index_variable, variable in enumerate(variables_list):
                    if variable.name == str(token):
                        # Locking the variable to prevent infinite lookaround resolution.
                        variables_list[index_variable]._lock = True
                        resolved_value = (
                            resolved_value[:index]
                            + resolve_variable_value(
                                variable_to_resolve=variable, variables_list=variables_list
                            )
                            + resolved_value[index + 1 :]
                        )
                        variables_list[index_variable]._lock = False
                        break
        return resolved_value