from interpreter.backends.base_adapter import BaseAdapter


class KukaAdapter(BaseAdapter):

    def __init__(self):

        self.program = []

    def execute(self, command, points):

        if command["type"] == "move":

            target = command["target"]

            point = points.get(target)

            if not point:
                raise ValueError(f"Unknown point: {target}")

            x = point["x"]
            y = point["y"]
            z = point["z"]

            self.program.append(
                f"PTP {{X {x},Y {y},Z {z}}}"
            )

        elif command["type"] == "grab":

            self.program.append(
                "GRIPPER_CLOSE"
            )

        elif command["type"] == "release":

            self.program.append(
                "GRIPPER_OPEN"
            )

        elif command["type"] == "home":

            self.program.append(
                "PTP HOME"
            )

    def save(self, filename):

        with open(filename, "w") as f:

            f.write("&ACCESS RVP\n")
            f.write("&REL 1\n\n")

            for line in self.program:
                f.write(line + "\n")