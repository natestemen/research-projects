import numpy as np
from scipy.integrate import simps
from scipy.optimize import minimize


def orthonormal_basis(x, N=10, inner_prod=None, start=None):
	if inner_prod is None:
		inner_prod = lambda f, g: simps(f*g, x)
	if start is None:
		mx = max(x)
		start = [np.sin(np.pi*n*x/mx) for n in range(1, N+1)]
	def norm(u, sqrt=True):
		if sqrt:
			return np.sqrt(inner_prod(u, u))
		return inner_prod(u, u)
	def proj(u, v):
		return u * inner_prod(u, v) / norm(u, sqrt=False)
	gs = []
	for v in start:
		for u in gs:
			v -= proj(u, v)
		gs.append(v / norm(v))
	return gs

def lin_combination(coeffs, basis):
	if len(coeffs) != len(basis):
		raise ValueError('cofficients and basis must have same size')
	soln = np.zeros(len(basis[0]))
	for c, b in zip(coeffs, basis):
		soln += c*b
	return soln




# def


# class Minimizer:
# 	def __init__(self, functional, constraint, domain, inner_prod=None):
# 		self.functional = functional
# 		self.constraint = constraint
# 		self.domain = domain
# 		self.inner_prod = inner_prod
#
# 	def orthonormal_basis(self, n=10, starting=None):
# 		a, b = self.domain[0], self.domain[1]
# 		x = np.linspace(a, b, self.num_pts)
# 		if starting is None:
# 			starting = [np.sin(np.pi*i*x/b) for i in range(1, n + 1)]
# 		if self.inner is None:
# 			self.inner = lambda f, g: simps(f*g, x)
# 		def projection(u, v):
# 			return u * self.inner(u, v) / self.inner(u, u)
# 		def norm(u):
# 			return np.sqrt(self.inner(u, u))
# 		orthonormal = []
# 		for v in starting:
# 			for u in orthonormal:
# 				v -= projection(u, v)
# 			orthonormal.append(v / norm(v))
# 		self.basis = orthonormal
# 		return orthonormal
#
# 	def approximate_solution(self, coefficients):
# 		soln = np.zeros(self.num_pts)
# 		for c, b in zip(coefficients, self.basis):
# 			soln += c * b
# 		return soln
#
# 	def min(self, guess, args, disp=True):
# 		cons = {'type': 'eq', 'fun': self.constraint}
# 		ops = {'maxiter': 1000, 'disp': disp}
# 		minimum = minimize(self.functional, guess, args=args, constraints=cons, options=ops)
# 		if not minimum.success:
# 			raise ValueError('Did not succeed :(')
# 		return minimum
#
# 	def min_soln(self, guess, args, disp=True):
# 		m = self.min(guess, args, disp=True)
# 		return self.approximate_solution(m.x)
