class warded:

    def __init__(self, name, number, ward, nric):
        self.__pubid = ''
        self.__name = name
        self.__number = number
        self.__ward = ward
        self.__nric = nric

    def get_pubid(self):
        return self.__pubid

    def set_pubid(self, pubid):
        self.__pubid = pubid
#getters

    def get_name(self):
        return self.__name

    def get_number(self):
        return self.__number

    def get_ward(self):
        return self.__ward

    def get_nric(self):
        return self.__nric

#setters

    def set_name(self, name):
        self.__name = name

    def set_number(self, number):
        self.__number = number

    def set_ward(self, ward):
        self.__ward = ward

    def set_nric(self, nric):
        self.__nric = nric


class A(warded):

    def __init__(self, name, number, ward, aroom, nric):
        warded.__init__(self, name, number, ward, nric)
        self.__aroom = aroom

    def get_aroom(self):
        return self.__aroom

    def set_aroom(self, aroom):
        self.__aroom = aroom


class B(warded):
    def __init__(self, name, number, ward, broom, nric):
        warded.__init__(self, name, number, ward, nric)
        self.__broom = broom

    def get_broom(self):
        return self.__broom

    def set_broom(self, broom):
        self.__broom = broom


class C(warded):
    def __init__(self, name, number, ward, croom, nric):
        warded.__init__(self, name, number, ward, nric)
        self.__croom = croom

    def get_croom(self):
        return self.__croom

    def set_croom(self, croom):
        self.__croom = croom



