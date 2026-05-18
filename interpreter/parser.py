from interpreter.lexer import tokenize


def parse_line(line: str):

    line = line.strip()

    # пустые строки
    if not line:
        return None

    # комментарии
    if line.startswith("#"):
        return None

    tokens = tokenize(line)

    if not tokens:
        return None

    # =========================================================
    # ROBOT
    # robot kuka KR150
    # =========================================================

    if line.startswith("robot"):

        if len(tokens) < 3:
            raise ValueError("Invalid robot declaration")

        return {
            "type": "robot",
            "name": tokens[1],
            "model": tokens[2]
        }

    # =========================================================
    # POINT
    # point pick (100,200,300)
    # =========================================================

    elif line.startswith("point"):

        try:
            parts = line.split()

            name = parts[1]

            coords = line[line.find("(") + 1: line.find(")")]

            x, y, z = coords.split(",")

            return {
                "type": "point",
                "name": name,
                "x": float(x),
                "y": float(y),
                "z": float(z)
            }

        except Exception:
            raise ValueError("Invalid point syntax")

    # =========================================================
    # TASK
    # task loading {
    # =========================================================

    elif line.startswith("task"):

        parts = line.split()

        if len(parts) < 2:
            raise ValueError("Invalid task declaration")

        return {
            "type": "task",
            "name": parts[1]
        }

    # =========================================================
    # END TASK BLOCK
    # }
    # =========================================================

    elif line == "}":

        return {
            "type": "task_end"
        }

    # =========================================================
    # kuka.move pick
    # ur.move home
    # =========================================================

    elif ".move" in line:

        try:
            left, target = line.split()

            robot = left.split(".")[0]

            return {
                "type": "move",
                "robot": robot,
                "target": target
            }

        except Exception:
            raise ValueError("Invalid move syntax")

    # =========================================================
    # kuka.grab
    # =========================================================

    elif ".grab" in line:

        robot = line.split(".")[0]

        return {
            "type": "grab",
            "robot": robot
        }

    # =========================================================
    # kuka.release
    # =========================================================

    elif ".release" in line:

        robot = line.split(".")[0]

        return {
            "type": "release",
            "robot": robot
        }

    # =========================================================
    # kuka.home
    # ur.home
    # =========================================================

    elif ".home" in line:

        robot = line.split(".")[0]

        return {
            "type": "home",
            "robot": robot
        }

    # =========================================================
    # wait 2
    # =========================================================

    elif line.startswith("wait"):

        parts = line.split()

        if len(parts) != 2:
            raise ValueError("Invalid wait syntax")

        return {
            "type": "wait",
            "time": int(parts[1])
        }

    # =========================================================
    # sync
    # =========================================================

    elif line == "sync":

        return {
            "type": "sync"
        }

    # =========================================================
    # parallel {
    # =========================================================

    elif line.startswith("parallel"):

        return {
            "type": "parallel_start"
        }

    # =========================================================
    # LEGACY MOVE
    # MOVE X=100 Y=200 Z=300 SPEED=50
    # =========================================================

    elif tokens[0] == "MOVE":

        args = {}
        i = 1

        while i < len(tokens):

            key = tokens[i]

            if i + 2 >= len(tokens):
                raise ValueError("Invalid MOVE syntax")

            if tokens[i + 1] != "=":
                raise ValueError("Expected '='")

            value = tokens[i + 2]

            # int
            if value.isdigit():
                value = int(value)

            args[key] = value

            i += 3

        # defaults
        if "TYPE" not in args:
            args["TYPE"] = "LIN"

        if "SPEED" not in args:
            args["SPEED"] = 100

        # validation
        if not (0 <= args.get("X", 0) <= 2000):
            raise ValueError("X out of range")

        if not (0 <= args.get("Y", 0) <= 2000):
            raise ValueError("Y out of range")

        if not (0 <= args.get("Z", 0) <= 2000):
            raise ValueError("Z out of range")

        if not (0 < args.get("SPEED", 100) <= 100):
            raise ValueError("Invalid SPEED (1-100)")

        return {
            "cmd": "MOVE",
            "args": args
        }

    # =========================================================
    # LEGACY PICK
    # =========================================================

    elif tokens[0] == "PICK":

        args = {}
        i = 1

        while i < len(tokens):

            key = tokens[i]

            if tokens[i + 1] != "=":
                raise ValueError("Expected '='")

            value = int(tokens[i + 2])

            args[key] = value

            i += 3

        return {
            "cmd": "PICK",
            "args": args
        }

    # =========================================================
    # LEGACY PLACE
    # =========================================================

    elif tokens[0] == "PLACE":

        args = {}
        i = 1

        while i < len(tokens):

            key = tokens[i]

            if tokens[i + 1] != "=":
                raise ValueError("Expected '='")

            value = int(tokens[i + 2])

            args[key] = value

            i += 3

        return {
            "cmd": "PLACE",
            "args": args
        }

    # =========================================================
    # LEGACY GRIP
    # =========================================================

    elif tokens[0] == "GRIP":

        if len(tokens) < 2:
            raise ValueError("GRIP requires state")

        return {
            "cmd": "GRIP",
            "state": tokens[1]
        }

    # =========================================================
    # LEGACY WAIT
    # =========================================================

    elif tokens[0] == "WAIT":

        if len(tokens) < 2:
            raise ValueError("WAIT requires time")

        return {
            "cmd": "WAIT",
            "time": int(tokens[1])
        }

    # =========================================================
    # UNKNOWN
    # =========================================================

    else:
        raise ValueError(f"Unknown command: {line}")