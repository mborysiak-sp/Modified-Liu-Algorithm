class Task:

    def __init__(self, name, p, r, dj):
        self.name = name
        self.p = p
        self.currentP = self.p
        self.r = r
        self.dj = dj
        self.after = []
        self.before = []
        self.di = 0

    def find_modified_deadline(self):
        if not self.after:
            self.di = self.dj
            return self.di

        deadline_list = [self.dj]

        for task in self.after:
            deadline_list.append(task.find_modified_deadline())

        self.di = min(deadline_list)

        return self.di

    # def copy(self):
    #     copy = Task("", 0, 0, 0)
    #
    #     copy.name = self.name
    #     copy.dj = self.dj
    #     copy.di = self.di
    #     copy.p = self.p
    #     copy.after = self.after
    #     copy.before = self.before
    #
    #     return copy

    def link(self, task):
        task.before.append(self)
        self.after.append(task)
