def to_krl(command: dict):
    if command["cmd"] == "MOVE":
        args = command["args"]

        x = args.get("X", 0)
        y = args.get("Y", 0)
        z = args.get("Z", 0)

        speed = args.get("SPEED", 100)
        move_type = args.get("TYPE", "LIN")

        if move_type == "LIN":
            return f"LIN {{X {x}, Y {y}, Z {z}}} C_DIS ; speed={speed}"

        elif move_type == "PTP":
            return f"PTP {{X {x}, Y {y}, Z {z}}} ; speed={speed}"

        else:
            return "; UNKNOWN MOVE TYPE"

    elif command["cmd"] == "GRIP":
        if command["state"] == "OPEN":
            return "GRIPPER_OPEN()"
        else:
            return "GRIPPER_CLOSE()"

    elif command["cmd"] == "WAIT":
        return f"WAIT SEC {command['time']}"
    
    elif command["cmd"] == "PICK":
        x = command["args"].get("X", 0)
        y = command["args"].get("Y", 0)
        z = command["args"].get("Z", 0)

        return (
            f"LIN {{X {x}, Y {y}, Z {z + 100}}}\n"  # подлет сверху
            f"LIN {{X {x}, Y {y}, Z {z}}}\n"
            f"GRIPPER_CLOSE()\n"
            f"LIN {{X {x}, Y {y}, Z {z + 100}}}"
    )

    elif command["cmd"] == "PLACE":
        x = command["args"].get("X", 0)
        y = command["args"].get("Y", 0)
        z = command["args"].get("Z", 0)

        return (
            f"LIN {{X {x}, Y {y}, Z {z + 100}}}\n"
            f"LIN {{X {x}, Y {y}, Z {z}}}\n"
            f"GRIPPER_OPEN()\n"
            f"LIN {{X {x}, Y {y}, Z {z + 100}}}"
        )
    
    else:
        return "; UNKNOWN COMMAND"