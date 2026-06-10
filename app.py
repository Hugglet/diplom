from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

import os

from interpreter.lark_parser import parse_rcml
from interpreter.dispatcher import Dispatcher
from interpreter.scheduler import Scheduler
from simulation.robodk_bridge import RoboDKBridge

app = Flask(__name__)


# =========================================================
# INDEX
# =========================================================

@app.route("/")
def index():

    return render_template(

        "index.html",

        kuka_src="",

        kuka_dat="",

        ur_script=""
    )

# =========================================================
# SIMULATE
# =========================================================

@app.route("/simulate", methods=["POST"])
def simulate():

    try:

        data = request.get_json()

        rcml_code = data.get("code", "")

        ast = parse_rcml(rcml_code)

        robots = {}
        points = {}

        sim = RoboDKBridge()

        # =================================================
        # EXECUTE
        # =================================================

        for cmd in ast:

            # ---------------------------------------------
            # ROBOTS
            # ---------------------------------------------

            if cmd["type"] == "robot":

                robots[cmd["name"]] = cmd["model"]

            # ---------------------------------------------
            # POINTS
            # ---------------------------------------------

            elif cmd["type"] == "point":

                points[cmd["name"]] = {

                    "x": cmd["x"],
                    "y": cmd["y"],
                    "z": cmd["z"]
                }

            # ---------------------------------------------
            # MOVE
            # ---------------------------------------------

            elif cmd["type"] == "move":

                target = points[cmd["target"]]

                sim.move_robot(

                    cmd["robot"],

                    target["x"],
                    target["y"],
                    target["z"]
                )

            # ---------------------------------------------
            # HOME
            # ---------------------------------------------

            elif cmd["type"] == "home":

                sim.move_home(

                    cmd["robot"]
                )

        return jsonify({

            "success": True
        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)
        })

# =========================================================
# RUN RCML
# =========================================================

@app.route("/run", methods=["POST"])
def run_rcml():

    try:

        # =================================================
        # GET JSON
        # =================================================

        data = request.get_json()

        if not data:

            return jsonify({

                "success": False,

                "error": "No JSON received"
            })

        # =================================================
        # GET RCML CODE
        # =================================================

        rcml_code = data.get("code", "")

        print("\n========== RCML ==========")
        print(rcml_code)

        # =================================================
        # REGISTRIES
        # =================================================

        robots = {}
        points = {}

        parallel_mode = False

        dispatcher = Dispatcher()

        scheduler = Scheduler()

        # =================================================
        # PARSE RCML
        # =================================================

        ast = parse_rcml(rcml_code)

        print("\n========== AST ==========")
        print(ast)

        # =================================================
        # EXECUTE AST
        # =================================================

        for cmd in ast:

            print("\nCMD:", cmd)

            # =============================================
            # ROBOT
            # =============================================

            if cmd["type"] == "robot":

                robots[cmd["name"]] = cmd["model"]

                print("REGISTER ROBOT:", robots)

            # =============================================
            # POINT
            # =============================================

            elif cmd["type"] == "point":

                points[cmd["name"]] = {

                    "x": cmd["x"],
                    "y": cmd["y"],
                    "z": cmd["z"]

                }

                print("REGISTER POINT:", points)

            # =============================================
            # TASK START
            # =============================================

            elif cmd["type"] == "task":

                pass

            # =============================================
            # PARALLEL START
            # =============================================

            elif cmd["type"] == "parallel_start":

                parallel_mode = True

            # =============================================
            # TASK END
            # =============================================

            elif cmd["type"] == "task_end":

                parallel_mode = False

            # =============================================
            # SYNC
            # =============================================

            elif cmd["type"] == "sync":

                print("SYNC")

            # =============================================
            # WAIT
            # =============================================

            elif cmd["type"] == "wait":

                print("WAIT:", cmd["time"])

            # =============================================
            # EXECUTION COMMANDS
            # =============================================

            elif cmd["type"] in [

                "move",
                "grab",
                "release",
                "home"

            ]:

                cmd["parallel"] = parallel_mode

                robot_name = cmd["robot"]

                print("ROBOT:", robot_name)

                # =========================================
                # AUTO ROBOT SELECTION
                # =========================================

                if robot_name == "auto":

                    try:

                        target = points[cmd["target"]]

                        task = {

                            "dimensions": 1.0,
                            "mass": 1.0,
                            "time": 5.0,
                            "singularity": 0.2
                        }

                        selected_robot = scheduler.choose_robot(

                            task,
                            target
                        )

                        print(

                            "\nAUTO SELECTED:",
                            selected_robot
                        )

                        robot_name = selected_robot

                        cmd["robot"] = selected_robot

                    except Exception as e:

                        print(

                            "\nSCHEDULER ERROR:",
                            e
                        )

                        robot_name = "kuka"

                        cmd["robot"] = "kuka"

                # =========================================
                # GET ROBOT MODEL
                # =========================================

                robot_model = robots.get(robot_name)

                print("MODEL:", robot_model)

                if not robot_model:

                    raise ValueError(

                        f"Unknown robot: {robot_name}"
                    )

                # =========================================
                # DISPATCH
                # =========================================

                dispatcher.dispatch(

                    robot_model,
                    cmd,
                    points
                )

        # =================================================
        # SAVE GENERATED FILES
        # =================================================

        dispatcher.save_all()

        # =================================================
        # OUTPUTS
        # =================================================

        kuka_src = ""
        kuka_dat = ""
        ur_script = ""

        # =============================================
        # KUKA SRC
        # =============================================

        if os.path.isfile("output/kuka.src"):

            with open(

                "output/kuka.src",

                "r",

                encoding="utf-8"

            ) as f:

                kuka_src = f.read()

        # =============================================
        # KUKA DAT
        # =============================================

        if os.path.isfile("output/kuka.dat"):

            with open(

                "output/kuka.dat",

                "r",

                encoding="utf-8"

            ) as f:

                kuka_dat = f.read()

        # =============================================
        # UR SCRIPT
        # =============================================

        if os.path.isfile("output/ur.script"):

            with open(

                "output/ur.script",

                "r",

                encoding="utf-8"

            ) as f:

                ur_script = f.read()

        # =================================================
        # RETURN JSON
        # =================================================

        return jsonify({

            "success": True,

            "kuka_src": kuka_src,

            "kuka_dat": kuka_dat,

            "ur_script": ur_script
        })

    except Exception as e:

        print("\n========== ERROR ==========")
        print(e)

        return jsonify({

            "success": False,

            "error": str(e)
        })


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    app.run(debug=True)