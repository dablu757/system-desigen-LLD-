'''
1. What is Abstraction?
    Abstraction hides implementation details and exposes only essential functionality 
    using abstract classes and interfaces.
'''
# *****************************************************
'''
2. What is Encapsulation?
    Encapsulation = binding data + methods together and restricting direct access to data.
-----------------------------
Goal:
   1.Protect object state
   2.Allow controlled access
   3.Prevent invalid usage

-----------------------------
In your C++ example:
    Data members are private
    Access happens only through methods

-----------------------------

How Encapsulation Works in Python (Important)
    Python does NOT have strict private variables like C++, but it provides:
    Naming conventions
    ->Name mangling (__var)
    ->Properties (@property) ← best practice 
'''
# *****************************************************
'''
3. What is Inheritance?
    Inheritance allows a child class to reuse properties and methods of a parent class.
'''

# *****************************************************
'''
Abstraction defines what a class should do.
Encapsulation controls how data is accessed.
Inheritance allows reusing and extending behavior.
'''

from abc import ABC, abstractmethod


# -------- Abstraction --------
class Car(ABC):

    @abstractmethod
    def startEngien(self):
        pass

    @abstractmethod
    def accelerare(self):
        pass

    @abstractmethod
    def applyBreak(self):
        pass


# -------- Base Class (Parent) --------
class MyCar(Car):

    def __init__(self, model, brand):
        self.__model = model
        self.__brand = brand
        self.__isEngienOn = False
        self.__currentSpeed = 0

    def startEngien(self):
        self.__isEngienOn = True
        print(f"{self.__brand} {self.__model} engine started 🔥")

    def accelerare(self):
        if not self.__isEngienOn:
            print("Engine is OFF. Cannot accelerate.")
            return
        self.__currentSpeed += 20
        print(f"Speed: {self.__currentSpeed} km/h")

    def applyBreak(self):
        self.__currentSpeed = max(0, self.__currentSpeed - 10)
        print(f"Speed reduced to {self.__currentSpeed} km/h")

    # -------- Properties --------
    @property
    def speed(self):
        return self.__currentSpeed

    @speed.setter
    def speed(self, value):
        if value < 0:
            raise ValueError("Speed cannot be negative")
        if value > 300:
            raise ValueError("Speed limit exceeded")
        self.__currentSpeed = value

    @property
    def engine_status(self):
        return "ON" if self.__isEngienOn else "OFF"


# -------- Inheritance: Manual Car --------
class ManualCar(MyCar):

    def __init__(self, model, brand):
        super().__init__(model, brand)
        self.__currentGear = 0

    def shiftGear(self, gear):
        if gear < 0 or gear > 6:
            print("Invalid gear")
            return
        self.__currentGear = gear
        print(f"Shifted to gear {self.__currentGear}")

    @property
    def gear(self):
        return self.__currentGear


# -------- Inheritance: Electric Car --------
class ElectricCar(MyCar):

    def __init__(self, model, brand):
        super().__init__(model, brand)
        self.__battery = 100  # %

    def accelerare(self):
        if self.__battery <= 0:
            print("Battery empty 🔋")
            return
        super().accelerare()
        self.__battery -= 5
        print(f"Battery: {self.__battery}%")

    def applyBreak(self):
        super().applyBreak()
        self.__battery = min(100, self.__battery + 2)
        print(f"Battery recharged to {self.__battery}% 🔌")

    @property
    def battery(self):
        return self.__battery


# -------- Usage --------
if __name__ == "__main__":

    print("\n--- Manual Car ---")
    manual = ManualCar("Swift", "Maruti")
    manual.startEngien()
    manual.shiftGear(1)
    manual.accelerare()
    manual.applyBreak()
    print("Gear:", manual.gear)

    print("\n--- Electric Car ---")
    ev = ElectricCar("Model 3", "Tesla")
    ev.startEngien()
    ev.accelerare()
    ev.applyBreak()
    print("Battery:", ev.battery)


    
    

        
     