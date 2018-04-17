import unittest
from unittest.mock import patch 
import sys


sys.path.append('../src')  #need this to find switch_lights

from switch_lights.main import *

class TestCommand(unittest.TestCase):
    
    def setUp(self):
        self.MyTest1 = LightTester(5)
        self.turnon9=('turn on', '0', '0', '2', '2')
        self.turnoff4 = ('turn off', '0', '0', '1', '1')
        self.turnon100= ('turn on', '0', '0', '9', '9')   # parsed data will look like this 
        self.switch4 = ('switch', '0', '0', '1', '1')
        self.switch4_part2 = ('switch', '2', '2', '3', '3')
        self.minusTurnOff4 =  ('turn off', '-1', '-1', '1', '1')
        self.smallGrid = LightTester (2)
        
    def tearDown(self):
        pass
    
    def test_grid(self):
        """ Test that a grid of the correct size is generated"""
        self.assertTrue((self.smallGrid.getGrid() == [[False, False], [False, False]]))
    
    def test_initialState(self): 
        """ Test to ensure counter starts at 0"""
        self.assertEqual(self.MyTest1.counter(),0,"'initial counter' test failed")
          
    
    def test_on(self):
        """ Test that False can be changed to True"""
        self.MyTest1.apply(self.turnon9)  
        self.assertEqual(self.MyTest1.counter(),9,"'turn on' test failed")
    
    def test_off(self):
        """ Test that True can changed to False"""
        self.MyTest1.apply(self.turnon9)  # turn on 9 
        self.MyTest1.apply(self.turnoff4) # turn off 4 -- answer is 5
        self.assertEqual(self.MyTest1.counter(),5,"'turn off' test failed")
        
        
    def test_switch(self):
        """ Test that True can be changed to False"""
        self.MyTest1.apply(self.turnon9)  # turn on 9
        self.MyTest1.apply(self.switch4)   # switch (i.e. turn off) 4 -- answer is 5
        self.assertEqual(self.MyTest1.counter(),5,"'switch on' test failed")
        
    def test_switch_off(self):
        """ Test that False can be changed to True"""
        self.MyTest1.apply(self.turnon9)  # turn on 9
        self.MyTest1.apply(self.switch4)   # turn off 4 -- 5 are now on
        self.MyTest1.apply(self.switch4_part2)   
        # (2,2) is on initially, so now off -- 4 are now on + another 3 = 7
        self.assertEqual(self.MyTest1.counter(),7,"'switch off' test failed")  
        
       
    def test_range(self):   
        """ Test that values outside the range are  brought back to grid range """ 
        self.MyTest1.apply(self.turnon100)  # should scale back to size of this grid
        self.assertEqual(self.MyTest1.counter(),25,"'adjust' test failed")
        self.MyTest1.apply(self.minusTurnOff4)
        self.assertEqual(self.MyTest1.counter(),21,"'adjust' test failed")
        

if __name__== '__main__':
    unittest.main()
