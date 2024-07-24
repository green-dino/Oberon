import logging

logging.basicConfig(level=logging.INFO)

class ScopeOfChange:
    def __init__(self, scope: str) -> None:
        self.scope = scope
        logging.info(f"Initialized ScopeOfChange with scope: {self.scope}")

class StepsInvolved:
    def __init__(self, steps: str) -> None:
        self.steps = steps
        logging.info(f"Initialized StepsInvolved with steps: {self.steps}")

class ResourcesRequired:
    def __init__(self, resources: str) -> None:
        self.resources = resources
        logging.info(f"Initialized ResourcesRequired with resources: {self.resources}")

class TimelineForSteps:
    def __init__(self, timeline: str) -> None:
        self.timeline = timeline
        logging.info(f"Initialized TimelineForSteps with timeline: {self.timeline}")

class TestingAndValidation:
    def __init__(self, procedures: str) -> None:
        self.procedures = procedures
        logging.info(f"Initialized TestingAndValidation with procedures: {self.procedures}")

class RollbackPlan:
    def __init__(self, rollback_plan: str) -> None:
        self.rollback_plan = rollback_plan
        logging.info(f"Initialized RollbackPlan with rollback_plan: {self.rollback_plan}")

class ChangeImplementationPlan:
    def __init__(self, scope: str, steps: str, resources: str, timeline: str, testing_procedures: str, rollback_plan: str) -> None:
        self.scope = ScopeOfChange(scope)
        self.steps = StepsInvolved(steps)
        self.resources = ResourcesRequired(resources)
        self.timeline = TimelineForSteps(timeline)
        self.testing_procedures = TestingAndValidation(testing_procedures)
        self.rollback_plan = RollbackPlan(rollback_plan)
        logging.info("Initialized ChangeImplementationPlan")
