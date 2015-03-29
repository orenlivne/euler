'''
============================================================
"Fizz buzz" is a word game we will use to teach the robots about division. Let's learn computers.

You should write a function that will receive a positive integer and return:
"Fizz Buzz" if the number is divisible by 3 and by 5;
"Fizz" if the number is divisible by 3;
"Buzz" if the number is divisible by 5; 
The number as a string for other cases.
Input: A number as an integer.

Output: The answer as a string.

http://www.checkio.org/mission/fizz-buzz/

Created on Mar 29, 2015
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
def fizzbuzz(x):
    mod3 = x % 3
    mod5 = x % 5
    if mod3 == 0 and mod5 == 0: return "Fizz Buzz"
    elif mod3 == 0: return "Fizz"
    elif mod5 == 0: return "Buzz"
    else: return str(x)
    
if __name__ == '__main__':
    assert fizzbuzz(15) == "Fizz Buzz"
    assert fizzbuzz(6) == "Fizz"
    assert fizzbuzz(5) == "Buzz"
    assert fizzbuzz(7) == "7"
