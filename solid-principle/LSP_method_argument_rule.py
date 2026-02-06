class Parent:    
    def display(self,msg:str):
        print(f"parent message : {msg}")


class Child(Parent):
    def display(self,msg:str):
        print(f"child message : {msg}")


class Client:
   def __init__(self, parent :Parent) -> None:
       self.p = parent

   def print_msg(self):
       self.p.display('Hello from client')

       

if __name__ == "__main__":
    parent = Parent()
    child = Child()

    client1 = Client(parent)
    client1.print_msg()

    client2 = Client(child)
    client2.print_msg()

    # obj.add(5)

    