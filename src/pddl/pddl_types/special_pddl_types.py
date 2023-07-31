

from pddl.pddl_types.base_pddl_types import ObjectType


# A pddl type used to count the number of objects of a certain type
# Used for propositionalization
class IntType(ObjectType):
    type_name = "int"
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
