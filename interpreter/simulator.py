import time


class KukaSimulator:
    def __init__(self):
        self.connected = True

    def send(self, krl_command: str):
        logs = []

        # разбиваем многострочные команды
        commands = krl_command.split("\n")

        for cmd in commands:
            cmd = cmd.strip()

            if not cmd:
                continue

            # имитация выполнения
            time.sleep(0.3)

            logs.append(f"[SIM] Executed: {cmd}")

        return logs


# глобальный экземпляр
robot = KukaSimulator()