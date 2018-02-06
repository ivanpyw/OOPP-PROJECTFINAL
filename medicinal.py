# class Descbill:
#     def __init__(self, product, quantity, price):
#         self.__product = product
#         self.__quantity = quantity
#         self.__price = price
#
#         def get_product(self):
#             return self.__product
#
#         def get_quantity(self):
#             return self.__quantity
#
#         def get_price(self):
#             return self.__price
#
#         def set_product(self, product):
#             self.__product = product
#
#         def set_quantity(self, quantity):
#             self.__quantity = quantity
#
#         def set_price(self, price):
#             self.__price = price

class Medicinal:
    def __init__(self, product, price, id):
        self.product = product
        self.id = id
        self.price = price
        self.pubid = ""

    def get_product(self):
        return self.product

    def get_id(self):
        return self.id

    def get_price(self):
        return self.price

    def get_pubid(self):
        return self.pubid


    def set_product(self, product):
        self.product = product


    def set_id(self, id):
        self.id = id

    def set_price(self, price):
        self.price = price

    def set_pubid(self, pubid):
        self.pubid = pubid

