from typing import Dict, Optional
from minedojo.sim.wrappers.ar_nn.ar_nn_wrapper import ARNNWrapper

import numpy as np
from pddl.pddl_types.base_pddl_types import AgentType
from pddl.functions import XPositionFunction, YPositionFunction, ZPositionFunction

# TODO: If we ever implement drop, we need to remember that dropped items don't get the NBT tag for presistance


def read_plan(plan_path: str):
    """
    Read the plan from the pddl file
    Each line has the following format: <action no.>: (<action name> <action args>)
    """

    action_sequence = []
    with open(plan_path, "r") as file:
        for line in file:
            if line[0] == ";":
                continue

            action_sequence.append(
                line.split(":")[1].strip().split(" ")[0].strip("(")
            )  # )

    return action_sequence


def move_command(
    env,
    direction: str,
    jump_dir: int,
    agent: AgentType,
):
    """
    Move the agent in the environment by using teleport command
    """

    command = ""
    if direction == "south":
        command = "/tp @p {} {} {}".format(
            agent.functions[XPositionFunction].value,
            agent.functions[YPositionFunction].value + jump_dir,
            agent.functions[ZPositionFunction].value + 1,
        )
    elif direction == "north":
        command = "/tp @p {} {} {}".format(
            agent.functions[XPositionFunction].value,
            agent.functions[YPositionFunction].value + jump_dir,
            agent.functions[ZPositionFunction].value - 1,
        )
    elif direction == "east":
        command = "/tp @p {} {} {}".format(
            agent.functions[XPositionFunction].value + 1,
            agent.functions[YPositionFunction].value + jump_dir,
            agent.functions[ZPositionFunction].value,
        )
    elif direction == "west":
        command = "/tp @p {} {} {}".format(
            agent.functions[XPositionFunction].value - 1,
            agent.functions[YPositionFunction].value + jump_dir,
            agent.functions[ZPositionFunction].value,
        )

    env.execute_cmd(command)


def place_block(env, block_name: str, agent: AgentType) -> None:
    """
    set the desired block to be one in front and one below the player
    """

    # place the block in the world
    # example command: /setblock <x> <y> <z> <new block name> [variation] [oldBlockHandling:default=replace] [dataTag (for new block)]
    command = "/setblock {} {} {} {}".format(
        agent.functions[XPositionFunction].value,
        agent.functions[YPositionFunction].value,
        agent.functions[ZPositionFunction].value + 1,
        block_name,
    )
    env.execute_cmd(command)

    # decrement this block from the agent's inventory
    # https://www.digminecraft.com/game_commands/clear_command.php
    # example command: /clear [targets] [item] [data - variant] [maxCount] [dataTag]
    # example: /clear @a tnt 0 10
    command = f"/clear @a {block_name} 0 1"
    env.execute_cmd(command)


def break_block(env, block_name: str, agent: AgentType) -> None:
    """
    break a block in front of the agent
    """

    # https://www.digminecraft.com/game_commands/setblock_command.php
    command = "/setblock {} {} {} {}".format(
        agent.functions[XPositionFunction].value,
        agent.functions[YPositionFunction].value,
        agent.functions[ZPositionFunction].value + 1,
        "air",
    )
    env.execute_cmd(command)

    # decrement this block from the agent's inventory
    # https://www.digminecraft.com/game_commands/clear_command.php
    # example command: /clear [targets] [item] [data - variant] [maxCount] [dataTag]
    # example: /clear @a tnt 0 10
    command = f"/give @p {block_name}"
    env.execute_cmd(command)


def jump(env, direction, agent):
    """
    direction up = tp one up and one in front
    direction down = tp one behind and one down
    """

    if direction == "up":
        command = "/tp @p {} {} {}".format(
            agent.functions[XPositionFunction].value,
            agent.functions[YPositionFunction].value + 1,
            agent.functions[ZPositionFunction].value - 1,
        )
    elif direction == "down":
        command = "/tp @p {} {} {}".format(
            agent.functions[XPositionFunction].value,
            agent.functions[YPositionFunction].value - 1,
            agent.functions[ZPositionFunction].value + 1,
        )
    else:
        raise ValueError("direction must be either 'up' or 'down'")

    env.execute_cmd(command)


# def drop(env, item_name, inventory, action_vector):
#     """
#     remove the item from the agent's inventory and spawn the item into the world
#     """

#     # equip the relevant inventory slot
#     action_vector[5] = 5
#     for i, name in enumerate(inventory["name"]):
#         if name == item_name:
#             action_vector[7] = i
#             break
#     env.step(action_vector)
#     action_vector[5] = 2
#     return action_vector


def get_prop_action_from_str(
    action: str, agent: AgentType, env: ARNNWrapper, inventory: Optional[Dict] = None
):
    """
    Formulate the action vector from the pddl action string
    """
    action_vector = env.action_space.no_op()
    # split by first hyphen
    action_name, action_args = action.split("-", 1)
    if action_name == "move":
        move_command(env, action_args, 0, agent)
    elif action_name == "jumpup":
        move_command(env, action_args, 1, agent)
    elif action_name == "jumpdown":
        move_command(env, action_args, -1, agent)
    elif action_name == "place":
        # eg action is "place-obsidian"
        # action_args will be "obsidian"
        place_block(env, action_args, agent)
    elif action_name == "break":
        break_block(env, action_args, agent)
    elif action_name == "drop":
        assert inventory is not None
        action_vector[5] = 2
        for i, name in enumerate(inventory["name"]):
            if name == action_args:
                action_vector[7] = i
                break

    return action_vector


def get_action_from_str(
    action: str, agent: AgentType, env: ARNNWrapper, inventory: Optional[Dict] = None
):
    """
    Formulate the action vector from the pddl action string
    """
    action_vector = env.action_space.no_op()
    # split by first hyphen
    action_name, action_args = action.split("-", 1)
    if action_name == "move":
        move_command(env, action_args, 0, agent)
    elif action_name == "place":
        # eg action is "place-obsidian"
        # action_args will be "obsidian"
        place_block(env, action_args, agent)
    elif action_name == "break":
        break_block(env, action_args, agent)
    elif action_name == "jump":
        jump(env, action_args, agent)
    elif action_name == "drop":
        assert inventory is not None
        action_vector[5] = 2
        for i, name in enumerate(inventory["name"]):
            if name == action_args:
                action_vector[7] = i
                break

    return action_vector


def check_goal_state(obs, voxel_size, goal):
    agent_pos = obs["location_stats"]["pos"].astype(int)

    # loop over all the blocks in the goal and check if they are present
    for block in goal["blocks"]:
        block_position = block["position"]

        relative_position = (
            np.array(
                [
                    int(block_position["x"]),
                    int(block_position["y"]),
                    int(block_position["z"]),
                ]
            )
            - agent_pos
        )
        relative_position += np.array(
            [
                (voxel_size["xmax"] - voxel_size["xmin"]) // 2,
                (voxel_size["ymax"] - voxel_size["ymin"]) // 2,
                (voxel_size["zmax"] - voxel_size["zmin"]) // 2,
            ]
        )

        actual = obs["voxels"]["block_name"][
            relative_position[0], relative_position[1], relative_position[2]
        ]
        if actual != block["type"]:
            return False

    # loop over all the inventory items in the goal and check if they are present
    for inv_item in goal["inventory"]:
        for i, name in enumerate(obs["inventory"]["name"]):
            if name == inv_item["type"]:
                if obs["inventory"]["quantity"][i] < inv_item["quantity"]:
                    return False
                break

    return True
