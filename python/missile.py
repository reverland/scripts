import matplotlib.pyplot as plt
import numpy as np
tolerance = 1e-1
radius = np.pi

# missile 1
x_m1, y_m1 = -np.pi, 0
v_m1 = 5

# missile 2
x_m2, y_m2 = 0, np.pi
v_m2 = v_m1
# missile 3
x_m3, y_m3 = np.pi, 0
v_m3 = v_m1
# missile 4
x_m4, y_m4 = 0, -np.pi
v_m4 = v_m1

plt.figure(figsize=(10, 10), dpi=80)
plt.title(" missile flight simulator ", fontsize=40)
plt.xlim(-4, 4)
plt.ylim(-4, 4)
#plt.xticks([])
#plt.yticks([])

# set spines
ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data', 0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data', 0))
plt.xticks([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi], [r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])
plt.yticks([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi], [r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])

plt.annotate('missile start point', xy=(x_m1, y_m1),  xycoords='data',
             xytext=(+15, +15), textcoords='offset points', fontsize=12,
             arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

# alpha labels
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontsize(16)
    label.set_bbox(dict(facecolor='white', edgecolor='None', alpha=0.65))


class ob(object):
    """docstring for ob"""
    def __init__(self, x, y):
        self.x = x
        self.y = y


class missile(ob):
    """docstring for missile"""
    def __init__(self, x, y):
        super(missile, self).__init__(x, y)

    def forward(self, v, target):
        """docstring for forward"""
        if self.x < target.x:
            alpha = np.arctan((target.y - self.y) / (target.x - self.x))
        elif self.x > target.x:
            alpha = np.pi + np.arctan((target.y - self.y) / (target.x - self.x))
        elif self.x == target.x and self.y < target.y:
            alpha = np.pi / 2
        else:
            alpha = -np.pi / 2
        self.x = self.x + v * 0.01 * np.cos(alpha)
        self.y = self.y + v * 0.01 * np.sin(alpha)
        return self.x, self.y

    def distance(self, target):
        """docstring for distance"""
        return np.sqrt((self.x - target.x) ** 2 + (self.y - target.y) ** 2)


class target(ob):
    """docstring for target"""
    def __init__(self, x, y):
        super(target, self).__init__(x, y)

    def newposition(self, x, y):
        """docstring for newposition"""
        self.x = x
        self.y = y

m1 = missile(x_m1, y_m1)
m2 = missile(x_m2, y_m2)
m3 = missile(x_m3, y_m3)
m4 = missile(x_m4, y_m4)

while True:
    if m1.distance(m2) < tolerance or m1.distance(m3) < tolerance or m1.distance(m4) < tolerance:
        print "collision"
        plt.plot(x_m1, y_m1, 'o')
        plt.annotate('crash point', xy=(x_m1, y_m1),  xycoords='data',
                     xytext=(+15, +15), textcoords='offset points', fontsize=12,
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
        plt.pause(0.1)
        plt.show()
        break
    elif m3.distance(m2) < tolerance or m3.distance(m4) < tolerance:
        print "collision"
        plt.plot(x_m3, y_m3, 'o')
        plt.annotate('crash point', xy=(x_m3, y_m3),  xycoords='data',
                     xytext=(+15, +15), textcoords='offset points', fontsize=12,
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
        plt.pause(0.1)
        plt.show
        break
    x_m1, y_m1 = m1.forward(v_m1, m2)
    x_m2, y_m2 = m2.forward(v_m2, m3)
    x_m3, y_m3 = m3.forward(v_m3, m4)
    x_m4, y_m4 = m4.forward(v_m4, m1)
    #print alpha, beta
    plt.plot(x_m1, y_m1, 'bx', alpha=.5)
    plt.plot(x_m2, y_m2, 'k*', alpha=.5)
    plt.plot(x_m3, y_m3, 'r.', alpha=.5)
    plt.plot(x_m4, y_m4, 'gp', alpha=.5)
    plt.legend(("missile1", "missile2", "missile3", "missile4"), loc="upper left", prop={'size': 12})
    plt.pause(0.1)
