class Address:
    """ Hold all the fields for a mailing address. """
    def __init__(self):
        """ Set up the address fields. """
        self.name = ""
        self.line1 = ""
        self.line2 = ""
        self.city = ""
        self.state = ""
        self.zip = ""
        self.age = 0
        self.jop = ""

    @staticmethod
    def hello():
        print("Hello World?")