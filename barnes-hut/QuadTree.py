class QuadTree:
    class _Node:
        def __init__(self, parent, children, upleft, botright, body):
            self._parent = parent
            self._children = children
            self._upleft = upleft
            self._botright = botright
            self._body = body
            self._mass = 0
            self._cmpos = None

    def __init__(self, topleft, botright):
        self._root = QuadTree._Node(None, [None]*4,
                                    (0, topleft), (botright, 0),
                                    Body(0,0,[botright/2,topleft/2],
                                    [0,0]))
        self._root._body.live = False
        self.topleft = topleft
        self.botright = botright

    def is_empty(self):
        return self._root == None

    def _leaves(self, node):
        for child in node._children:
            if child is not None:
                for other in self._leaves(child):
                    yield other
                if child._body is not None:
                    yield child

    def _bodies(self):
        '''yields the actual bodies at the leaves of the quadtree'''
        if not self.is_empty():
            for leaf in self._leaves(self._root):
                yield leaf._body

    def _preorder(self, node):
        for child in node._children:
            if child is not None:
                yield child
                for other in self._preorder(child):
                    yield other

    def __iter__(self):
        '''yields the node of everything that isnt None'''
        if not self.is_empty():
            yield self._root
            for node in self._preorder(self._root):
                yield node

    def _update_node(self, node, body):
        if node._cmpos is None:
            node._cmpos = body.pos[-1]
        else:
            node._cmpos = (node._mass*np.array(node._cmpos) + body.mas*np.array(body.pos[-1]))/(node._mass + body.mas)
#             xcm = (node._mass*node._cmpos[0] + body.mas*body.pos[-1][0])/(node._mass + body.mas)
#             ycm = (node._mass*node._cmpos[1] + body.mas*body.pos[-1][1])/(node._mass + body.mas)
#             node._cmpos = (xcm, ycm)
        node._mass = node._mass + body.mas
        node._body = None

    def insert(self, body):
        self._update_node(self._root, body)
        self._rec_insert(self._root, body)

    def _rec_insert(self, node, body):
        centerx = (node._botright[0] - node._upleft[0])/2
        centery = (node._upleft[1] - node._botright[1])/2
        x = body.pos[-1][0]
        y = body.pos[-1][1]
        right = x >= centerx
        top = y >= centery

        if x > self.botright or y > self.topleft:
            # x = x % self.botright
            # y = y % self.topleft
            # body.pos[-1] = [x,y]
            # self.insert(body)
            return

        if not right and top:
            '''top left'''
            if node._children[0] is None:
                node._children[0] = QuadTree._Node(node, [None]*4,
                                               (0,self.topleft),
                                               (centerx, centery),
                                               body)
            else:
                if node._children[0]._body is not None:
                    bod = node._children[0]._body
                    node._children[0] = QuadTree._Node(node._children[0], [None]*4,
                                               (0,self.topleft),
                                               (centerx, centery),
                                               None)
                    self._update_node(node._children[0], bod)
                    self._rec_insert(node._children[0], bod)
                self._update_node(node._children[0], body)
                self._rec_insert(node._children[0], body)
        elif right and top:
            '''top right'''
            if node._children[1] is None:
                node._children[1] = QuadTree._Node(node, [None]*4,
                                               (centerx, self.topleft),
                                               (self.botright, centery),
                                               body)
            else:
                if node._children[1]._body is not None:
                    bod = node._children[1]._body
                    node._children[1] = QuadTree._Node(node._children[0], [None]*4,
                                               (centerx, self.topleft),
                                               (self.botright, centery),
                                               None)
                    self._update_node(node._children[1], bod)
                    self._rec_insert(node._children[1], bod)
                self._update_node(node._children[1], body)
                self._rec_insert(node._children[1], body)
        elif not right and not top:
            '''bottom left'''
            if node._children[2] is None:
                node._children[2] = QuadTree._Node(node, [None]*4,
                                               (0, centery),
                                               (centerx, 0),
                                               body)
            else:
                if node._children[2]._body is not None:
                    bod = node._children[2]._body
                    node._children[2] = QuadTree._Node(node._children[2], [None]*4,
                                               (0, centery),
                                               (centerx, 0),
                                               None)
                    self._update_node(node._children[2], bod)
                    self._rec_insert(node._children[2], bod)
                self._update_node(node._children[2], body)
                self._rec_insert(node._children[2], body)
        elif right and not top:
            '''bottom right'''
            if node._children[3] is None:
                node._children[3] = QuadTree._Node(node, [None]*4,
                                               (centerx, centery),
                                               (self.botright, 0),
                                               body)
            else:
                if node._children[3]._body is not None:
                    bod = node._children[3]._body
                    node._children[3] = QuadTree._Node(node._children[3], [None]*4,
                                               (centerx, centery),
                                               (self.botright, 0),
                                               None)
                    self._update_node(node._children[3], bod)
                    self._rec_insert(node._children[3], bod)
                self._update_node(node._children[3], body)
                self._rec_insert(node._children[3], body)
        else:
            raise ValueError('uhhhh')

    def _bodybody_force(self, bod1, bod2):
        R = np.array(bod2.pos[-1]) - np.array(bod1.pos[-1])
        R_norm = np.linalg.norm(R)
        return (G*bod1.mas*bod2.mas/(np.sqrt(R_norm**2 + epsilon**2)**3))*R

    def _nodebody_force(self, body, node):
        R = np.array(node._cmpos) -  np.array(bod.pos[1])
        R_norm = np.linalg.norm(R)
        return (G*body.mas*node._mass/(np.sqrt(R_norm**2 + epsilon**2)**3))*R

    def _recur_force(self, body, node):
        for child in node._children:
            if child is not None:
                if child._body is None:
                    cm_dist = np.sqrt((body.pos[-1][0] - child._cmpos[0])**2 +
                                     (body.pos[-1][1] - child._cmpos[1])**2)
                    if child._botright[0]/cm_dist < theta:
                        bdy.force += self._nodebody_force(bdy, node)
                    else:
                        self._recur_force(body, child)
                else:
                    if child._body is not body:
                        body.force += self._bodybody_force(body, child._body)

    def update_force(self):
        for bdy in self._bodies():
            self._recur_force(bdy, self._root)

    def _time_step(self, dt):
        self.update_force()
        for body in self._bodies():
            if body.live:
                body.vel = body.vel + dt*body.force
                new_pos = body.pos[-1] + body.vel*dt
                body.pos = np.append(body.pos, [new_pos], axis = 0)
