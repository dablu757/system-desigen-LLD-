'''
Abstraction hides implementation details and exposes only essential functionality 
using abstract classes and interfaces.
'''
from abc import ABC, abstractmethod
class Car(ABC):

    @abstractmethod
    def startCar():
        pass

    @abstractmethod
    def shiftGare():
        pass


class MyCar(Car):
   
    def startCar(self):
       print("this is start car mehtod")

    def shiftGare(self):
        print('this is shift gare method')



if __name__ == "__main__":
    my_car = MyCar()
    my_car.startCar()
    my_car.shiftGare()

