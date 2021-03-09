def dvprd(a,b):
	"""

	Computes the vector product a x b and returns c

	"""
	c[0] = a[1]*b[2] - b[1]*a[2]
	c[1] = a[2]*b[0] - b[2]*a[0]
	c[2] = a[0]*b[1] - b[0]*a[1]
	return c