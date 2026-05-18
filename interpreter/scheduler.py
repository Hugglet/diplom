class Scheduler:

    def __init__(self):

        # =================================================
        # ROBOT DATABASE
        # =================================================

        self.robots = {

            "kuka": {

                "payload": 150,
                "precision": 0.5,
                "speed": 6,
                "energy": 8,
                "reach": 20,
                "busy": 4
            },

            "ur": {

                "payload": 3,
                "precision": 0.1,
                "speed": 9,
                "energy": 3,
                "reach": 8,
                "busy": 2
            }
        }

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
    # CALCULATE SCORE
    # =====================================================

    def calculate_score(self, robot, task):

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
            robot["payload"] / task["mass"]
        )

        score += (
            payload_ratio *
            self.weights["mass"]
        )

        # -------------------------------------------------
        # 3. DISTANCE
        # -------------------------------------------------

        distance_score = 1 / (
            task["distance"] + 1
        )

        score += (
            distance_score *
            self.weights["distance"]
        )

        # -------------------------------------------------
        # 4. TIME
        # -------------------------------------------------

        time_score = (
            robot["speed"] / task["time"]
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
            1 / robot["precision"]
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

        load_penalty = robot["busy"]

        score -= (
            load_penalty *
            self.weights["load"]
        )

        # -------------------------------------------------
        # 10. ENERGY
        # -------------------------------------------------

        energy_penalty = robot["energy"]

        score -= (
            energy_penalty *
            self.weights["energy"]
        )

        return score

    # =====================================================
    # CHOOSE ROBOT
    # =====================================================

    def choose_robot(self, task):

        best_robot = None

        best_score = -999999

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
                task
            )

            print(robot_name, score)

            if score > best_score:

                best_score = score

                best_robot = robot_name

        return best_robot