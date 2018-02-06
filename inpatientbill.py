# class inpatientbill():
#     def __init__(self,nric,productu,quantity):
#         self.__nric = nric
#         self.__productu = productu
#         self.__quantity = quantity
#         # self.__subtotal = subtotal
#         # self.__datecreated = datecreated
#         # self.__staffid = staffid
#
#     def get_nric(self):
#         return self.__nric
#     def set_nric(self,nric):
#         self.__nric = nric
#
#     def get_productu(self):
#         return self.__productu
#     def set_product(self, productu):
#         self.__productu = productu
#
#     def get_quantity(self):
#         return self.__quantity
#
#     def set_quantity(self, quantity):
#         self.__quantity = quantity
#
#     # def get_subtotal(self):
#     #     return self.__subtotal
#     #
#     # def set_subtotal(self, subtotal):
#     #     self.__subtotal = subtotal
#     #
#     # def get_datecreated(self):
#     #     return self.__datecreated
#     #
#     # def set_datecreated(self, datecreated):
#     #     self.__datecreated = datecreated
#
# # class inpatientbill():
# #     def __init__(self,nric,productu,quantity,subtotal,datecreated,staffid):
# #         self.__nric = nric
# #         self.__productu = productu
# #         self.__quantity = quantity
# #         self.__subtotal = subtotal
# #         self.__datecreated = datecreated
# #         self.__staffid = staffid
# #
# #     def get_nric(self):
# #         return self.__nric
# #
# #     def set_product(self, productu):
# #         self.__productu = productu
# #
# #     def get_quantity(self):
# #         return self.__quantity
# #
# #     def set_quantity(self, quantity):
# #         self.__quantity = quantity
# #
# #     def get_subtotal(self):
# #         return self.__subtotal
# #
# #     def set_subtotal(self, subtotal):
# #         self.__subtotal = subtotal
# #
# #     def get_datecreated(self):
# #         return self.__datecreated
# #
# #     def set_datecreated(self, datecreated):
# #         self.__datecreated = datecreated
class products():
    def __init__(self,id,productName,unitPrice):
        self.__id = id
        self.__productName = productName
        self.__unitPrice = unitPrice

    def get_id(self):
        return self.__id
    def set_id(self,id):
        self.__id = id

    def get_productName(self):
        return self.__productName
    def set_productName(self,productName):
        self.__productName = productName

    def get_unitPrice(self):
        return self.__unitPrice
    def set_unitPrice(self,unitPrice):
        self.__unitPrice = unitPrice


class inpatientbill(products):
    def __init__(self, nric, quantity, subtotal, id, productName, unitPrice):
        super().__init__(id,productName,unitPrice)
        self.__nric = nric
        self.__quantity = quantity
        self.__subtotal = subtotal
        # self.__datecreated = datecreated


    def get_nric(self):
        return self.__nric

    def set_nric(self,nric):
        self.__nric = nric

    def get_productu(self):
        return self.__productu

    def set_product(self, productu):
        self.__productu = productu

    def get_quantity(self):
        return self.__quantity

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def get_subtotal(self):
        return self.__subtotal

    def set_subtotal(self, subtotal):
        self.__subtotal = subtotal
class p():
    def __init__(self,productid, nric, product,quantity):
        self.__productid = productid
        self.__nric = nric
        self.__product = product
        self.__quantity = quantity

    def get_productid(self):
        return self.__productid
    def set_productid(self,productid):
        self.__productid = productid


    def get_nric(self):
        return self.__nric

    def set_nric(self, nric):
        self.__nric = nric
    def get_product(self):
        return self.__product
    def set_product(self,product):
        self.__product = product

    def get_quantity(self):
        return self.__quantity
    def set_quantity(self,quantity):
        self.__quantity = quantity




            #
    # def get_datecreated(self):
    #     return self.__datecreated
    #
    # def set_datecreated(self, datecreated):
    #     self.__datecreated = datecreated
