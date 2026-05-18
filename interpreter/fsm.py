class RobotFSM:
    def __init__(self):
        self.state = "IDLE"

    def transition(self, command):
        cmd = command["cmd"]

        if self.state == "IDLE":
            if cmd == "MOVE":
                self.state = "MOVING"
            elif cmd == "PICK":
                self.state = "PICKING"
            elif cmd == "PLACE":
                self.state = "PLACING"

        elif self.state == "MOVING":
            self.state = "IDLE"

        elif self.state == "PICKING":
            self.state = "IDLE"

        elif self.state == "PLACING":
            self.state = "IDLE"

        else:
            self.state = "ERROR"

        return self.state