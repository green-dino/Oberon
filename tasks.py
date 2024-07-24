class Task:
    def __init__(self, name, action):
        self.name = name
        self.action = action  # This could be a string representing a method to call or a callable object itself

    def execute(self):
        # Execute the task's action
        print(f"Executing {self.name}")
        self.action()