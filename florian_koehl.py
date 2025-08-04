import datetime
import inspect
import os

def TOFLORIAN(message: str):
    # Get the caller’s frame info
    caller_frame = inspect.stack()[1]
    filename = os.path.relpath(caller_frame.filename)
    line_number = caller_frame.lineno
    function_name = caller_frame.function

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {filename}:{line_number} ({function_name}) ➜ TODO: {message}\n"

    with open("my_todo_wall.txt", "a", encoding="utf-8") as f:
        f.write(log_line)

















