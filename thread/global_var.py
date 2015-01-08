'''
============================================================
TBA

Created on Jun 18, 2013
@author: Oren Livne <livne@uchicago.edu>
============================================================
'''
def another_function():   
    global boo
    print boo  

def say_boo_twice():   
    global boo
    boo = 'Boo!'
    print boo, boo
    print '\t', 'In called function',
    another_function()  

print 'in function where var is defined:',
say_boo_twice() 
print 'outside the function: ' + boo  # works
print 'In another function:',
another_function()
