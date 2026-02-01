class Parent(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def getX(self):
        print(f"the value of x is: {self.x}")
        return
    
    def getY(self):
        print(f"the value of y is: {self.y}")
        return
    
    def addition(self):
        return self.x+self.y
    

class Child(Parent):
    def __init__(self,x,y,z):
        super().__init__(x,y)
        self.z = z

    def getZ(self):
        print(f"the value of z is: {self.z}")
        return
    
    def addition(self):
        return super().addition() + self.z
    

if __name__ == "__main__":
    parent = Parent(x=10,y=20)
    print(f"parent summition: {parent.addition()}")
    child = Child(10,20,30)
    print(f"child summition: {child.addition()}")

