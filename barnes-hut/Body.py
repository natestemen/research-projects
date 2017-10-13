import numpy as np

class Body:
	def __init__(self, mass, radius, position, velocity):
		self.mass = mass
		self.rad = radius
		self.pos = np.array(position)
		self.vel = np.array(velocity)

	def __str__(self):
		return 'mass:\t' + str(self.mass) + '\n' + \
			'radii:\t' + str(self.rad) + '\n' +   \
			'pos:\t' + str(self.pos) + '\n' +     \
			'vel:\t' + str(self.vel)

	def speed(self):
		return np.sqrt(sum(v**2 for v in self.vel))

	def __add__(self, other):
		new_rad = np.sqrt(self.rad**2 + other.rad**2)
		new_mas = self.mass + other.mas
		new_vel = (self.mass*self.vel + other.mas*other.vel) / new_mas
		new_pos = (self.pos + other.pos) / 2
		return Body(new_mas, new_rad, new_pos, new_vel)

	def _collision(self, other):
		'''check self and other to see if they have collided'''
		rad_dist = self.rad + other.rad
		com_dist = np.sqrt(sum(v**2 for v in (self.pos - other.pos)))
		# return rad_dist, com_dist
		if com_dist <= rad_dist:
			return self + other

B = Body(1,1,[1,1],[0,1])
B.mas
D = Body(2,2, [-1,0],[0,0])
B.rad
New = D._collision(B)
