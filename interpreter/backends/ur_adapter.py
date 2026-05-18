from interpreter.backends.base_adapter import BaseAdapter


class URAdapter(BaseAdapter):

    def __init__(self):

        self.lines = []

        self.lines.append("def rcml_program():")

    # =====================================================
    # MOVE
    # =====================================================

    def move(self, cmd, points):

        target = cmd["target"]

        point = points[target]

        x = point["x"] / 1000
        y = point["y"] / 1000
        z = point["z"] / 1000

        self.lines.append(

            f"    movel(p["

            f"{x},{y},{z},"

            f"0,3.14,0"

            f"])"
        )

    # =====================================================
    # HOME
    # =====================================================

    def home(self, cmd):

        self.lines.append(

            "    movej([0,-1.57,1.57,0,1.57,0])"
        )

    # =====================================================
    # GRAB
    # =====================================================

    def grab(self):

        self.lines.append(
            "    # grab"
        )

    # =====================================================
    # RELEASE
    # =====================================================

    def release(self):

        self.lines.append(
            "    # release"
        )

    # =====================================================
    # SAVE
    # =====================================================

    def save(self):

        self.lines.append("")
        self.lines.append("end")

        with open(

            "output/ur.script",

            "w"

        ) as f:

            f.write(

                "\n".join(self.lines)
            )