from robodk.robolink import *
from robodk.robomath import *

RDK = Robolink()


class RoboDKBridge:

    def __init__(self):

        self.robots = {}

    # =====================================================
    # CONNECT ROBOT
    # =====================================================

    def connect_robot(

        self,

        robot_name

    ):

        robot = RDK.Item(robot_name)

        if not robot.Valid():

            raise Exception(

                f"Robot not found: {robot_name}"
            )

        self.robots[robot_name] = robot

        return robot

    # =====================================================
    # MOVE ROBOT
    # =====================================================

    def move_robot(

        self,

        robot_name,

        x,

        y,

        z

    ):

        robot = self.robots.get(robot_name)

        if not robot:

            robot = self.connect_robot(
                robot_name
            )

        target = transl(x, y, z)

        robot.MoveL(target)

    # =====================================================
    # HOME
    # =====================================================

    def home(

        self,

        robot_name

    ):

        robot = self.robots.get(robot_name)

        if not robot:

            robot = self.connect_robot(
                robot_name
            )

        home = robot.JointsHome()

        robot.MoveJ(home)