from ..Roles.roles import (
    SecureSoftwareAssessor , SecurityControlAssessor , SecurityArchitect , 
    SoftwareDeveloper , SystemsAdministrator , SystemsArchitect , SystemsDeveloper , CyberDefenseAnalyst
   
)
class Block:
    def __init__(self, name):
        self.tasks = []
        self.name = name
        self.roles = []

    def add_task(self, task):
        self.tasks.append(task)

    def execute_tasks(self):
        for task in self.tasks:
            task.execute()
    
