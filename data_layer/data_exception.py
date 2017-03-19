class DataLayerException(Exception):
    """Raise for data layer exception exception"""
    def __init__(self, dErrorArguments):
        Exception.__init__(self, "Data Layer Exception {0}".format(dErrorArguments))

        if dErrorArguments is None:
            self.errorArgs = {
                        'code': 500,
                        'message': 'Internal Error'
                    }
        else:
            self.errorArgs = dErrorArguments
