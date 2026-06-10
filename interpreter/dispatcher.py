from interpreter.backends.kuka_adapter import KukaAdapter
from interpreter.backends.ur_adapter import URAdapter


class Dispatcher:

    def __init__(self):

        self.kuka = KukaAdapter()

        self.ur = URAdapter()

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

        # -------------------------------------------------
        # HOME
        # -------------------------------------------------

        elif cmd_type == "home":

            adapter.home(cmd)

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

        # -------------------------------------------------
        # WAIT
        # -------------------------------------------------

        elif cmd_type == "wait":

            pass

        # -------------------------------------------------
        # SYNC
        # -------------------------------------------------

        elif cmd_type == "sync":

            pass

    # =====================================================
    # SAVE ALL
    # =====================================================

    def save_all(self):

        self.kuka.save()

        self.ur.save()