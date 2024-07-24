import logging

logging.basicConfig(level=logging.INFO)

class DocumentTitle:
    def __init__(self, title: str) -> None:
        self.title = title
        logging.info(f"Initialized DocumentTitle with title: {self.title}")

class DocumentNumber:
    def __init__(self, number: str) -> None:
        self.number = number
        logging.info(f"Initialized DocumentNumber with number: {self.number}")

class RevisionHistory:
    def __init__(self, history: str) -> None:
        self.history = history
        logging.info(f"Initialized RevisionHistory with history: {self.history}")

class DateOfLastRevision:
    def __init__(self, date: str) -> None:
        self.date = date
        logging.info(f"Initialized DateOfLastRevision with date: {self.date}")

class DocumentOwner:
    def __init__(self, owner: str) -> None:
        self.owner = owner
        logging.info(f"Initialized DocumentOwner with owner: {self.owner}")

class DistributionList:
    def __init__(self, distribution_list: str) -> None:
        self.distribution_list = distribution_list
        logging.info(f"Initialized DistributionList with distribution_list: {self.distribution_list}")

class DocumentControlInformation:
    def __init__(self, title: str, number: str, history: str, last_revision_date: str, owner: str, distribution_list: str) -> None:
        self.title = DocumentTitle(title)
        self.number = DocumentNumber(number)
        self.history = RevisionHistory(history)
        self.last_revision_date = DateOfLastRevision(last_revision_date)
        self.owner = DocumentOwner(owner)
        self.distribution_list = DistributionList(distribution_list)
        logging.info("Initialized DocumentControlInformation")
