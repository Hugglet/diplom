from flask import Flask, render_template, request

from interpreter.lark_parser import parse_rcml
from interpreter.dispatcher import Dispatcher

app = Flask(__name__)


# =========================================================
# MAIN PAGE
# =========================================================

@app.route("/", methods=["GET", "POST"])
def index():

    kuka_code = ""
    ur_code = ""

    # =====================================================
    # RUN RCML
    # =====================================================

    if request.method == "POST":

        try:

            # -------------------------------------------------
            # GET RCML CODE
            # -------------------------------------------------

            rcml_code = request.form.get("rcml", "")

            # -------------------------------------------------
            # REGISTRIES
            # -------------------------------------------------

            robots = {}
            points = {}

            parallel_mode = False

            dispatcher = Dispatcher()

            # -------------------------------------------------
            # PARSE RCML
            # -------------------------------------------------

            ast = parse_rcml(rcml_code)

            # -------------------------------------------------
            # EXECUTE AST
            # -------------------------------------------------

            for cmd in ast:

                # ---------------------------------------------
                # ROBOT
                # ---------------------------------------------

                if cmd["type"] == "robot":

                    robots[cmd["name"]] = cmd["model"]

                # ---------------------------------------------
                # POINT
                # ---------------------------------------------

                elif cmd["type"] == "point":

                    points[cmd["name"]] = {

                        "x": cmd["x"],
                        "y": cmd["y"],
                        "z": cmd["z"]

                    }

                # ---------------------------------------------
                # PARALLEL START
                # ---------------------------------------------

                elif cmd["type"] == "parallel_start":

                    parallel_mode = True

                # ---------------------------------------------
                # TASK END
                # ---------------------------------------------

                elif cmd["type"] == "task_end":

                    parallel_mode = False

                # ---------------------------------------------
                # EXECUTION COMMANDS
                # ---------------------------------------------

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

            # -------------------------------------------------
            # SAVE FILES
            # -------------------------------------------------

            dispatcher.save_all()

            # -------------------------------------------------
            # READ GENERATED CODE
            # -------------------------------------------------

            with open("output/kuka.src") as f:

                kuka_code = f.read()

            with open("output/ur.script") as f:

                ur_code = f.read()

        except Exception as e:

            kuka_code = str(e)

    # =====================================================
    # RENDER PAGE
    # =====================================================

    return render_template(

        "index.html",

        kuka_code=kuka_code,

        ur_code=ur_code
    )


# =========================================================
# START FLASK
# =========================================================

if __name__ == "__main__":

    app.run(debug=True)
    