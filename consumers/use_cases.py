

class ConsumerUseCase:
    def __init__(self, repo):
        self.__repo = repo
    
    def get_failed(self, application_id):
        """ Gets failed requests from DB """ 
        return self.__repo.get_failed(application_id)

    def trigger_notifications_reprocessing(self, application_id):
        """ Triggers notifications reprocessing """