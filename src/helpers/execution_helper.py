import numpy as np

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
            action_sequence.append(line.split(":")[1].strip().split(" ")[0].strip("("))
    return action_sequence

def move_command(env, direction: str):
    """
    Move the agent in the environment by using teleport command
    """
    if direction == "south":
        env.execute_cmd("/tp @p ~ ~ ~1")
    elif direction == "north":
        env.execute_cmd("/tp @p ~ ~ ~-1")
    elif direction == "east":
        env.execute_cmd("/tp @p ~1 ~ ~")
    elif direction == "west":
        env.execute_cmd("/tp @p ~-1 ~ ~") 
    

def get_action_from_str(action: str, inventory, env):
    """
    Formulate the action vector from the pddl action string
    """
    action_vector = env.action_space.no_op()
    # split by first hyphen
    action_name, action_args = action.split("-", 1)
    if action_name == "move":
        move_command(env, action_args)
    elif action_name =="drop":
        action_vector[5] = 2
        for i, name in enumerate(inventory['name']):
            if name == action_args:
                action_vector[7] = i
                break
    
    return action_vector

def check_goal_state(obs, voxel_size, goal):
    agent_pos = obs["location_stats"]["pos"].astype(int)

    # loop over all the blocks in the goal and check if they are present
    for block in goal["blocks"]:
        block_position = block["position"]

        relative_position = np.array([int(block_position['x']), int(block_position['y']), int(block_position['z'])]) - agent_pos
        relative_position += np.array([(voxel_size['xmax']-voxel_size['xmin'])//2, (voxel_size['ymax']-voxel_size['ymin'])//2, (voxel_size['zmax']-voxel_size['zmin'])//2])

        actual = obs["voxels"]["block_name"][relative_position[0], relative_position[1], relative_position[2]]
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





    


