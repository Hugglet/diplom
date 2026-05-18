from interpreter.backends.base_adapter import BaseAdapter


class KukaAdapter(BaseAdapter):

    def __init__(self):

        self.lines = []

        self.dat_lines = []

        # =========================================
        # SRC HEADER
        # =========================================

        self.lines.append("&ACCESS RVP")
        self.lines.append("&REL 1")
        self.lines.append("")
        self.lines.append("DEF rcml_auto()")
        self.lines.append("")
        self.lines.append("PTP HOME")
        self.lines.append("")

        # =========================================
        # DAT HEADER
        # =========================================

        self.dat_lines.append("DEFDAT rcml_auto")
        self.dat_lines.append("")

    # =====================================================
    # MOVE
    # =====================================================

    def move(self, cmd, points):

        target = cmd["target"]

        point = points[target]

        # ---------------------------------------------
        # DAT POSITION
        # ---------------------------------------------

        self.dat_lines.append(

            f"DECL E6POS {target.upper()}={{"

            f"X {point['x']},"

            f"Y {point['y']},"

            f"Z {point['z']}"

            f"}}"
        )

        # ---------------------------------------------
        # SRC COMMAND
        # ---------------------------------------------

        self.lines.append(

            f"LIN {target.upper()}"
        )

    # =====================================================
    # HOME
    # =====================================================

    def home(self, cmd):

        self.lines.append("PTP HOME")

    # =====================================================
    # GRAB
    # =====================================================

    def grab(self):

        self.lines.append("; GRAB")

    # =====================================================
    # RELEASE
    # =====================================================

    def release(self):

        self.lines.append("; RELEASE")

    # =====================================================
    # SAVE FILES
    # =====================================================

    def save(self):

        # SRC END

        self.lines.append("")
        self.lines.append("END")

        # DAT END

        self.dat_lines.append("")
        self.dat_lines.append("ENDDAT")

        # SAVE SRC

        with open(

            "output/kuka.src",

            "w"

        ) as f:

            f.write(

                "\n".join(self.lines)
            )

        # SAVE DAT

        with open(

            "output/kuka.dat",

            "w"

        ) as f:

            f.write(

                "\n".join(self.dat_lines)
            )