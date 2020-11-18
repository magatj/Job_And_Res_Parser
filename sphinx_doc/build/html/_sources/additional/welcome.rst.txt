GRID Code Documentation
=======================

Create Horizontal Lines.::

	def hori(c,s):
		for i in range(c):
			print('+', end = '')
			for j in range(s):
				print('-', end ='')
		print('+')


Create Vertical Lines.::	
	
	def verti(c,s):
		for i in range(c):
			print('|', end = '')
			for j in range(s):
			    print(' ',end = '')
		print('|')
		
		
Create Grid.::

	def grid(r,c,s):
		for i in range(r):
			hori(c,s)
			for j in range(s):
				verti(c,s)
		hori(c,s)

Result

grid(5,6,5)

.. program-output:: python 'C:\Users\jesse\Documents\sphinx_doc\source\additional\grid.py'