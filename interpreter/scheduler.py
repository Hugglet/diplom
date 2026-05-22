import json
import math


class Scheduler:

    def __init__(self):

        # =================================================
        # LOAD ENVIRONMENT CONFIG
        # =================================================

        with open(

            "config/environment.json",

            "r",

            encoding="utf-8"

        ) as f:

            self.config = json.load(f)

        # =================================================
        # ROBOTS
        # =================================================

        self.robots = self.config["robots"]

        # =================================================
        # WEIGHTS
        # =================================================

        self.weights = {

            "dimensions": 0.10,
            "mass": 0.15,
            "distance": 0.10,
            "time": 0.10,
            "workspace": 0.10,
            "singularity": 0.10,
            "precision": 0.10,
            "speed": 0.10,
            "load": 0.05,
            "energy": 0.10
        }

    # =====================================================
    # DISTANCE
    # =====================================================

    def calculate_distance(

        self,

        robot_pos,

        target_pos

    ):

        return math.sqrt(

            (robot_pos["x"] - target_pos["x"]) ** 2 +

            (robot_pos["y"] - target_pos["y"]) ** 2 +

            (robot_pos["z"] - target_pos["z"]) ** 2
        )

    # =====================================================
    # CALCULATE SCORE
    # =====================================================

    def calculate_score(

        self,

        robot,

        task,

        target_point

    ):

        score = 0

        # -------------------------------------------------
        # 1. DIMENSIONS
        # -------------------------------------------------

        score += (

            task["dimensions"] *

            self.weights["dimensions"]
        )

        # -------------------------------------------------
        # 2. MASS
        # -------------------------------------------------

        payload_ratio = (

            robot["payload"] /

            task["mass"]
        )

        score += (

            payload_ratio *

            self.weights["mass"]
        )

        # -------------------------------------------------
        # 3. DISTANCE
        # -------------------------------------------------

        distance = self.calculate_distance(

            robot["position"],

            target_point
        )

        distance_score = 1 / (

            distance + 1
        )

        score += (

            distance_score *

            self.weights["distance"] * 100
        )

        # -------------------------------------------------
        # 4. TIME
        # -------------------------------------------------

        time_score = (

            robot["speed"] /

            task["time"]
        )

        score += (

            time_score *

            self.weights["time"]
        )

        # -------------------------------------------------
        # 5. WORKSPACE
        # -------------------------------------------------

        workspace_score = (

            robot["reach"] / 20
        )

        score += (

            workspace_score *

            self.weights["workspace"]
        )

        # -------------------------------------------------
        # 6. SINGULARITY
        # -------------------------------------------------

        singularity_penalty = (

            task["singularity"]
        )

        score -= (

            singularity_penalty *

            self.weights["singularity"]
        )

        # -------------------------------------------------
        # 7. PRECISION
        # -------------------------------------------------

        precision_score = (

            1 / robot["accuracy"]
        )

        score += (

            precision_score *

            self.weights["precision"]
        )

        # -------------------------------------------------
        # 8. SPEED
        # -------------------------------------------------

        score += (

            robot["speed"] *

            self.weights["speed"]
        )

        # -------------------------------------------------
        # 9. LOAD
        # -------------------------------------------------

        load_penalty = (

            robot["current_load"]
        )

        score -= (

            load_penalty *

            self.weights["load"]
        )

        # -------------------------------------------------
        # 10. ENERGY
        # -------------------------------------------------

        energy_penalty = (

            robot["energy_factor"]
        )

        score -= (

            energy_penalty *

            self.weights["energy"]
        )

        return score

    # =====================================================
    # CHOOSE ROBOT
    # =====================================================

    def choose_robot(

        self,

        task,

        target_point

    ):

        best_robot = None

        best_score = -999999

        # =================================================
        # ANALYZE ROBOTS
        # =================================================

        for robot_name, robot in self.robots.items():

            # ---------------------------------------------
            # HARD LIMITS
            # ---------------------------------------------

            if robot["payload"] < task["mass"]:

                continue

            # ---------------------------------------------
            # SCORE
            # ---------------------------------------------

            score = self.calculate_score(

                robot,
                task,
                target_point
            )

            print(

                robot_name,
                score
            )

            # ---------------------------------------------
            # BEST ROBOT
            # ---------------------------------------------

            if score > best_score:

                best_score = score

                best_robot = robot_name

        return best_robot