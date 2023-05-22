from typing import List
from pddl.pddl_types.types_names import TypeName
from pddl.pddl_types.named_pddl_types import NamedBlockType, NamedItemType
from pddl.operators import *
from pddl.predicates import *
from pddl.functions import *


class Action:
    def __init__(self) -> None:
        self.name = None
        self.parameters = []
        self.preconditions = []
        self.effects = []

    def to_pddl(self) -> str:
        raise NotImplementedError


class Move(Action):

    def __init__(self, dir: str) -> None:
        super().__init__()
        self.dir = dir
        self.action_name = "move-" + dir
        self.parameters = {TypeName.AGENT_TYPE_NAME.value: "?ag"}

    def construct_preconditions(self):
        directions = {"north": "-1", "south": "1", "east": "1", "west": "-1"}
        if (self.dir == "east" or self.dir == "west"):
            x_equality = pddl_equal(f"({XPositionFunction.var_name} ?b)",
                                    pddl_add(
                                        f"({XPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})",
                                        directions[self.dir]
                                    ))
        else:
            x_equality = pddl_equal(
                f"({XPositionFunction.var_name} ?b)", f"({XPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})")

        if (self.dir == "north" or self.dir == "south"):
            z_equality = pddl_equal(f"({ZPositionFunction.var_name} ?b)",
                                    pddl_add(
                                        f"({ZPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})",
                                        directions[self.dir]
                                    ))
        else:
            z_equality = pddl_equal(
                f"({ZPositionFunction.var_name} ?b)", f"({ZPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})")

        self.preconditions = pddl_and(f"({AgentAlivePredicate.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})",
                                      pddl_not(pddl_exists({TypeName.BLOCK_TYPE_NAME.value: "?b"},
                                                           pddl_and(
                                          x_equality,
                                          pddl_equal(
                                              f"({YPositionFunction.var_name} ?b)", pddl_add(
                                                  f"({YPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})", "1")),
                                          z_equality,
                                      ))))

    def construct_effects(self):
        effect = ""
        if self.dir == "north":
            effect = pddl_decrease(
                f"({ZPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})", "1")
        elif self.dir == "south":
            effect = pddl_increase(
                f"({ZPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})", "1")
        elif self.dir == "east":
            effect = pddl_increase(
                f"({XPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})", "1")
        elif self.dir == "west":
            effect = pddl_decrease(
                f"({XPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})", "1")
        self.effects = pddl_and(effect)

    def to_pddl(self):
        self.construct_preconditions()
        self.construct_effects()
        out = f"(:action {self.action_name}\n"
        out += f"\t:parameters ({' '.join([f'{v} - {k}' for k, v in self.parameters.items()])})\n"
        out += f"\t:precondition {self.preconditions}\n"
        out += f"\t:effect {self.effects}\n"
        out += ")\n"
        return out


class Pickup(Action):
    def __init__(self, item: str) -> None:
        super().__init__()
        self.item = item
        self.action_name = "pickup-" + item
        self.parameters = {TypeName.AGENT_TYPE_NAME.value: "?ag", item: "?i"}

    def construct_preconditions(self):
        self.preconditions = pddl_and(f"({ItemPresentPredicate.var_name} {self.parameters[self.item]})",
                        pddl_equal(f"({XPositionFunction.var_name} {self.parameters[self.item]})", f"({XPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})"),
                        pddl_equal(f"({YPositionFunction.var_name} {self.parameters[self.item]})", f"({YPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})"),
                        pddl_equal(f"({ZPositionFunction.var_name} {self.parameters[self.item]})", f"({ZPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})"),)
        
    def construct_effects(self):
        self.effects = pddl_and(pddl_increase(f"({InventoryFunction.var_name.format(self.item)} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})", "1"),
                                pddl_not(f"({ItemPresentPredicate.var_name} {self.parameters[self.item]})"))
        

    def to_pddl(self):
        self.construct_preconditions()
        self.construct_effects()
        out = f"(:action {self.action_name}\n"
        out += f"\t:parameters ({' '.join([f'{v} - {k}' for k, v in self.parameters.items()])})\n"
        out += f"\t:precondition {self.preconditions}\n"
        out += f"\t:effect {self.effects}\n"
        out += ")\n"
        return out
    
class Drop(Action):
    def __init__(self, item:str) -> None:
        super().__init__()
        self.item = item
        self.action_name = "drop-" + item
        self.parameters = {TypeName.AGENT_TYPE_NAME.value: "?ag", item: "?i"}
    
    def construct_preconditions(self):
        self.preconditions = pddl_and(pddl_ge(f"({InventoryFunction.var_name.format(self.item)} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})", "1"),
                                      pddl_not(f"({ItemPresentPredicate.var_name} {self.parameters[self.item]})"))
        
    def construct_effects(self):
        self.effects = pddl_and(f"({ItemPresentPredicate.var_name} {self.parameters[self.item]})",
                                pddl_assign(f"({XPositionFunction.var_name} {self.parameters[self.item]})", f"({XPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})"),
                                pddl_assign(f"({YPositionFunction.var_name} {self.parameters[self.item]})", f"({YPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})"),
                                pddl_assign(f"({ZPositionFunction.var_name} {self.parameters[self.item]})", pddl_add(f"({ZPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})", "-1")),
                                pddl_decrease(f"({InventoryFunction.var_name.format(self.item)} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})", "1"))
                                
    
    def to_pddl(self):
        self.construct_preconditions()
        self.construct_effects()
        out = f"(:action {self.action_name}\n"
        out += f"\t:parameters ({' '.join([f'{v} - {k}' for k, v in self.parameters.items()])})\n"
        out += f"\t:precondition {self.preconditions}\n"
        out += f"\t:effect {self.effects}\n"
        out += ")\n"
        return out

class Break(Action):
    def __init__(self, block: str) -> None:
        super().__init__()
        self.block = block
        self.action_name = "break-" + block
        self.parameters = {TypeName.AGENT_TYPE_NAME.value: "?ag", block: "?b"}

    def construct_preconditions(self):
        self.preconditions = pddl_and(pddl_equal(f"({XPositionFunction.var_name} {self.parameters[self.block]})", f"({XPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})"),
                                     pddl_equal(f"({YPositionFunction.var_name} {self.parameters[self.block]})", pddl_add(f"({YPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})", "1")),
                                     pddl_equal(f"({ZPositionFunction.var_name} {self.parameters[self.block]})", pddl_add(f"({ZPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})", "-1")), 
                                      f"({BlockPresentPredicate.var_name} {self.parameters[self.block]})")

    def construct_effects(self):
        self.effects = pddl_and(pddl_not(f"({BlockPresentPredicate.var_name} {self.parameters[self.block]})"), pddl_increase(f"({InventoryFunction.var_name.format(self.block)} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})", "1"))

    def to_pddl(self):
        self.construct_preconditions()
        self.construct_effects()
        out = f"(:action {self.action_name}\n"
        out += f"\t:parameters ({' '.join([f'{v} - {k}' for k, v in self.parameters.items()])})\n"
        out += f"\t:precondition {self.preconditions}\n"
        out += f"\t:effect {self.effects}\n"
        out += ")\n"
        return out

class Place(Action):
    def __init__(self, block: str) -> None:
        super().__init__()
        self.block = block
        self.action_name = "place-" + block
        self.parameters = {TypeName.AGENT_TYPE_NAME.value: "?ag", block: "?b"}

    def construct_preconditions(self):
        self.preconditions = pddl_and(pddl_exists({TypeName.BLOCK_TYPE_NAME.value: "?bl"}, pddl_and(pddl_equal(f"({XPositionFunction.var_name} {self.parameters[self.block]})", f"({XPositionFunction.var_name} ?bl)"), # There must be a block underneath
                                                                                                    pddl_equal(f"({YPositionFunction.var_name} {self.parameters[self.block]})", pddl_add(f"({YPositionFunction.var_name} ?bl)", "1")),
                                                                                                    pddl_equal(f"({ZPositionFunction.var_name} {self.parameters[self.block]})", f"({ZPositionFunction.var_name} ?bl)"))), # There mustn't be a block at the same location
                                      pddl_not(pddl_exists({TypeName.BLOCK_TYPE_NAME.value: "?bl"}, pddl_and(pddl_equal(f"({XPositionFunction.var_name} {self.parameters[self.block]})", f"({XPositionFunction.var_name} ?bl)"),
                                                                                                             pddl_equal(f"({YPositionFunction.var_name} {self.parameters[self.block]})", f"({YPositionFunction.var_name} ?bl)"),
                                                                                                             pddl_equal(f"({ZPositionFunction.var_name} {self.parameters[self.block]})", f"({ZPositionFunction.var_name} ?bl)")))),
                                      pddl_and(pddl_equal(f"({XPositionFunction.var_name} {self.parameters[self.block]})", f"({XPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})"), # The player must be direction facing and standing next to the location
                                               pddl_equal(f"({YPositionFunction.var_name} {self.parameters[self.block]})", pddl_add(f"({YPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})", "1")),
                                               pddl_equal(f"({ZPositionFunction.var_name} {self.parameters[self.block]})", pddl_add(f"({ZPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})", "-1"))))
    def construct_effects(self):
        self.effects = pddl_and(f"({BlockPresentPredicate.var_name} {self.parameters[self.block]})", 
                                pddl_assign(f"({XPositionFunction.var_name} {self.parameters[self.block]})", f"({XPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})"),
                                pddl_assign(f"({YPositionFunction.var_name} {self.parameters[self.block]})", pddl_add(f"({YPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})","1")),
                                pddl_assign(f"({ZPositionFunction.var_name} {self.parameters[self.block]})", pddl_add(f"({ZPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})", "-1")),
                                pddl_decrease(f"({InventoryFunction.var_name.format(self.block)} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})", "1"))

    def to_pddl(self):
        self.construct_preconditions()
        self.construct_effects()
        out = f"(:action {self.action_name}\n"
        out += f"\t:parameters ({' '.join([f'{v} - {k}' for k, v in self.parameters.items()])})\n"
        out += f"\t:precondition {self.preconditions}\n"
        out += f"\t:effect {self.effects}\n"
        out += ")\n"
        return out


class JumpUp(Action):
    # jumps up one block forward
    def __init__(self) -> None:
        super().__init__()
        self.action_name = "jump-up"
        self.parameters = {TypeName.AGENT_TYPE_NAME.value: "?ag"}

    def construct_preconditions(self):
        self.preconditions = pddl_and(pddl_exists({TypeName.BLOCK_TYPE_NAME.value: "?bl"}, pddl_and(pddl_equal(f"({XPositionFunction.var_name} ?bl)", f"({XPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})"),
                                                                                                    pddl_equal(f"({YPositionFunction.var_name} ?bl)", f"({YPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})"),
                                                                                                    pddl_equal(f"({ZPositionFunction.var_name} ?bl)", pddl_add(f"({ZPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})", "-1"))))) # There must be a block underneath and infront
    def construct_effects(self):
        self.effects = pddl_and(pddl_assign(f"({ZPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})", pddl_add(f"({ZPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})", "-1")),
                                pddl_assign(f"({YPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})", pddl_add(f"({YPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})", "1")))

    def to_pddl(self):
        self.construct_preconditions()
        self.construct_effects()
        out = f"(:action {self.action_name}\n"
        out += f"\t:parameters ({' '.join([f'{v} - {k}' for k, v in self.parameters.items()])})\n"
        out += f"\t:precondition {self.preconditions}\n"
        out += f"\t:effect {self.effects}\n"
        out += ")\n"
        return out
