#! /usr/bin/env python
import numpy
D_1 = 400e-3
d_1 = 180e-3
u_1 = 7.83e3
h_1 = 60e-3
Mass_1  =  numpy.pi * 1/4.0 * (D_1 **2 - d_1 **2) * u_1 * h_1
print Mass_1
D_1 = 400e-3
d_1 = 290e-3
u_1 = 7.83e3
h_1 = 20e-3
width = 90e-3
Mass_2  =  numpy.pi * 1/4.0 * (D_1 **2 - d_1 **2) * u_1 * h_1
Force =2 * numpy.arcsin(width/D_1/2.0) * (2 * numpy.sin(numpy.arcsin(width/D_1/2.0)) * D_1 / 2.0 - d_1 / 2.0 * numpy.sin(numpy.arcsin(width / d_1 /2))) * 5e6
print Mass_2,Force
D_1 = 400e-3
#d_1 = 290e-3
u_1 = 7.83e3
h_1 = 20e-3
Mass_3  =  numpy.pi * 1/4.0 * (D_1 **2) * u_1 * h_1
print Mass_3
print Mass_1 + Mass_2 + Mass_3
