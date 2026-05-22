from interpreter.backends.kuka_adapter import KukaAdapter
from interpreter.backends.ur_adapter import URAdapter

# RoboDK OPTIONAL
try:

    from simulation.robodk_bridge import RoboDKBridge

    ROBODK_AVAILABLE = True

except:

    ROBODK_AVAILABLE = False


class Dispatcher:

    def __init__(self):

        self.kuka = KukaAdapter()

        self.ur = URAdapter()

        # =============================================
        # OPTIONAL ROBO DK
        # =============================================

        self.sim = None

        if ROBODK_AVAILABLE:

            try:

                self.sim = RoboDKBridge()

            except Exception as e:

                print(

                    "RoboDK init error:",
                    e
                )

    # =====================================================
    # DISPATCH
    # =====================================================

    def dispatch(

        self,

        robot_model,

        cmd,

        points

    ):

        # -------------------------------------------------
        # SELECT ADAPTER
        # -------------------------------------------------

        if "KR" in robot_model:

            adapter = self.kuka

        elif "UR" in robot_model:

            adapter = self.ur

        else:

            raise ValueError(

                f"Unknown robot model: {robot_model}"
            )

        # -------------------------------------------------
        # COMMAND TYPE
        # -------------------------------------------------

        cmd_type = cmd["type"]

        # -------------------------------------------------
        # MOVE
        # -------------------------------------------------

        if cmd_type == "move":

            adapter.move(cmd, points)

            # =============================================
            # OPTIONAL ROBO DK SIMULATION
            # =============================================

            if self.sim:

                try:

                    target = points[cmd["target"]]

                    self.sim.move_robot(

                        cmd["robot"],

                        target["x"],
                        target["y"],
                        target["z"]

                    )

                except Exception as e:

                    print(

                        "RoboDK move error:",
                        e
                    )

        # -------------------------------------------------
        # HOME
        # -------------------------------------------------

        elif cmd_type == "home":

            adapter.home(cmd)

            # OPTIONAL ROBO DK

            if self.sim:

                try:

                    self.sim.home(

                        cmd["robot"]
                    )

                except Exception as e:

                    print(

                        "RoboDK home error:",
                        e
                    )

        # -------------------------------------------------
        # GRAB
        # -------------------------------------------------

        elif cmd_type == "grab":

            adapter.grab()

        # -------------------------------------------------
        # RELEASE
        # -------------------------------------------------

        elif cmd_type == "release":

            adapter.release()

    # =====================================================
    # SAVE ALL
    # =====================================================

    def save_all(self):

        self.kuka.save()

        self.ur.save()