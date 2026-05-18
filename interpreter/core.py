from interpreter.parser import parse_line
from interpreter.krl import to_krl
from interpreter.fsm import RobotFSM
from interpreter.simulator import robot
import time


def run_rcml(code: str):
    lines = code.split("\n")
    output = []

    fsm = RobotFSM()

    for i, line in enumerate(lines, start=1):
        line = line.strip()

        if not line:
            continue

        try:
            cmd = parse_line(line)

            state = fsm.transition(cmd)
            krl = to_krl(cmd)

            sim_logs = robot.send(krl)

            log = {
                "line": i,
                "command": cmd["cmd"],
                "state": state,
                "krl": krl,
                "simulator": sim_logs,
                "status": "OK",
                "time": time.strftime("%H:%M:%S")
            }

            output.append(log)

        except Exception as e:
            output.append({
                "line": i,
                "status": "ERROR",
                "error": str(e),
                "time": time.strftime("%H:%M:%S")
            })

    return output

def save_krl_program(commands):
    with open("program.src", "w") as f:
        for cmd in commands:
            f.write(cmd + "\n")