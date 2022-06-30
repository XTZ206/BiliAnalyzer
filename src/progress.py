import os.path
from typing import Optional, Dict, List


class ProgressCounter:
    prompt = {"running": "Running", "finished": "Finished"}

    def __init__(self, prompt: Optional[Dict[str, str]] = None):
        self.total = -1
        self.current = 0
        if prompt is not None:
            self.prompt = prompt

    def reset_progress(self):
        self.current = 0
        self.total = -1

    def set_progress_total(self, total: int):
        self.reset_progress()
        self.total = total

    def inc_progress(self):
        self.current += 1

    @property
    def have_started(self):
        return self.total != -1

    @property
    def have_finished(self):
        return (self.current >= self.total) and self.have_started

    @property
    def progress_str(self):
        if self.have_finished:
            return f"{self.prompt['finished']} {self.current}/{self.total}"
        else:
            return f"{self.prompt['running']} {self.current}/{self.total}"


class Progress:
    prompt = {"running": "Running", "finished": "Finished"}

    def __init__(self, prompt: Dict[str, str]):
        self.progress_counter = ProgressCounter(prompt)


# TODO: Change Log to Logging Module
class Logger:
    def __init__(self, fp, newline=True):
        self.fp = fp
        self.log: List[str] = []
        self.newline = newline
        if os.path.exists(self.fp):
            with open(self.fp, "r") as f:
                self.log.extend(f.readlines())

    def add_to_log(self, log: str, newline: Optional[bool] = None, save: bool = True):
        if newline is None:
            newline = self.newline
        if newline and log[-1] != '\n':
            log = log + '\n'
        self.log.append(log)

        if save:
            self.save_log()

    def save_log(self):
        with open(self.fp, "w", encoding="utf-8") as f:
            f.writelines(self.log)
