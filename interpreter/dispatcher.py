from interpreter.backends.kuka_adapter import KukaAdapter
from interpreter.backends.ur_adapter import URAdapter


class Dispatcher:

    def __init__(self):

        self.backends = {
            "KR150": KukaAdapter(),
            "UR3e": URAdapter()
        }

    def dispatch(self, robot_model, command, points):

        backend = self.backends.get(robot_model)

        if not backend:
            raise ValueError(f"No backend for {robot_model}")

        backend.execute(command, points)

    def save_all(self):

        self.backends["KR150"].save(
            "output/kuka.src"
        )

        self.backends["UR3e"].save(
            "output/ur.script"
        )