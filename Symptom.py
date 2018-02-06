# class Symptoms:
#
#     def __init__(self, travel, allergies, specify, type, nric):
#         self.__pubid = ''
#         self.__travel = travel
#         self.__allergies = allergies
#         self.__specify = specify
#         self.__nric = nric
#         self.__type = type
#
# #pubid
#
#     def get_pubid(self):
#         return self.__pubid
#
#     def set_pubid(self, pubid):
#         self.__pubid = pubid
#
# #getters
#
#     def get_travel(self):
#         return self.__travel
#
#     def get_allergies(self):
#         return self.__allergies
#
#     def get_type(self):
#         return self.__type
#
#     def get_specify(self):
#         return self.__specify
#
#     def get_nric(self):
#         return self.__nric
#
# #setters
#
#     def set_travel(self, travel):
#         self.__travel = travel
#
#     def set_allergies(self, allergies):
#         self.__allergies = allergies
#
#     def set_type(self, type):
#         self.__type = type
#
#     def set_specify(self, specify):
#         self.__specify = specify
#
#     def set_nric(self, nric):
#         self.__nric = nric
#
#
# class ChestPain(Symptoms):
#
#     def __init__(self, allergies, travel, type, specify, painrate, nric):
#         Symptoms.__init__(self, allergies, travel, type, specify, nric)
#         self.__painrate = painrate
#
#     def get_painrate(self):
#         return self.__painrate
#
#     def set_painrate(self, painrate):
#         self.__painrate = painrate
#
# class AbdominalPain(Symptoms):
#
#     def __init__(self, allergies, travel, type, specify, painrate, nric):
#         Symptoms.__init__(self, allergies, travel, type, specify, nric)
#         self.__painrate = painrate
#
#     def get_painrate(self):
#         return self.__painrate
#
#     def set_painrate(self, painrate):
#         self.__painrate = painrate
#
# class Fever(Symptoms):
#
#     def __init__(self, allergies, travel, type, specify, osymps, nric):
#         Symptoms.__init__(self, allergies, travel, type, specify, nric)
#         self.__osymps = osymps
#
#     def get_osymps(self):
#         return self.__osymps
#
#     def set_osymps(self, osymps):
#         self.__osymps = osymps
#
# class Breathless(Symptoms):
#
#     def __init__(self, allergies, travel, type, specify, history, nric):
#         Symptoms.__init__(self, allergies, travel, type, specify, nric)
#         self.__history = history
#
#     def get_history(self):
#         return self.__history
#
#     def set_history(self, history):
#         self.__history = history

class Symptoms:

    def __init__(self, travel, allergies, specify, type, nric):
        self.__pubid = ''
        self.__travel = travel
        self.__allergies = allergies
        self.__specify = specify
        self.__nric = nric
        self.__type = type

#pubid

    def get_pubid(self):
        return self.__pubid

    def set_pubid(self, pubid):
        self.__pubid = pubid

#getters

    def get_travel(self):
        return self.__travel

    def get_allergies(self):
        return self.__allergies

    def get_type(self):
        return self.__type

    def get_specify(self):
        return self.__specify

    def get_nric(self):
        return self.__nric

#setters

    def set_travel(self, travel):
        self.__travel = travel

    def set_allergies(self, allergies):
        self.__allergies = allergies

    def set_type(self, type):
        self.__type = type

    def set_specify(self, specify):
        self.__specify = specify

    def set_nric(self, nric):
        self.__nric = nric


class ChestPain(Symptoms):

    def __init__(self, allergies, travel, type, specify, painrate, nric):
        Symptoms.__init__(self, allergies, travel, type, specify, nric)
        self.__painrate = painrate

    def get_painrate(self):
        return self.__painrate

    def set_painrate(self, painrate):
        self.__painrate = painrate

class AbdominalPain(Symptoms):

    def __init__(self, allergies, travel, type, specify, painrate, nric):
        Symptoms.__init__(self, allergies, travel, type, specify, nric)
        self.__painrate = painrate

    def get_painrate(self):
        return self.__painrate

    def set_painrate(self, painrate):
        self.__painrate = painrate

class Fever(Symptoms):

    def __init__(self, allergies, travel, type, specify, osymps, nric):
        Symptoms.__init__(self, allergies, travel, type, specify, nric)
        self.__osymps = osymps

    def get_osymps(self):
        return self.__osymps

    def set_osymps(self, osymps):
        self.__osymps = osymps

class Breathless(Symptoms):

    def __init__(self, allergies, travel, type, specify, history, nric):
        Symptoms.__init__(self, allergies, travel, type, specify, nric)
        self.__history = history

    def get_history(self):
        return self.__history

    def set_history(self, history):
        self.__history = history




