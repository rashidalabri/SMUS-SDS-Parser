class NotLoggedInException(Exception):

    def __init__(self):
        Exception.__init__(self, "The session you are using is not logged in.")
