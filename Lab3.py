import math

h0 = 0.1   # The default used h0
N = 200    # The default used N steps of the Euler method

# This function writes a one dimensional list to a file with name f_name.
def write_to_file(f_name, lst):
    temp = open(f_name, 'w')
    i = 1
    for e in lst:
        temp.write("%d %.20f\n" % (i, e))
        i += 1
    temp.close()

# This function writes a two dimentional list to a file with name f_name.    
def write_to_file2(f_name, lst):
    temp = open(f_name, 'w')

    for e in lst:
        temp.write("%f %d\n" % (e[0], e[1]))

    temp.close()

# This function finds the maximum value (in absolute value) of a 1D list
def lst_max(lst):
    lrg = 0
    for e in lst:
        if abs(e) > lrg:
            lrg = abs(e)
    return lrg

# eulerMethod takes in initial position and velocity x0 and v0 respectively, as 
# well as step size h, and returns tuple (x, v) the new subsequent position and
# velocity estimated by the explicited Euler Method.
def eulerMethod(x0, v0, h):
    x = x0 + h * v0
    v = v0 - h * x0
    return (x, v)

# Implements the explicit euler method using initial conditions x0 and v0 in 
# addition to step size h, n times.
def eulerMethodN(x0, v0, h, n):
    lst = [[x0], [v0]]
    temp = (x0, v0)
    for index in range(n):
        temp = eulerMethod(temp[0], temp[1], h)
        lst[0].append(temp[0])
        lst[1].append(temp[1])
    return lst

# Determines the (x, v) tuple using the solved differential equation form for 
# an ideal spring with k/m = 1.
def springMethod(x0, v0, t):
    cost = math.cos(t)
    sint = math.sin(t)
    xt = x0 * cost + v0 * sint
    vt = v0 * cost - x0 * sint
    return (xt, vt)

def springMethodN(x0, v0, h, n):
    lst = [[x0], [v0]]
    t = 0
    for index in range(n):
        t += h
        temp = springMethod(x0, v0, t)
        lst[0].append(temp[0])
        lst[1].append(temp[1])
    return lst

# Used in problem 2 to plot the global errors over a number of n for a given h
def spring_global_error(x0, v0, h, n):
    eul_meth = eulerMethodN(x0, v0, h, n)
    spr_meth = springMethodN(x0, v0, h, n)
    lst = [[0], [0]]
    for index in range(n):
        lst[0].append(spr_meth[0][index + 1] - eul_meth[0][index + 1])
        lst[1].append(spr_meth[1][index + 1] - eul_meth[1][index + 1])
    return lst

# Used in problem 3 to find the truncation error as h shrinks
def expError(x0, v0, h, n):
    denom = 1
    lst = []
    for index in range(n):
        eul_meth = eulerMethod(x0, v0, h / denom)
        spr_meth = springMethod(x0, v0, h / denom)
        diff = spr_meth - eul_meth
        lst.append(diff)
        denom /= 2
    return lst

def eulerEnergy(x, v, h):
    return x ** 2 + v ** 2

# Used to compute problem 4, the evolution of the energy using the euler method
def sprEnergyN(x0, v0, h, n):
    lst = [0]
    energy = x0 ** 2 + v0 ** 2
    posVel = eulerMethodN(x0, v0, h, n)
    x = posVel[0]
    v = posVel[1]
    for index in range(n):
        temp = eulerEnergy(x[index], v[index], h)
        lst.append(energy - temp)
    return lst

# Used to compute problem 5, the implict Euler method.
def implicitEuler(x0, v0, h):
    denom = 1 + h ** 2
    x = x0 + h * v0
    v = v0 - h * x0
    return (x / denom, v / denom)  

# The N version of implicit Euler.
def implicitEulerN(x0, v0, h, n):
    lst = [[x0], [v0]]
    temp = (x0, v0)
    for index in range(n):
        temp = implicitEuler(temp[0], temp[1], h)
        lst[0].append(temp[0])
        lst[1].append(temp[1])
    return lst

# The implicit error's global error.
def implicitError(x0, v0, h, n):
    imp_meth = implicitEulerN(x0, v0, h, n)
    spr_meth = springMethodN(x0, v0, h, n)
    lst = [[0], [0]]
    for index in range(n):
        lst[0].append(spr_meth[0][index + 1] - imp_meth[0][index + 1])
        lst[1].append(spr_meth[1][index + 1] - imp_meth[1][index + 1])
    return lst

def impEnergyN(x0, v0, h, n):
    lst = [0]
    energy = x0 ** 2 + v0 ** 2
    posVel = implicitEulerN(x0, v0, h, n)
    x = posVel[0]
    v = posVel[1]
    for index in range(n):
        temp = eulerEnergy(x[index], v[index], h)
        lst.append(energy - temp)
    return lst

def main():
    global h0
    global N
    
    euler = eulerMethodN(0, 10, h0, N)
    spring = springMethodN(0, 10, h0, N)
    P2 = spring_global_error(0, 10, h0, N)
    
    # Problem 1 files
    write_to_file("euler_pos.txt", euler[0])
    write_to_file("euler_vel.txt", euler[1])
    
    write_to_file("true_pos.txt", spring[0])
    write_to_file("true_vel.txt", spring[1])
    
    # Problem 2 files
    write_to_file("pos_err.txt", P2[0])
    write_to_file("vel_err.txt", P2[1])
    
    # Problem 3 files
    num = 1
    P3 = []
    for i in range(10):
        P3.append(lst_max(spring_global_error(0, 10, h0 / num, N)[0]))
        num *= 2
    write_to_file("h_scale.txt", P3)
    
    # Problem 4 files
    write_to_file("euler_energy.txt", sprEnergyN(0, 10, h0, N))
    
    # Problem 5 files
    imp_err = implicitError(0, 10, h0, N)
    write_to_file("imp_pos_error.txt", imp_err[0])
    write_to_file("imp_vel_error.txt", imp_err[1])
    write_to_file("implicit_energy.txt", impEnergyN(0, 10, h0, N))
    
main()
