from robodk.robolink import Robolink
from robodk.robomath import transl

import os
import subprocess
import time


class RoboDKBridge:

    def __init__(self):

        try:

            # =============================================
            # ROBO DK EXECUTABLE
            # =============================================

            robodk_exe = (

                r"C:\RoboDK\bin\RoboDK.exe"
            )

            # =============================================
            # SCENE
            # =============================================

            self.scene_path = (

                r"C:\SUAI\Diplom\Scenes\R-SUAI_conveyor.rdk"
            )

            # =============================================
            # START ROBO DK
            # =============================================

            subprocess.Popen([

                robodk_exe,

                self.scene_path
            ])

            print(

                "\nStarting RoboDK..."
            )

            # =============================================
            # WAIT STARTUP
            # =============================================

            time.sleep(5)

            # =============================================
            # CONNECT API
            # =============================================

            self.RDK = Robolink()

            print(

                "\nRoboDK connected"
            )

            # =============================================
            # RUN MAIN PROGRAM
            # =============================================

            main_program = self.RDK.Item(

                "MAIN_SCENE"
            )

            if main_program.Valid():

                print(

                    "\nRunning MAIN_SCENE"
                )

                main_program.RunProgram()

            else:

                print(

                    "\nMAIN_SCENE not found"
                )

        except Exception as e:

            print(

                "\nRoboDK connection error:",
                e
            )

            self.RDK = None

    # =====================================================
    # GET ROBOT
    # =====================================================

    def get_robot(

        self,

        robot_name

    ):

        if self.RDK is None:

            return None

        robot = self.RDK.Item(

            robot_name
        )

        if not robot.Valid():

            print(

                f"\nRobot not found: {robot_name}"
            )

            return None

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

        try:

            robot = self.get_robot(

                robot_name
            )

            if robot is None:

                return

            target = transl(

                x,
                y,
                z
            )

            robot.MoveJ(target)

            print(

                f"\n{robot_name} moved to",

                x, y, z
            )

        except Exception as e:

            print(

                "\nRoboDK move error:",
                e
            )

    # =====================================================
    # MOVE HOME
    # =====================================================

    def move_home(

        self,

        robot_name

    ):

        try:

            robot = self.get_robot(

                robot_name
            )

            if robot is None:

                return

            robot.MoveJ(

                robot.JointsHome()
            )

            print(

                f"\n{robot_name} HOME"
            )

        except Exception as e:

            print(

                "\nRoboDK home error:",
                e
            )