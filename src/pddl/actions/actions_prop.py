from typing import List, Optional

from pddl.pddl_types.types_names import TypeName
from pddl.pddl_types.named_pddl_types import NamedBlockType, NamedItemType
from pddl.operators import *
from pddl.predicates import *
from pddl.functions import *

#TODO: add direction that we are facing as a parameter to the move action 

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
        # self.item_to_pickup = item_to_pickup
        self.action_name = (
            "move-" + dir
        )  # + "-only" if item_to_pickup is None else "-and-pickup-" + self.item_to_pickup.name

        # have separate dictionaries for parameter names and types, but such that a common key is used to index corresponding values in both
        # this is necessary because multiple parameters have different names but the same type
        self.param_name = {
            "Agent": "?ag",
            "XPosition": "?x",
            "ZPosition": "?z",
            "XPositionStart": "?x_start",
            "XPositionEnd": "?x_end",
            "YPositionUp": "?y_up",
            "YPositionDown": "?y_down",
            "ZPositionStart": "?z_start",
            "ZPositionEnd": "?z_end",
        }

        self.param_types = {
            "Agent": TypeName.AGENT_TYPE_NAME.value,
            "XPosition": TypeName.POSITION_TYPE_NAME.value,
            "ZPosition": TypeName.POSITION_TYPE_NAME.value,
            "XPositionStart": TypeName.POSITION_TYPE_NAME.value,
            "XPositionEnd": TypeName.POSITION_TYPE_NAME.value,
            "YPositionUp": TypeName.POSITION_TYPE_NAME.value,
            "YPositionDown": TypeName.POSITION_TYPE_NAME.value,
            "ZPositionStart": TypeName.POSITION_TYPE_NAME.value,
            "ZPositionEnd": TypeName.POSITION_TYPE_NAME.value,
        }

    def construct_parameters(self):
        # need this generator since extra params have been added to the dicts in order to be more general
        move_east_west = self.dir == "east" or self.dir == "west"
        self.parameters = ""

        # loop through all the parameters and add them to the parameters dict if they are used
        for key in self.param_name.keys():
            # if we move east or west, we use x_start and x_end, but only z
            # if we move north or south, we use z_start and z_end, but only x

            # if we are not dealing with x or z positions, then process as normal
            if not ("XPosition" in key or "ZPosition" in key):
                self.parameters += f"{self.param_name[key]} - {self.param_types[key]} "
                continue

            if key == "XPositionStart" or key == "XPositionEnd" or key == "ZPosition":
                if move_east_west:
                    self.parameters += (
                        f"{self.param_name[key]} - {self.param_types[key]} "
                    )
                else:
                    continue
            elif key == "XPosition" or key == "ZPositionStart" or key == "ZPositionEnd":
                if not move_east_west:
                    self.parameters += (
                        f"{self.param_name[key]} - {self.param_types[key]} "
                    )
                else:
                    continue

        self.parameters = self.parameters.strip()

    def construct_preconditions(self):
        # depending on the direction of travel, we need to check that the end location is not occupied by a block/item
        # we will set the x_start, x_end, z_start, and z_end variables to hold the relevant arg names so we can just look them up later
        move_east_west = self.dir == "east" or self.dir == "west"
        direction_should_increase = self.dir == "south" or self.dir == "east"
        if move_east_west:
            x_start = self.param_name["XPositionStart"]
            x_end = self.param_name["XPositionEnd"]
        else:
            x_start = self.param_name["XPosition"]
            x_end = self.param_name["XPosition"]

        if not move_east_west:
            z_start = self.param_name["ZPositionStart"]
            z_end = self.param_name["ZPositionEnd"]
        else:
            z_start = self.param_name["ZPosition"]
            z_end = self.param_name["ZPosition"]

        # todo: confirm that these orders are correct
        if direction_should_increase:
            sequential_predicate = AreSequentialPredicate.to_precondition(
                x_start if move_east_west else z_start,
                x_end if move_east_west else z_end,
            )
        else:
            sequential_predicate = AreSequentialPredicate.to_precondition(
                x_end if move_east_west else z_end,
                x_start if move_east_west else z_start,
            )

        block_var = "?b"
        item_var = "?i"
        self.preconditions = pddl_and(
            f"({AgentAlivePredicate.var_name} {self.param_name['Agent']})\n",
            AtXLocationPredicate.to_precondition(self.param_name["Agent"], x_start),
            AtYLocationPredicate.to_precondition(
                self.param_name["Agent"],
                self.param_name[
                    "YPositionDown"
                ],  # agent coord is the bottom of the agent
            ),
            AtZLocationPredicate.to_precondition(self.param_name["Agent"], z_start),
            sequential_predicate,
            AreSequentialPredicate.to_precondition(self.param_name["YPositionDown"], self.param_name["YPositionUp"]),
            pddl_not(
                pddl_exists(
                    {TypeName.BLOCK_TYPE_NAME.value: block_var},
                    pddl_and(
                        f"({BlockPresentPredicate.var_name} {block_var})\n",
                        AtXLocationPredicate.to_precondition(block_var, x_end),
                        # here we check that there is no block at the level of the agent (bottom) or the agent's eyeline (top)
                        pddl_or(
                            AtYLocationPredicate.to_precondition(
                                block_var, self.param_name["YPositionUp"]
                            ),
                            AtYLocationPredicate.to_precondition(
                                block_var, self.param_name["YPositionDown"]
                            ),
                        ),
                        AtZLocationPredicate.to_precondition(block_var, z_end),
                    ),
                )
            ),
            pddl_not(
                pddl_exists(
                    {TypeName.ITEM_TYPE_NAME.value: item_var},
                    pddl_and(
                        f"({ItemPresentPredicate.var_name} {item_var})\n",
                        AtXLocationPredicate.to_precondition(item_var, x_end),
                        # here we only check that there is no item at the level of the agent (bottom) since items cannot float
                        # they would require a block to be placed beneath it, which is handled by the previous precondition
                        AtYLocationPredicate.to_precondition(
                            item_var, self.param_name["YPositionDown"]
                        ),
                        AtZLocationPredicate.to_precondition(item_var, z_end),
                    ),
                )
            ),
        )

    def construct_effects(self):
        # this is as simple as saying that agent is not at the start and is at the end
        if self.dir == "north" or self.dir == "south":
            start = self.param_name["ZPositionStart"]
            end = self.param_name["ZPositionEnd"]
            predicate_to_use = AtZLocationPredicate
        else:
            start = self.param_name["XPositionStart"]
            end = self.param_name["XPositionEnd"]
            predicate_to_use = AtXLocationPredicate

        self.effects = pddl_and(
            pddl_not(predicate_to_use.to_precondition(self.param_name["Agent"], start)),
            predicate_to_use.to_precondition(self.param_name["Agent"], end),
        )

    def to_pddl(self):
        self.construct_parameters()
        self.construct_preconditions()
        self.construct_effects()
        out = f"(:action {self.action_name}\n"
        out += f"\t:parameters ({self.parameters})\n"
        out += f"\t:precondition {self.preconditions}\n"
        out += f"\t:effect {self.effects}\n"
        out += ")\n"
        return out


class MoveAndPickup(Action):
    def __init__(self, dir, item) -> None:
        super().__init__()
        self.dir = dir
        self.item = item
        self.action_name = f"move-{dir}-and-pickup-{item}"

        self.param_name = {
            "Agent": "?ag",
            "Item": "?i",
            "XPosition": "?x",
            "ZPosition": "?z",
            "XPositionStart": "?x_start",
            "XPositionEnd": "?x_end",
            "YPositionUp": "?y_up",
            "YPositionDown": "?y_down",
            "ZPositionStart": "?z_start",
            "ZPositionEnd": "?z_end",
            "NStart": "?n_start",
            "NEnd": "?n_end",

        }

        self.param_types = { "Agent": TypeName.AGENT_TYPE_NAME.value,
            "Item": self.item, 
            "XPosition": TypeName.POSITION_TYPE_NAME.value,
            "ZPosition": TypeName.POSITION_TYPE_NAME.value,
            "XPositionStart": TypeName.POSITION_TYPE_NAME.value,
            "XPositionEnd": TypeName.POSITION_TYPE_NAME.value,
            "YPositionUp": TypeName.POSITION_TYPE_NAME.value,
            "YPositionDown": TypeName.POSITION_TYPE_NAME.value,
            "ZPositionStart": TypeName.POSITION_TYPE_NAME.value,
            "ZPositionEnd": TypeName.POSITION_TYPE_NAME.value,
            "NStart": TypeName.COUNT_TYPE_NAME.value,
            "NEnd": TypeName.COUNT_TYPE_NAME.value,
        }

    def construct_parameters(self):
        # need this generator since extra params have been added to the dicts in order to be more general
        move_east_west = self.dir == "east" or self.dir == "west"
        self.parameters = ""

        # loop through all the parameters and add them to the parameters dict if they are used
        for key in self.param_name.keys():
            # if we move east or west, we use x_start and x_end, but only z
            # if we move north or south, we use z_start and z_end, but only x

            # if we are not dealing with x or z positions, then process as normal
            if not ("XPosition" in key or "ZPosition" in key):
                self.parameters += f"{self.param_name[key]} - {self.param_types[key]} "
                continue

            if key == "XPositionStart" or key == "XPositionEnd" or key == "ZPosition":
                if move_east_west:
                    self.parameters += (
                        f"{self.param_name[key]} - {self.param_types[key]} "
                    )
                else:
                    continue
            elif key == "XPosition" or key == "ZPositionStart" or key == "ZPositionEnd":
                if not move_east_west:
                    self.parameters += (
                        f"{self.param_name[key]} - {self.param_types[key]} "
                    )
                else:
                    continue

        self.parameters = self.parameters.strip()

    def construct_preconditions(self):
        # depending on the direction of travel, we need to check that the end location is not occupied by a block/item
        # we will set the x_start, x_end, z_start, and z_end variables to hold the relevant arg names so we can just look them up later
        move_east_west = self.dir == "east" or self.dir == "west"
        direction_should_increase = self.dir == "south" or self.dir == "east"
        if move_east_west:
            x_start = self.param_name["XPositionStart"]
            x_end = self.param_name["XPositionEnd"]
        else:
            x_start = self.param_name["XPosition"]
            x_end = self.param_name["XPosition"]

        if not move_east_west:
            z_start = self.param_name["ZPositionStart"]
            z_end = self.param_name["ZPositionEnd"]
        else:
            z_start = self.param_name["ZPosition"]
            z_end = self.param_name["ZPosition"]

        # todo: confirm that these orders are correct
        if direction_should_increase:
            sequential_predicate = AreSequentialPredicate.to_precondition(
                x_start if move_east_west else z_start,
                x_end if move_east_west else z_end,
            )
        else:
            sequential_predicate = AreSequentialPredicate.to_precondition(
                x_end if move_east_west else z_end,
                x_start if move_east_west else z_start,
            )

        block_var = "?b"
        item_var = "?i"
        self.preconditions = pddl_and(
            f"({AgentAlivePredicate.var_name} {self.param_name['Agent']})\n",
            AtXLocationPredicate.to_precondition(self.param_name["Agent"], x_start),
            AtYLocationPredicate.to_precondition(
                self.param_name["Agent"],
                self.param_name[
                    "YPositionDown"
                ],  # agent coord is the bottom of the agent
            ),
            AtZLocationPredicate.to_precondition(self.param_name["Agent"], z_start),
            sequential_predicate,
            AreSequentialPredicate.to_precondition(self.param_name["YPositionDown"], self.param_name["YPositionUp"]),
            pddl_not(
                pddl_exists(
                    {TypeName.BLOCK_TYPE_NAME.value: block_var},
                    pddl_and(
                        f"({BlockPresentPredicate.var_name} {block_var})\n",
                        AtXLocationPredicate.to_precondition(block_var, x_end),
                        # here we check that there is no block at the level of the agent (bottom) or the agent's eyeline (top)
                        pddl_or(
                            AtYLocationPredicate.to_precondition(
                                block_var, self.param_name["YPositionUp"]
                            ),
                            AtYLocationPredicate.to_precondition(
                                block_var, self.param_name["YPositionDown"]
                            ),
                        ),
                        AtZLocationPredicate.to_precondition(block_var, z_end),
                    ),
                )
            ),
            pddl_exists(
                {TypeName.ITEM_TYPE_NAME.value: item_var},
                pddl_and(
                    f"({ItemPresentPredicate.var_name} {item_var})\n",
                    AtXLocationPredicate.to_precondition(item_var, x_end),
                    # here we only check that there is no item at the level of the agent (bottom) since items cannot float
                    # they would require a block to be placed beneath it, which is handled by the previous precondition
                    AtYLocationPredicate.to_precondition(
                        item_var, self.param_name["YPositionDown"]
                    ),
                    AtZLocationPredicate.to_precondition(item_var, z_end),
                ),
            )
        )

    def construct_effects(self):
        # this is as simple as saying that agent is not at the start and is at the end
        if self.dir == "north" or self.dir == "south":
            start = self.param_name["ZPositionStart"]
            end = self.param_name["ZPositionEnd"]
            predicate_to_use = AtZLocationPredicate
            item_location_x = self.param_name["XPosition"]
            item_location_z = self.param_name["ZPositionEnd"]
        else:
            start = self.param_name["XPositionStart"]
            end = self.param_name["XPositionEnd"]
            predicate_to_use = AtXLocationPredicate
            item_location_x = self.param_name["XPositionEnd"]
            item_location_z = self.param_name["ZPosition"]

        self.effects = pddl_and(
            pddl_not(predicate_to_use.to_precondition(self.param_name["Agent"], start)),
            predicate_to_use.to_precondition(self.param_name["Agent"], end),
            pddl_not(AgentHasNItemsPredicate.to_precondition(self.param_name["Agent"], self.param_name["NStart"], item_type=self.item)),
            pddl_not(AtXLocationPredicate.to_precondition(self.param_name["Item"], item_location_x)),
            pddl_not(AtYLocationPredicate.to_precondition(self.param_name["Item"], self.param_name["YPositionDown"])),
            pddl_not(AtZLocationPredicate.to_precondition(self.param_name["Item"], item_location_z)),
            AgentHasNItemsPredicate.to_precondition(self.param_name["Agent"], self.param_name["NEnd"], item_type=self.item),
            pddl_not(ItemPresentPredicate.to_precondition()),
        )

    def to_pddl(self):
        self.construct_parameters()
        self.construct_preconditions()
        self.construct_effects()
        out = f"(:action {self.action_name}\n"
        out += f"\t:parameters {self.parameters}\n"
        out += f"\t:precondition {self.preconditions}\n"
        out += f"\t:effect {self.effects}\n"
        out += ")\n"
        return out


class Drop(Action):
    def __init__(self, item: str) -> None:
        super().__init__()
        self.item = item
        self.action_name = "drop-" + item
        self.parameters = {TypeName.AGENT_TYPE_NAME.value: "?ag", item: "?i"}

    def construct_preconditions(self):
        self.preconditions = pddl_and(
            pddl_ge(
                f"({InventoryFunction.var_name.format(self.item)} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})",
                "1",
            ),
            pddl_not(f"({ItemPresentPredicate.var_name} {self.parameters[self.item]})"),
        )

    def construct_effects(self):
        self.effects = pddl_and(
            f"({ItemPresentPredicate.var_name} {self.parameters[self.item]})",
            pddl_assign(
                f"({XPositionFunction.var_name} {self.parameters[self.item]})",
                f"({XPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})",
            ),
            pddl_assign(
                f"({YPositionFunction.var_name} {self.parameters[self.item]})",
                f"({YPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})",
            ),
            pddl_assign(
                f"({ZPositionFunction.var_name} {self.parameters[self.item]})",
                pddl_add(
                    f"({ZPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})",
                    "-1",
                ),
            ),
            pddl_decrease(
                f"({InventoryFunction.var_name.format(self.item)} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})",
                "1",
            ),
        )

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
        self.block = block + "-block"
        self.item = block
        self.action_name = "break-" + block
        self.parameters = {TypeName.AGENT_TYPE_NAME.value: "?ag", self.block: "?b"}

    def construct_preconditions(self):
        self.preconditions = pddl_and(
            pddl_equal(
                f"({XPositionFunction.var_name} {self.parameters[self.block]})",
                f"({XPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})",
            ),
            pddl_equal(
                f"({YPositionFunction.var_name} {self.parameters[self.block]})",
                f"({YPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})",
            ),
            pddl_equal(
                f"({ZPositionFunction.var_name} {self.parameters[self.block]})",
                pddl_add(
                    f"({ZPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})",
                    "-1",
                ),
            ),
            f"({BlockPresentPredicate.var_name} {self.parameters[self.block]})",
        )

    def construct_effects(self):
        self.effects = pddl_and(
            pddl_not(
                f"({BlockPresentPredicate.var_name} {self.parameters[self.block]})"
            ),
            pddl_increase(
                f"({InventoryFunction.var_name.format(self.item)} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})",
                "1",
            ),
        )

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
        # separate the names of blocks and items in pddl
        self.block = block + "-block"
        self.item = block
        self.action_name = "place-" + block
        self.parameters = {TypeName.AGENT_TYPE_NAME.value: "?ag", self.block: "?b"}

    def construct_preconditions(self):
        self.preconditions = pddl_and(
            pddl_exists(
                {TypeName.BLOCK_TYPE_NAME.value: "?bl"},
                pddl_and(
                    pddl_equal(
                        f"({XPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})",
                        f"({XPositionFunction.var_name} ?bl)",
                    ),  # There must be a block underneath
                    pddl_equal(
                        f"({YPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})",
                        pddl_add(f"({YPositionFunction.var_name} ?bl)", "1"),
                    ),
                    pddl_equal(
                        f"({ZPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})",
                        pddl_add(f"({ZPositionFunction.var_name} ?bl)", "1"),
                    ),
                ),
            ),  # There mustn't be a block at the same location
            pddl_not(
                pddl_exists(
                    {TypeName.BLOCK_TYPE_NAME.value: "?bl"},
                    pddl_and(
                        pddl_equal(
                            f"({XPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})",
                            f"({XPositionFunction.var_name} ?bl)",
                        ),
                        pddl_equal(
                            f"({YPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})",
                            f"({YPositionFunction.var_name} ?bl)",
                        ),
                        pddl_equal(
                            f"({ZPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})",
                            pddl_add(f"({ZPositionFunction.var_name} ?bl)", "1"),
                        ),
                    ),
                )
            ),
        )

    def construct_effects(self):
        self.effects = pddl_and(
            f"({BlockPresentPredicate.var_name} {self.parameters[self.block]})",
            pddl_assign(
                f"({XPositionFunction.var_name} {self.parameters[self.block]})",
                f"({XPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})",
            ),
            pddl_assign(
                f"({YPositionFunction.var_name} {self.parameters[self.block]})",
                f"({YPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})",
            ),
            pddl_assign(
                f"({ZPositionFunction.var_name} {self.parameters[self.block]})",
                pddl_add(
                    f"({ZPositionFunction.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})",
                    "-1",
                ),
            ),
            pddl_decrease(
                f"({InventoryFunction.var_name.format(self.item)} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})",
                "1",
            ),
        )

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
    def __init__(self, dir: str) -> None:
        super().__init__()
        self.dir = dir
        # self.item_to_pickup = item_to_pickup
        self.action_name = (
            "jumpup-" + dir
        )  # + "-only" if item_to_pickup is None else "-and-pickup-" + self.item_to_pickup.name

        # have separate dictionaries for parameter names and types, but such that a common key is used to index corresponding values in both
        # this is necessary because multiple parameters have different names but the same type
        self.param_name = {
            "Agent": "?ag",
            "XPosition": "?x",
            "ZPosition": "?z",
            "XPositionStart": "?x_start",
            "XPositionEnd": "?x_end",
            "YPositionUp": "?y_up",
            "YPositionUpUp": "?y_up_up", # for jumping up
            "YPositionDown": "?y_down",
            "ZPositionStart": "?z_start",
            "ZPositionEnd": "?z_end",
        }

        self.param_types = {
            "Agent": TypeName.AGENT_TYPE_NAME.value,
            "XPosition": TypeName.POSITION_TYPE_NAME.value,
            "ZPosition": TypeName.POSITION_TYPE_NAME.value,
            "XPositionStart": TypeName.POSITION_TYPE_NAME.value,
            "XPositionEnd": TypeName.POSITION_TYPE_NAME.value,
            "YPositionUp": TypeName.POSITION_TYPE_NAME.value,
            "YPositionUpUp": TypeName.POSITION_TYPE_NAME.value,
            "YPositionDown": TypeName.POSITION_TYPE_NAME.value,
            "ZPositionStart": TypeName.POSITION_TYPE_NAME.value,
            "ZPositionEnd": TypeName.POSITION_TYPE_NAME.value,
        }

    def construct_parameters(self):
        # need this generator since extra params have been added to the dicts in order to be more general
        move_east_west = self.dir == "east" or self.dir == "west"
        self.parameters = ""

        # loop through all the parameters and add them to the parameters dict if they are used
        for key in self.param_name.keys():
            # if we move east or west, we use x_start and x_end, but only z
            # if we move north or south, we use z_start and z_end, but only x

            # if we are not dealing with x or z positions, then process as normal
            if not ("XPosition" in key or "ZPosition" in key):
                self.parameters += f"{self.param_name[key]} - {self.param_types[key]} "
                continue

            if key == "XPositionStart" or key == "XPositionEnd" or key == "ZPosition":
                if move_east_west:
                    self.parameters += (
                        f"{self.param_name[key]} - {self.param_types[key]} "
                    )
                else:
                    continue
            elif key == "XPosition" or key == "ZPositionStart" or key == "ZPositionEnd":
                if not move_east_west:
                    self.parameters += (
                        f"{self.param_name[key]} - {self.param_types[key]} "
                    )
                else:
                    continue

        self.parameters = self.parameters.strip()

    def construct_preconditions(self):
        # depending on the direction of travel, we need to check that the end location is not occupied by a block/item
        # we will set the x_start, x_end, z_start, and z_end variables to hold the relevant arg names so we can just look them up later
        move_east_west = self.dir == "east" or self.dir == "west"
        direction_should_increase = self.dir == "south" or self.dir == "east"
        if move_east_west:
            x_start = self.param_name["XPositionStart"]
            x_end = self.param_name["XPositionEnd"]
        else:
            x_start = self.param_name["XPosition"]
            x_end = self.param_name["XPosition"]

        if not move_east_west:
            z_start = self.param_name["ZPositionStart"]
            z_end = self.param_name["ZPositionEnd"]
        else:
            z_start = self.param_name["ZPosition"]
            z_end = self.param_name["ZPosition"]

        # todo: confirm that these orders are correct
        if direction_should_increase:
            sequential_predicate = AreSequentialPredicate.to_precondition(
                x_start if move_east_west else z_start,
                x_end if move_east_west else z_end,
            )
        else:
            sequential_predicate = AreSequentialPredicate.to_precondition(
                x_end if move_east_west else z_end,
                x_start if move_east_west else z_start,
            )

        block_var = "?b"
        item_var = "?i"
        self.preconditions = pddl_and(
            f"({AgentAlivePredicate.var_name} {self.param_name['Agent']})\n",
            AtXLocationPredicate.to_precondition(self.param_name["Agent"], x_start),
            AtYLocationPredicate.to_precondition(
                self.param_name["Agent"],
                self.param_name[
                    "YPositionDown"
                ],  # agent coord is the bottom of the agent
            ),
            AtZLocationPredicate.to_precondition(self.param_name["Agent"], z_start),
            sequential_predicate,
            AreSequentialPredicate.to_precondition(self.param_name["YPositionDown"], self.param_name["YPositionUp"]),
            AreSequentialPredicate.to_precondition(self.param_name["YPositionUp"], self.param_name["YPositionUpUp"]),
            pddl_not(
                pddl_exists(
                    {TypeName.BLOCK_TYPE_NAME.value: block_var},
                    pddl_and(
                        f"({BlockPresentPredicate.var_name} {block_var})\n",
                        AtXLocationPredicate.to_precondition(block_var, x_end),
                        # here we check that there is no block at the level of the agent (bottom) or the agent's eyeline (top)
                        pddl_or(
                            AtYLocationPredicate.to_precondition(
                                block_var, self.param_name["YPositionUp"]
                            ),
                            AtYLocationPredicate.to_precondition(
                                block_var, self.param_name["YPositionUpUp"]
                            ),
                        ),
                        AtZLocationPredicate.to_precondition(block_var, z_end),
                    ),
                )
            ),
            pddl_exists(
                {TypeName.BLOCK_TYPE_NAME.value: block_var},
                pddl_and(
                    f"({BlockPresentPredicate.var_name} {block_var})\n",
                    AtXLocationPredicate.to_precondition(block_var, x_end),
                    # here we check that there is no block at the level of the agent (bottom) or the agent's eyeline (top)
                    AtYLocationPredicate.to_precondition(block_var, self.param_name["YPositionDown"]),
                    AtZLocationPredicate.to_precondition(block_var, z_end),
                ),
            ),
            pddl_not(
                pddl_exists(
                    {TypeName.ITEM_TYPE_NAME.value: item_var},
                    pddl_and(
                        f"({ItemPresentPredicate.var_name} {item_var})\n",
                        AtXLocationPredicate.to_precondition(item_var, x_end),
                        # here we only check that there is no item at the level of the agent (bottom) since items cannot float
                        # they would require a block to be placed beneath it, which is handled by the previous precondition
                        pddl_or(
                            AtYLocationPredicate.to_precondition(
                                item_var, self.param_name["YPositionDown"]
                            ),
                            AtYLocationPredicate.to_precondition(
                                item_var, self.param_name["YPositionUp"]
                            )
                        ),
                        AtZLocationPredicate.to_precondition(item_var, z_end),
                    ),
                )
            ),
        )

    def construct_effects(self):
        # this is as simple as saying that agent is not at the start and is at the end
        if self.dir == "north" or self.dir == "south":
            start = self.param_name["ZPositionStart"]
            end = self.param_name["ZPositionEnd"]
            predicate_to_use = AtZLocationPredicate
        else:
            start = self.param_name["XPositionStart"]
            end = self.param_name["XPositionEnd"]
            predicate_to_use = AtXLocationPredicate

        self.effects = pddl_and(
            pddl_not(predicate_to_use.to_precondition(self.param_name["Agent"], start)),
            predicate_to_use.to_precondition(self.param_name["Agent"], end),
            pddl_not(AtYLocationPredicate.to_precondition(self.param_name["Agent"], self.param_name["YPositionDown"])),
            AtYLocationPredicate.to_precondition(self.param_name["Agent"], self.param_name["YPositionUp"]),
        )

    def to_pddl(self):
        self.construct_parameters()
        self.construct_preconditions()
        self.construct_effects()
        out = f"(:action {self.action_name}\n"
        out += f"\t:parameters ({self.parameters})\n"
        out += f"\t:precondition {self.preconditions}\n"
        out += f"\t:effect {self.effects}\n"
        out += ")\n"
        return out




class JumpDown(Action):
    # jumps up one block forward
    def __init__(self, dir: str) -> None:
        super().__init__()
        self.dir = dir
        # self.item_to_pickup = item_to_pickup
        self.action_name = (
            "jumpdown-" + dir
        )  # + "-only" if item_to_pickup is None else "-and-pickup-" + self.item_to_pickup.name

        # have separate dictionaries for parameter names and types, but such that a common key is used to index corresponding values in both
        # this is necessary because multiple parameters have different names but the same type
        self.param_name = {
            "Agent": "?ag",
            "XPosition": "?x",
            "ZPosition": "?z",
            "XPositionStart": "?x_start",
            "XPositionEnd": "?x_end",
            "YPositionUp": "?y_up",
            "YPositionDown": "?y_down", # where legs are
            "YPosition2Down": "?y_2_down", # for jumping down
            "YPosition3Down": "?y_3_down", # for making sure there is landing space
            "ZPositionStart": "?z_start",
            "ZPositionEnd": "?z_end",
        }

        self.param_types = {
            "Agent": TypeName.AGENT_TYPE_NAME.value,
            "XPosition": TypeName.POSITION_TYPE_NAME.value,
            "ZPosition": TypeName.POSITION_TYPE_NAME.value,
            "XPositionStart": TypeName.POSITION_TYPE_NAME.value,
            "XPositionEnd": TypeName.POSITION_TYPE_NAME.value,
            "YPositionUp": TypeName.POSITION_TYPE_NAME.value,
            "YPositionDown": TypeName.POSITION_TYPE_NAME.value,
            "YPosition2Down": TypeName.POSITION_TYPE_NAME.value,
            "YPosition3Down": TypeName.POSITION_TYPE_NAME.value,
            "ZPositionStart": TypeName.POSITION_TYPE_NAME.value,
            "ZPositionEnd": TypeName.POSITION_TYPE_NAME.value,
        }

    def construct_parameters(self):
        # need this generator since extra params have been added to the dicts in order to be more general
        move_east_west = self.dir == "east" or self.dir == "west"
        self.parameters = ""

        # loop through all the parameters and add them to the parameters dict if they are used
        for key in self.param_name.keys():
            # if we move east or west, we use x_start and x_end, but only z
            # if we move north or south, we use z_start and z_end, but only x

            # if we are not dealing with x or z positions, then process as normal
            if not ("XPosition" in key or "ZPosition" in key):
                self.parameters += f"{self.param_name[key]} - {self.param_types[key]} "
                continue

            if key == "XPositionStart" or key == "XPositionEnd" or key == "ZPosition":
                if move_east_west:
                    self.parameters += (
                        f"{self.param_name[key]} - {self.param_types[key]} "
                    )
                else:
                    continue
            elif key == "XPosition" or key == "ZPositionStart" or key == "ZPositionEnd":
                if not move_east_west:
                    self.parameters += (
                        f"{self.param_name[key]} - {self.param_types[key]} "
                    )
                else:
                    continue

        self.parameters = self.parameters.strip()

    def construct_preconditions(self):
        # depending on the direction of travel, we need to check that the end location is not occupied by a block/item
        # we will set the x_start, x_end, z_start, and z_end variables to hold the relevant arg names so we can just look them up later
        move_east_west = self.dir == "east" or self.dir == "west"
        direction_should_increase = self.dir == "south" or self.dir == "east"
        if move_east_west:
            x_start = self.param_name["XPositionStart"]
            x_end = self.param_name["XPositionEnd"]
        else:
            x_start = self.param_name["XPosition"]
            x_end = self.param_name["XPosition"]

        if not move_east_west:
            z_start = self.param_name["ZPositionStart"]
            z_end = self.param_name["ZPositionEnd"]
        else:
            z_start = self.param_name["ZPosition"]
            z_end = self.param_name["ZPosition"]

        # todo: confirm that these orders are correct
        if direction_should_increase:
            sequential_predicate = AreSequentialPredicate.to_precondition(
                x_start if move_east_west else z_start,
                x_end if move_east_west else z_end,
            )
        else:
            sequential_predicate = AreSequentialPredicate.to_precondition(
                x_end if move_east_west else z_end,
                x_start if move_east_west else z_start,
            )

        block_var = "?b"
        item_var = "?i"
        self.preconditions = pddl_and(
            f"({AgentAlivePredicate.var_name} {self.param_name['Agent']})\n",
            AtXLocationPredicate.to_precondition(self.param_name["Agent"], x_start),
            AtYLocationPredicate.to_precondition(
                self.param_name["Agent"],
                self.param_name[
                    "YPositionDown"
                ],  # agent coord is the bottom of the agent
            ),
            AtZLocationPredicate.to_precondition(self.param_name["Agent"], z_start),
            sequential_predicate,
            AreSequentialPredicate.to_precondition(self.param_name["YPosition3Down"], self.param_name["YPosition2Down"]),
            AreSequentialPredicate.to_precondition(self.param_name["YPosition2Down"], self.param_name["YPositionDown"]),
            AreSequentialPredicate.to_precondition(self.param_name["YPositionDown"], self.param_name["YPositionUp"]),
            pddl_not(
                pddl_exists(
                    {TypeName.BLOCK_TYPE_NAME.value: block_var},
                    pddl_and(
                        f"({BlockPresentPredicate.var_name} {block_var})\n",
                        AtXLocationPredicate.to_precondition(block_var, x_end),
                        # here we check that there is no block at the level of the agent (bottom) or the agent's eyeline (top)
                        pddl_or(
                            AtYLocationPredicate.to_precondition(
                                block_var, self.param_name["YPositionUp"]
                            ),
                            AtYLocationPredicate.to_precondition(
                                block_var, self.param_name["YPositionDown"]
                            ),
                            AtYLocationPredicate.to_precondition(
                                block_var, self.param_name["YPosition2Down"]
                            ),
                        ),
                        AtZLocationPredicate.to_precondition(block_var, z_end),
                    ),
                )
            ),
            pddl_exists(
                {TypeName.BLOCK_TYPE_NAME.value: block_var},
                pddl_and(
                    f"({BlockPresentPredicate.var_name} {block_var})\n",
                    AtXLocationPredicate.to_precondition(block_var, x_end),
                    # here we check that there is no block at the level of the agent (bottom) or the agent's eyeline (top)
                    AtYLocationPredicate.to_precondition(block_var, self.param_name["YPosition3Down"]),
                    AtZLocationPredicate.to_precondition(block_var, z_end),
                ),
            ),
            pddl_not(
                pddl_exists(
                    {TypeName.ITEM_TYPE_NAME.value: item_var},
                    pddl_and(
                        f"({ItemPresentPredicate.var_name} {item_var})\n",
                        AtXLocationPredicate.to_precondition(item_var, x_end),
                        # here we only check that there is no item at the level of the agent (bottom) since items cannot float
                        # they would require a block to be placed beneath it, which is handled by the previous precondition
                        pddl_or(
                            AtYLocationPredicate.to_precondition(
                                item_var, self.param_name["YPosition2Down"]
                            ),
                        ),
                        AtZLocationPredicate.to_precondition(item_var, z_end),
                    ),
                )
            ),
        )

    def construct_effects(self):
        # this is as simple as saying that agent is not at the start and is at the end
        if self.dir == "north" or self.dir == "south":
            start = self.param_name["ZPositionStart"]
            end = self.param_name["ZPositionEnd"]
            predicate_to_use = AtZLocationPredicate
        else:
            start = self.param_name["XPositionStart"]
            end = self.param_name["XPositionEnd"]
            predicate_to_use = AtXLocationPredicate

        self.effects = pddl_and(
            pddl_not(predicate_to_use.to_precondition(self.param_name["Agent"], start)),
            predicate_to_use.to_precondition(self.param_name["Agent"], end),
            pddl_not(AtYLocationPredicate.to_precondition(self.param_name["Agent"], self.param_name["YPositionDown"])),
            AtYLocationPredicate.to_precondition(self.param_name["Agent"], self.param_name["YPosition2Down"]),
        )

    def to_pddl(self):
        self.construct_parameters()
        self.construct_preconditions()
        self.construct_effects()
        out = f"(:action {self.action_name}\n"
        out += f"\t:parameters ({self.parameters})\n"
        out += f"\t:precondition {self.preconditions}\n"
        out += f"\t:effect {self.effects}\n"
        out += ")\n"
        return out

class CheckGoal(Action):
    # checks the goal achieved predicate of the agent
    def __init__(self, goal) -> None:
        self.action_name = "check-goal"
        self.parameters = {TypeName.AGENT_TYPE_NAME.value: "?ag"}
        self.goal = goal

    def construct_preconditions(self):
        blocks = self.goal["blocks"]
        inventory = self.goal["inventory"]

        block_pddl = ""
        item_pddl = ""

        for block in blocks:
            block_pddl += pddl_exists(
                {block["type"] + "-block": "?b"},
                pddl_and(
                    pddl_equal(
                        f"({XPositionFunction.var_name} ?b)", block["position"]["x"]
                    ),
                    pddl_equal(
                        f"({YPositionFunction.var_name} ?b)", block["position"]["y"]
                    ),
                    pddl_equal(
                        f"({ZPositionFunction.var_name} ?b)", block["position"]["z"]
                    ),
                ),
            )
            block_pddl += "\n\t"

        for item in inventory:
            # each item in the inventory needs to have at least the specified quantity
            item_pddl += pddl_ge(
                f"({InventoryFunction.var_name.format(item['name'])} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})",
                str(item["quantity"]),
            )

        self.preconditions = pddl_and(block_pddl, item_pddl)

    def construct_effects(self):
        self.effects = pddl_and(
            f"({GoalAchievedPredicate.var_name} {self.parameters[TypeName.AGENT_TYPE_NAME.value]})"
        )

    def to_pddl(self):
        self.construct_preconditions()
        self.construct_effects()
        out = f"(:action {self.action_name}\n"
        out += f"\t:parameters ({' '.join([f'{v} - {k}' for k, v in self.parameters.items()])})\n"
        out += f"\t:precondition {self.preconditions}\n"
        out += f"\t:effect {self.effects}\n"
        out += ")\n"
        return out
