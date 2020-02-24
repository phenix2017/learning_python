class A(object):
 """_Private member should not be used outside of the internal. 
 Could be changed and modified without any notification. 
 """
 def _internal_use(self): 
     print("internal use")
"""_PrivateMember_: The simular with  "_PrivateMember" """
 def _internal_use_(self):
     pass
 """ front double underscore "__XX" withtout trailing underscore "__"
 or with at most "_" trailing underscore
 indicates it has specific meaning to the python interpreter.
 Python interpreter will add the class "_ClassName__XX"
 """   
 def __class_method(self):
     print("This is a class method")
 def __class_method__(self):
     print("class method ends up with __")