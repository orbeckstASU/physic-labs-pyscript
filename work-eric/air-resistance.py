import numpy as np
import matplotlib.pyplot as plt

# RK4 from class (11_ODE_applications: ode.py)
def rk4(y, f, t, h):
    """Runge-Kutta RK4 step"""
    k1 = f(t, y)
    k2 = f(t + 0.5 * h, y + 0.5 * h * k1)
    k3 = f(t + 0.5 * h, y + 0.5 * h * k2)
    k4 = f(t + h, y + h * k3)
    return y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


def C_L(S):
    return 0.62 * S**0.7

def simulate_baseball(v0, omega, r0=None,
                      h=0.01, C_D=0.40, g=9.81, rho=1.225,
                      r=0.07468/2, m=0.14883,
                      R_homeplate=18.4):
    """simulate baseball pitch
    
    Parameters
    ----------
    v0 : array
         initial velocity (vx, vy, vz) in m/s
    omega : array
         angular velocity vector of the ball ("spin"), in rad/s
    r0 : array, optional
         initial position of the ball (in m) when it leaves the pitcher's hand
         as (x, y, z); the default is (0, 2, 0)
    h : float, optional
         integration time step in s, default is 0.01 s
    C_D : float, optional
         drag coefficient, default is 0.40
    g : float, optional
         acceleration due to gravity, default 9.81 kg/(m*s^2)
    rho : float, optional
         density of air, default 1.225 kg/m^3
    r : float, optional
         radius of the baseball
    m : float, optional
         mass of the baseball
    R_homeplate : float, optional
         distance of the catcher from the pitcher
         
    Returns
    -------
    
    positions : array
         The array contains an entry (time, x, y, z) for each time step.
    """
    # all SI units (kg, m)
    if r0 is None:
        r0 = np.array([0, 0, 0])  # pitching at 2m height
    
    omega = np.asarray(omega)
        
    domega = np.linalg.norm(omega)
    A = np.pi*r**2
    rhoArm = rho * A * r / m
    b2 = 0.5 * C_D * rho * A
    
    a_gravity = np.array([0, -g, 0])

    def f(t, y):
        # y = [x, y, z, vx, vy, vz]
        v = y[3:]
        dv = np.linalg.norm(v)
        S = r*domega/dv
        a_magnus = 0.5 * C_L(S) * rhoArm / S * np.cross(omega, v)
        a_drag = -b2/m * dv * v
        a = a_gravity + a_drag + a_magnus
        return np.array([y[3], y[4], y[5],
                         a[0], a[1], a[2]])

    t = 0
    # initialize 3D!
    y = np.array([r0[0], r0[1], r0[2], v0[0], v0[1], v0[2]], dtype=np.float64)
    positions = [[t, y[0], y[1], y[2]]] # record t, x and y, z
    
    while y[1] >= -0.001:
        t += h
        y[:] = rk4(y, f, t, h)
        positions.append([t, y[0], y[1], y[2]])  # record t, x and y, z
        
    return np.array(positions)


# In the MLB:
# Average homerun exit velocity: 95 mph = 42.47 m/s
# Average homerun launch angle: 25-30 degrees = 0.436-0.524 rad
# Average homerun spin rate: 1500 rpms 
# 42.47 m/s at 25 degrees: vx, vy = 38.49, 17.95
# 42.47 m/s at 30 degrees: vx, vy = 36.78, 21.24

# Simulation with 95 mph at 30 degrees and 1500 rpm
r = simulate_baseball([36.78, 21.24, 0], omega=157.0796 * np.array([0,0,1]), C_D=0.4)

idx = 2  # y
plt.plot(r[:,1], r[:,idx])
plt.xlabel("$x$ (m)")
plt.ylabel("$y$ (m)")
plt.title("Projectile Motion")
plt.show()

print(f"Distance: {r[-1, 1]:.3f} meters = {(r[-1, 1]*3.28):.3f} feet")