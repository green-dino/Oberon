from change_request import ( 
    ChangeRequestNumber, ChangeRequestDate, RequestedBy, DescriptionOfChange, JustificationForChange,
    ImpactAssessment, ChangePriority, ChangeCategory, ChangeImplementationDate, ChangeApprover
)

from document_control import (
    DocumentTitle, DocumentNumber, RevisionHistory, DateOfLastRevision,
    DocumentOwner, DistributionList, DocumentControlInformation
)

from impact_assessment import (
    ScopeOfChange, StepsInvolved, ResourcesRequired, TimelineForSteps,
    TestingAndValidation, RollbackPlan, ChangeImplementationPlan
)

from communication import (
    StakeholdersAffected, CommunicationPlan, NotificationProcess, TrainingRequirements, 
    CommunicationAndNotification
)

from utils import create_instance


storage = {
    'change_requests': [],
    'documents': [],
    'impact_assessments': [],
    'communications': [],
}

