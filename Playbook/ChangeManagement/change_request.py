import logging
from typing import List, Optional
from enum import Enum
from datetime import datetime

logging.basicConfig(level=logging.INFO)

class ChangeRequestNumber:
    def __init__(self, number: int) -> None:
        self.number = number
        logging.info(f"Initialized ChangeRequestNumber with number: {self.number}")

    def increment(self) -> int:
        self.number += 1
        logging.info(f"Incremented ChangeRequestNumber to: {self.number}")
        return self.number

class ChangeRequestDate:
    def __init__(self, date: str) -> None:
        self.date = date
        logging.info(f"Initialized ChangeRequestDate with date: {self.date}")

class RequestedBy:
    def __init__(self, name: str, position: str) -> None:
        self.name = name
        self.position = position
        logging.info(f"Initialized RequestedBy with name: {self.name}, position: {self.position}")

class DescriptionOfChange:
    def __init__(self, description: str) -> None:
        self.description = description
        logging.info(f"Initialized DescriptionOfChange with description: {self.description}")

class JustificationForChange:
    def __init__(self, justification: str) -> None:
        self.justification = justification
        logging.info(f"Initialized JustificationForChange with justification: {self.justification}")

class ImpactAssessment:
    def __init__(self, risks: str, mitigation_measures: str) -> None:
        self.risks = risks
        self.mitigation_measures = mitigation_measures
        logging.info(f"Initialized ImpactAssessment with risks: {self.risks}, mitigation_measures: {self.mitigation_measures}")

class ChangePriority:
    def __init__(self, priority: str) -> None:
        self.priority = priority
        logging.info(f"Initialized ChangePriority with priority: {self.priority}")

class ChangeCategory:
    def __init__(self, category: str) -> None:
        self.category = category
        logging.info(f"Initialized ChangeCategory with category: {self.category}")

class ChangeImplementationDate:
    def __init__(self, date_time: str) -> None:
        self.date_time = date_time
        logging.info(f"Initialized ChangeImplementationDate with date_time: {self.date_time}")

class ChangeApprover:
    def __init__(self, approver: str, approval_date: str) -> None:
        self.approver = approver
        self.approval_date = approval_date
        logging.info(f"Initialized ChangeApprover with approver: {self.approver}, approval_date: {self.approval_date}")
