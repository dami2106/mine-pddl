import argparse
from typing import Dict, Tuple


def coords_3d(arg: str) -> Tuple[int, int, int]:
    # check if have ( and ) and remove them
    if arg[0] == "(" and arg[-1] == ")":
        arg = arg[1:-1]

        # split the string into a tuple of ints
        try:
            x, y, z = arg.split(",")
            return (int(x), int(y), int(z))
        except Exception:
            pass  # will raise error later

    raise argparse.ArgumentTypeError(
        "Coords must be in the form (x,y,z), where x, y, z are ints"
    )


def agent_start_position(arg: str) -> Dict[str, float]:
    # check if have ( and ) and remove them
    if arg[0] == "(" and arg[-1] == ")":
        arg = arg[1:-1]

        # split the string into a dict of floats
        try:
            x, y, z = [float(a) for a in arg.split(",")]

            # check if x and z need to be incremented by 0.5 (if not already specified)
            if int(x) + 0.5 != x:
                x = int(x) + 0.5
            if int(z) + 0.5 != z:
                z = int(z) + 0.5

            return {
                "x": x,
                "y": y,
                "z": z,
                "yaw": 0,
                "pitch": 0,
            }
        except Exception:
            pass  # will raise error later

    raise argparse.ArgumentTypeError(
        "Agent start position must be in the form (x,y,z), where x, y, z are numbers"
    )

def window_size(arg: str) -> Tuple[int, int]:
    # check if have ( and ) and remove them
    if arg[0] == "(" and arg[-1] == ")":
        arg = arg[1:-1]

        # split the string into a tuple of ints
        try:
            w, h = arg.split(",")
            return (int(w), int(h))
        except Exception:
            pass  # will raise error later

    raise argparse.ArgumentTypeError(
        "Window size must be in the form (w,h), where w, h are ints"
    )

def no_spaces(arg: str) -> str:
    return arg.replace(" ", "_")

def get_args_parser():
    parser = argparse.ArgumentParser("Mine-PDDL", add_help=True)

    # General stuff
    parser.add_argument(
        "--world-config",
        type=str,
        default="worlds/example.yaml",
        help="path to the description of the world",
    )
    parser.add_argument(
        "--world-name", type=str, default="open-ended", help="Name of the world"
    )
    parser.add_argument(
        "--world-type", type=str, default="flat", help="Type of the world"
    )
    parser.add_argument(
        "--world-seed", type=str, default="Enter the Nether", help="Seed for random generation of world"
    )
    parser.add_argument(
        "--window-size", type=window_size, default="(1024, 1024)", help="Size of the window. Format: (w, h)"
    )
    parser.add_argument(
        "--video-save-path",
        type=str,
        default="problems/our/images",
        help="Path to save the video (of the agent executing the provided plan)",
    )
    parser.add_argument(
        "--video-name", type=str, default="plan_video", help="Name of the video"
    )

    parser.add_argument(
        "--print-valid-types",
        action="store_true",
        help="Print block and item types that can be specified in the YAML config",
    )
    parser.set_defaults(print_valid_types=False)

    # args to generate/process PDDL
    parser.add_argument(
        "--domain-name",
        type=no_spaces,
        default="first_world",
        help="Name of the domain. Spaces will be replaced with underscores",
    )
    parser.add_argument(
        "--problem-name",
        type=no_spaces,
        default="first_world_problem",
        help="Name of the problem. Spaces will be replaced with underscores",
    )
    parser.add_argument(
        "--domain-file",
        type=str,
        default="./problems/our/domain_prop3.pddl",
        help="path to the PDDL domain file (note that this may be overwritten)",
    )
    parser.add_argument(
        "--problem-file",
        type=str,
        default="./problems/our/problem_prop3.pddl",
        help="path to the PDDL problem file (note that this may be overwritten)",
    )
    parser.add_argument(
        "--plan-file",
        type=str,
        default="./problems/our/plan.pddl",
        help="path to the PDDL plan file (note that this may be overwritten)",
    )

    # args to generate propositional or numerical PDDL
    parser.add_argument(
        "--pddl-type",
        type=str,
        choices=["propositional", "numerical"],
        help="specify if the PDDL files are propositional or numerical",
    )

    # args to define variables pertinent to the world
    parser.add_argument(
        "--max-inventory-stack",
        type=int,
        default=64,
        help="max stack size for inventory items",
    )
    parser.add_argument(
        "--observation-range",
        type=coords_3d,  # this a type conversion function
        default=(8, 4, 8),
        help="observation range of the agent in the form (x, y, z). Each component is the total range in that direction, where the agent is at the center",
    )
    parser.add_argument(
        "--agent-start-position",
        type=agent_start_position,
        default=(0.5, 4, 0.5),
        help="agent start position in the form (x, y, z), where x, y, z are numbers",
    )

    return parser
