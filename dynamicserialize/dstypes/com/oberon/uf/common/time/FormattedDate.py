## Script


from .CommutativeTimestamp import CommutativeTimestamp

# TODO: Remove after 16.4.1 no longer in field
class FormattedDate(CommutativeTimestamp):

    def __init__(self, timeInMillis=None):
        super(FormattedDate, self).__init__(timeInMillis)
