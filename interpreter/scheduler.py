import json
import math
import os


class Scheduler:

    def __init__(self):

        # =================================================
        # PROJECT ROOT
        # =================================================

        BASE_DIR = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                ".."
            )
        )

        # =================================================
        # CONFIG FILE
        # =================================================

        config_path = os.path.join(
            BASE_DIR,
            "config",
            "environment.json"
        )

        print("\nCONFIG PATH:")
        print(config_path)

        # =================================================
        # LOAD CONFIG
        # =================================================

        if not os.path.exists(config_path):

            raise FileNotFoundError(
                f"Config file not found:\n{config_path}"
            )

        with open(
            config_path,
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

        # 1. OBJECT DIMENSIONS

        score += (
            task["dimensions"]
            * self.weights["dimensions"]
        )

        # 2. PAYLOAD

        payload_ratio = (
            robot["payload"]
            / max(task["mass"], 0.1)
        )

        score += (
            payload_ratio
            * self.weights["mass"]
        )

        # 3. DISTANCE

        distance = self.calculate_distance(
            robot["position"],
            target_point
        )

        distance_score = 1 / (distance + 1)

        score += (
            distance_score
            * self.weights["distance"]
            * 100
        )

        # 4. EXECUTION TIME

        time_score = (
            robot["speed"]
            / max(task["time"], 0.1)
        )

        score += (
            time_score
            * self.weights["time"]
        )

        # 5. WORKSPACE

        workspace_score = (
            robot.get("reach", 500) / 20
        )

        score += (
            workspace_score
            * self.weights["workspace"]
        )

        # 6. SINGULARITY

        score -= (
            task["singularity"]
            * self.weights["singularity"]
        )

        # 7. ACCURACY

        precision_score = (
            1 / max(robot["accuracy"], 0.001)
        )

        score += (
            precision_score
            * self.weights["precision"]
        )

        # 8. SPEED

        score += (
            robot["speed"]
            * self.weights["speed"]
        )

        # 9. CURRENT LOAD

        score -= (
            robot["current_load"]
            * self.weights["load"]
        )

        # 10. ENERGY

        score -= (
            robot["energy_factor"]
            * self.weights["energy"]
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

        best_score = float("-inf")

        print("\n========== ROBOT ANALYSIS ==========")

        for robot_name, robot in self.robots.items():

            # PAYLOAD CHECK

            if robot["payload"] < task["mass"]:

                print(
                    f"{robot_name}: SKIPPED (payload too low)"
                )

                continue

            score = self.calculate_score(
                robot,
                task,
                target_point
            )

            print(
                f"{robot_name}: SCORE = {round(score, 2)}"
            )

            if score > best_score:

                best_score = score

                best_robot = robot_name

        print(
            "\n========== SCHEDULER RESULT =========="
        )

        print(
            f"Selected robot: {best_robot}"
        )

        print(
            f"Best score: {round(best_score, 2)}"
        )

        return best_robot