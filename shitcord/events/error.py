class InvalidEventException(Exception):
    def __init__(self, eventname):
        super().__init__('Received Event without parser: %s' % eventname)
        self.event = eventname
