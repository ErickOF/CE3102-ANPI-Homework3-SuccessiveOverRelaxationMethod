# -*- coding: utf-8 -*-
"""
Natural Cubic Splines Interpolation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17iYG0Kcj-b43oVOGbbDuQ0_xDgvcghrn

# Natural Cubic Splines Interpolation
## Inputs
* $\vec{p} = ((x_{0}, y_{0}), (x_{1}, y_{1}), ..., (x_{n}, y_{n}), (x_{n+1}, y_{n+1}))$

## Outputs
* $a, b, c, d$: interpolation coeficients
"""

import numpy as np
import matplotlib.pyplot as plt


def relajacion(A, b, x0, omega=0.5, tol=1e-8):
    """
    This is an implementation of the succesive over-relaxation method.

    Inputs:
    
      A: nxn numpy matrix
    
      b: n dimensional numpy vector
    
      omega: relaxation factor
    
      x0: an initial value
    
      tol: tolerance
    
    Returns:
    
      x: solution matrix
    """
    x = x0.copy()
    residual = np.linalg.norm(np.matmul(A, x) - b)
    while residual > tol:
        for i in range(A.shape[0]):
            sigma = 0
            for j in range(A.shape[1]):
                if j != i:
                    sigma += A[i][j] * x[j]
            x[i] = (1 - omega) * x[i] + (omega / A[i][i]) * (b[i] - sigma)
        residual = np.linalg.norm(np.matmul(A, x) - b)
    return x

def trazador_cubico(points):
    """
    Natural Cubic Splines Interpolation

    @points - list or tuple with points to compute interpolation
    
    return sigmas
    """
    # Validate some conditions
    if not isinstance(points, (list, tuple)):
        raise ValueError("'points' must be a list or tuple")
    elif len(points) < 4:
        raise ValueError("The length of 'points' must be greater than 1")

    # Convert points to numpy array
    points = np.array([np.array(p) for p in points])
    # Compute hk
    hk = points[1:, 0] - points[:-1, 0]
    # Compute delta_yk
    delta_yk = points[1:, 1] - points[:-1, 1]
    # Matrix and vector for solve linear system equation
    A, b = [], []
    # Amount of points - 1 (n)
    k = hk.shape[0]
    for i in range(1, k):
        # First case sigmas[1] = 0
        if i == 1:
            A.append([2*(hk[i - 1] + hk[i]), hk[i]] + [0]*(k - 3))
        # Second case sigmas[n+1] = 0
        elif i == k-1:
            A.append([0]*(k - 3) + [hk[i - 1], 2*(hk[i - 1] + hk[i])])
        else:
            A.append([0]*(i - 2) + [hk[i - 1], 2*(hk[i - 1] + hk[i]),
                                    hk[i]] + [0]*(k - 2 - i))
        b.append(6*(delta_yk[i]/hk[i] - delta_yk[i - 1]/hk[i - 1]))

    # Convert to numpy array
    A = np.array([np.array(a) for a in A])
    b = np.array(b)

    # Solving system linear equation
    x0 = np.zeros(b.shape)
    sigmas = relajacion(A, b, x0)
    # Append sigmas[1] = 0 and sigmas[n+1] = 0
    sigmas = np.append(0, np.append(sigmas, 0))

    # Coeficients
    a, b, c, d = [[], [], [], []]
    # Initial points
    xk = points[:, 0]
    yk = points[:, 1]
    # Compute coeficients
    for i in range(k-1):
        a.append((sigmas[i+1] - sigmas[i])/(6*hk[i]))
        b.append(sigmas[i]/2)
        c.append((yk[i+1] - yk[i])/hk[i] - (2*hk[i]*sigmas[i]+hk[i]*sigmas[i+1])/6)
        d.append(yk[i])

    # To numpy array
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    d = np.array(d)

    return a, b, c, d

def plot_ncsi(points, a, b, c, d):
    """
    Plotter for Natural Cubic Splines Interpolation

    @points - Initial points of NCSI
    
    @a - first coeficient
    
    @b - second coeficient
    
    @c - third coeficient
    
    @d - fourth coeficient
    """
    # Compute x values
    x = np.linspace(points[0][0], points[-1][0], 1000)
    # Interpolation polynomial
    pk = []
    # Compute interpolation polynomial
    for xk in x:
        for i in range(a.shape[0]):
            if points[i][0] <= xk <= points[i+1][0]:
                pk.append([xk, a[i]*(xk - points[i][0])**3 + b[i]*(xk - points[i][0])**2 + c[i]*(xk - points[i][0]) + d[i]])

    # Plot function
    plt.title('Natural Cubic Splines Interpolation')
    plt.plot([x for x, y in pk], [y for x, y in pk])
    plt.scatter([x for x, y in points], [y for x, y in points], c='red')
    plt.grid(True)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.show()


if __name__ == '__main__':
    points = [[-5, 0], [-4.5, 0.0707], [-4, 0], [-3.5, -0.0909],
              [-3, 0], [-2.5, 0.1273], [-2, 0], [-1.5, -0.2122],
              [-1, 0], [-0.5, 0.6366], [ 0, 1], [ 0.5,  0.6366],
              [ 1, 0], [ 1.5, 0.2122], [ 2, 0], [ 2.5,  0.1273],
              [ 3, 0], [ 3.5, 0.0909], [ 4, 0], [ 4.5,  0.0707],
              [5, 0]]
    a, b, c, d = trazador_cubico(points)
    plot_ncsi(points, a, b, c, d)
