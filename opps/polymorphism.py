'''
What is Polymorphism?
    One interface, many forms
------------------------------
In Python:
    Same method name
    Different behavior
    Behavior depends on object or arguments
------------------------------
Dynamic Polymorphism (Method Overriding)
    Runtime polymorphism
    Achieved using inheritance
..........................................
Concept
    Parent class defines a method
    Child class overrides it
    Method call decided at runtime
'''


#Dynamic Polymorphism → Method Overriding
class Car:
    '''
        Why this is Dynamic Polymorphism
            Same method: start()
            Different behavior
            Python decides at runtime which start() to call
        .........................
        This matches:
            Dynamic Polymorphism → Method Overriding
    '''
    def start(self):
        print('Car is starting')

class ManualCar(Car):
    def start(self):
        print('Manual car started with key')

class ElectricCar(Car):
    def start(self):
        print('Electric car started sliently')


# static Polymorphism → Method Overloading
'''
“Python mainly supports dynamic polymorphism via method overriding, 
and achieves *static-like polymorphism using default arguments or args, 
since it doesn’t support traditional method overloading.”
'''

class Calculator:
    def add(self,*args):
        return sum(args)
    



if __name__ == "__main__":
    car = [Car(),ManualCar(),ElectricCar()]
    calc = Calculator()
    print(calc.add(1,2,3))
    print(calc.add(1,2,3,4))


    # for car in car:
    #     car.start()