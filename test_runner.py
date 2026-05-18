from interpreter.parser import parse_line
from interpreter.dispatcher import Dispatcher

robots = {}
points = {}

parallel_mode = False

dispatcher = Dispatcher()

with open("examples/demo.rcml") as f:

    lines = f.readlines()

for line in lines:

    line = line.strip()

    if not line:
        continue

    print("\nRCML:", line)

    try:

        cmd = parse_line(line)

        if not cmd:
            continue

        print("PARSED:", cmd)

        # ----------------------------------
        # ROBOT
        # ----------------------------------

        if cmd["type"] == "robot":

            robots[cmd["name"]] = cmd["model"]

            print("REGISTER ROBOT:", robots)

        # ----------------------------------
        # POINT
        # ----------------------------------

        elif cmd["type"] == "point":

            points[cmd["name"]] = {
                "x": cmd["x"],
                "y": cmd["y"],
                "z": cmd["z"]
            }

            print("REGISTER POINT:", points)

        # ----------------------------------
        # TASK
        # ----------------------------------

        elif cmd["type"] == "task":

            print(f"TASK START: {cmd['name']}")

        # ----------------------------------
        # TASK END
        # ----------------------------------

        elif cmd["type"] == "task_end":

            if parallel_mode:

                parallel_mode = False

                print("PARALLEL BLOCK END")

            else:

                print("TASK END")

        # ----------------------------------
        # PARALLEL START
        # ----------------------------------

        elif cmd["type"] == "parallel_start":

            parallel_mode = True

            print("PARALLEL BLOCK START")

        # ----------------------------------
        # PARALLEL END
        # ----------------------------------

        elif cmd["type"] == "task_end":

            if parallel_mode:

                parallel_mode = False

                print("PARALLEL BLOCK END")

            else:

                print("TASK END")

        # ----------------------------------
        # MOVE / GRAB / RELEASE / HOME
        # ----------------------------------

        elif cmd["type"] in [
            "move",
            "grab",
            "release",
            "home"
        ]:

            cmd["parallel"] = parallel_mode

            robot_name = cmd["robot"]

            robot_model = robots.get(robot_name)

            if not robot_model:
                raise ValueError(f"Unknown robot: {robot_name}")

            generated = dispatcher.dispatch(
                robot_model,
                cmd,
                points
            )

            print("GENERATED:")
            print(generated)

        # ----------------------------------
        # WAIT
        # ----------------------------------

        elif cmd["type"] == "wait":

            print(f"WAIT {cmd['time']} sec")

        # ----------------------------------
        # SYNC
        # ----------------------------------

        elif cmd["type"] == "sync":

            print("SYNC ALL ROBOTS")

    except Exception as e:

        print("ERROR:", e)

dispatcher.save_all()

print("\nFILES GENERATED")