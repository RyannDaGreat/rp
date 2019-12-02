'''# ERROR
def b():a
b()'''

'''#NO ERROR
def b():a
a=None
b()'''

'''def b():a#ERROR
a=None
exec('b()',{})'''

'''def b():a#WHY NO ERROR?!
a=None
exec('b()',{'b':b})'''

'''def b():a#WHY ERROR?!
exec('a=None;b()',{'b':b})'''

'''def b():a#WHY ERROR?!
exec('b()',{'a':None,'b':b})'''

'''exec('b()',{'a':None,'b':lambda:a})# WHY ERROR?!'''

'''exec('b()',{'a':None,'b':lambda:eval('a')})# WHY ERROR?!'''

'''exec('b(globals())',{'a':None,'b':lambda g:eval('a',g)})'''# WHY NO ERROR?!
print(3)
d={}
exec('def b():a',d)
exec('a=None',d)
exec('b()',d)