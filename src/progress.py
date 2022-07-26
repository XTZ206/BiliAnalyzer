class ProgressCounter:
    def __init__(self):
        self.current = 0
        self.capacity = -1  # -1 指代未知工作量

    def reset_progress(self):
        self.current = 0
        self.capacity = -1

    def set_progress_capacity(self, capacity: int):
        self.reset_progress()
        self.capacity = capacity

    def inc_progress(self):
        if self.current < self.capacity:
            self.current += 1

    @property
    def have_started(self):
        return self.capacity != -1

    @property
    def have_finished(self):
        return (self.current >= self.capacity) and self.have_started

    @property
    def percentage(self):
        if not self.have_started:
            return 0
        elif self.have_finished:
            return 100
        else:
            return self.current * 100 // self.capacity


class Progress:
    def __init__(self, name: str):
        self.name: str = name
        self.counter: ProgressCounter = ProgressCounter()
