import logging as log
class Logger():
    def __init__(self, path, processId):
        self.path = path
        self.processId = processId
    def loggerCall(self, message=None, intention=None):
        log.basicConfig(filename=self.path, level=log.DEBUG,format='Date --> %(asctime)s , ProcessId --> %(process)s , Message --> %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
        log_func = log.info if intention == 'Info' else (log.warning if intention == 'Warn' else log.error)
        log_func(message)
