from lark import Transformer


class RCMLTransformer(Transformer):

    # =====================================================
    # ROBOT
    # =====================================================

    def robot_decl(self, items):

        return {
            "type": "robot",
            "name": str(items[0]),
            "model": str(items[1])
        }

    # =====================================================
    # POINT
    # =====================================================

    def point_decl(self, items):

        return {
            "type": "point",
            "name": str(items[0]),
            "x": float(items[1]),
            "y": float(items[2]),
            "z": float(items[3])
        }

    # =====================================================
    # TASK
    # =====================================================

    def task_decl(self, items):

        return {
            "type": "task",
            "name": str(items[0])
        }

    # =====================================================
    # PARALLEL
    # =====================================================

    def parallel_decl(self, items):

        return {
            "type": "parallel_start"
        }

    # =====================================================
    # MOVE
    # =====================================================

    def move_cmd(self, items):

        return {
            "type": "move",
            "robot": str(items[0]),
            "target": str(items[1])
        }

    # =====================================================
    # GRAB
    # =====================================================

    def grab_cmd(self, items):

        return {
            "type": "grab",
            "robot": str(items[0])
        }

    # =====================================================
    # RELEASE
    # =====================================================

    def release_cmd(self, items):

        return {
            "type": "release",
            "robot": str(items[0])
        }

    # =====================================================
    # HOME
    # =====================================================

    def home_cmd(self, items):

        return {
            "type": "home",
            "robot": str(items[0])
        }

    # =====================================================
    # SYNC
    # =====================================================

    def sync_cmd(self, items):

        return {
            "type": "sync"
        }

    # =====================================================
    # WAIT
    # =====================================================

    def wait_cmd(self, items):

        return {
            "type": "wait",
            "time": int(items[0])
        }

    # =====================================================
    # STATEMENT
    # =====================================================

    def statement(self, items):

        if not items:

            return {
                "type": "task_end"
            }

        return items[0]

    # =====================================================
    # START
    # =====================================================

    def start(self, items):

        return items