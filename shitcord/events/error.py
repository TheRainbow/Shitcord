class InvalidEventException(Exception):
    def __init__(self, event_name):
        super().__init__('Received Event without parser: %s' % event_name)

        self.event = event_name
