class Body:
    def __init__(self, mass, radius, position, velocity):
        self.mas = mass
        self.rad = radius
        self.pos = np.array([position])
        self.vel = np.array(velocity)
        self.force = np.array([0.,0.])
        self.live = True
    def __str__(self):
        return 'mass:\t' + str(self.mas) + '\n' +    \
               'radii:\t' + str(self.rad) + '\n' +   \
               'pos:\t' + str(self.pos) + '\n' +     \
               'vel:\t' + str(self.vel) + '\n' +     \
               'force:\t' + str(self.force) + '\n' + \
               'live:\t' + str(self.live)
    def speed(self):
        return np.sqrt(sum(v**2 for v in self.vel))
    def _kill(self):
        self.live = False
    def __add__(self, other):
        new_rad = np.sqrt(self.rad**2 + other.rad**2)
        new_mas = self.mas + other.mas
        new_xvel = (self.mas*self.vel[0] + other.mas*other.vel[0])/new_mas
        new_yvel = (self.mas*self.vel[1] + other.mas*other.vel[1])/new_mas
        new_vel = (new_xvel, new_yvel)
        xc = (self.pos[-1][0] + other.pos[-1][0])/2
        yc = (self.pos[-1][1] + other.pos[-1][1])/2
        new_pos = (xc, yc)
        self._kill()
        other._kill()
        return Body(new_mas, new_rad, new_pos, new_vel)

    def _collision(self, other):
        '''check self and other to see if they have collided'''
        rad_dist = self.rad + other.rad
        part_dist = np.sqrt((self.pos[-1][0] - other.pos[-1][0])**2
                            + (self.pos[-1][1] - other.pos[-1][1])**2)
        if part_dist <= rad_dist:
            return self + other
