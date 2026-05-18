from interpreter.backends.base_adapter import BaseAdapter


class URAdapter(BaseAdapter):

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
                f"movej([{x},{y},{z}])"
            )

        elif command["type"] == "grab":

            self.program.append(
                "set_digital_out(0, True)"
            )

        elif command["type"] == "release":

            self.program.append(
                "set_digital_out(0, False)"
            )

        elif command["type"] == "home":

            self.program.append(
                "movej(home)"
            )

    def save(self, filename):

        with open(filename, "w") as f:

            for line in self.program:
                f.write(line + "\n")