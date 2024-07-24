import logging

logging.basicConfig(level=logging.INFO)

class StakeholdersAffected:
    def __init__(self, stakeholders: str) -> None:
        self.stakeholders = stakeholders
        logging.info(f"Initialized StakeholdersAffected with stakeholders: {self.stakeholders}")

class CommunicationPlan:
    def __init__(self, plan: str) -> None:
        self.plan = plan
        logging.info(f"Initialized CommunicationPlan with plan: {self.plan}")

class NotificationProcess:
    def __init__(self, process: str) -> None:
        self.process = process
        logging.info(f"Initialized NotificationProcess with process: {self.process}")

class TrainingRequirements:
    def __init__(self, requirements: str) -> None:
        self.requirements = requirements
        logging.info(f"Initialized TrainingRequirements with requirements: {self.requirements}")

class CommunicationAndNotification:
    def __init__(self, stakeholders: str, plan: str, process: str, training: str) -> None:
        self.stakeholders = StakeholdersAffected(stakeholders)
        self.plan = CommunicationPlan(plan)
        self.process = NotificationProcess(process)
        self.training = TrainingRequirements(training)
        logging.info("Initialized CommunicationAndNotification")
