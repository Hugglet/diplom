from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

import os

from interpreter.lark_parser import parse_rcml
from interpreter.dispatcher import Dispatcher

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
# RUN RCML
# =========================================================

@app.route("/run", methods=["POST"])
def run_rcml():

    try:

        data = request.get_json()

        rcml_code = data.get("code", "")

        # =================================================
        # REGISTRIES
        # =================================================

        robots = {}
        points = {}

        parallel_mode = False

        dispatcher = Dispatcher()

        # =================================================
        # PARSE RCML
        # =================================================

        ast = parse_rcml(rcml_code)

        # =================================================
        # EXECUTE AST
        # =================================================

        for cmd in ast:

            # =============================================
            # ROBOT
            # =============================================

            if cmd["type"] == "robot":

                robots[cmd["name"]] = cmd["model"]

            # =============================================
            # POINT
            # =============================================

            elif cmd["type"] == "point":

                points[cmd["name"]] = {

                    "x": cmd["x"],
                    "y": cmd["y"],
                    "z": cmd["z"]

                }

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

                robot_model = robots.get(robot_name)

                if not robot_model:

                    raise ValueError(

                        f"Unknown robot: {robot_name}"
                    )

                dispatcher.dispatch(

                    robot_model,
                    cmd,
                    points

                )

        # =================================================
        # SAVE OUTPUT FILES
        # =================================================

        dispatcher.save_all()

        # =================================================
        # READ GENERATED FILES
        # =================================================

        # ---------------------------------------------
        # KUKA SRC
        # ---------------------------------------------

        if os.path.exists("output/kuka.src"):

            with open("output/kuka.src") as f:

                kuka_src = f.read()

        else:

            kuka_src = ""

        # ---------------------------------------------
        # KUKA DAT
        # ---------------------------------------------

        if os.path.exists("output/kuka.dat"):

            with open("output/kuka.dat") as f:

                kuka_dat = f.read()

        else:

            kuka_dat = ""

        # ---------------------------------------------
        # UR SCRIPT
        # ---------------------------------------------

        if os.path.exists("output/ur.script"):

            with open("output/ur.script") as f:

                ur_script = f.read()

        else:

            ur_script = ""

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

        return jsonify({

            "success": False,

            "error": str(e)
        })


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    app.run(debug=True)