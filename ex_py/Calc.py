#! /usr/bin/env/python
import numpy as np
file = open("/home/tarena/ex_py/python/55/zyw0803.d49",'r')
file_firstLine = file.readline()
file_flString = file_firstLine.strip('\n')
file_flString = file_flString.split('\t')
for i_firstline in range(0,len(file_flString)):
    if file_flString[i_firstline] == 'Strain':
        i_strain = i_firstline
    elif file_flString[i_firstline] == 'Stress(MPa)':
        i_stress = i_firstline
#strain,stress = np.genfromtxt(file,skip_header = 1,usecols = (i_strain,i_stress),unpack = True)
strain,stress = np.genfromtxt(file,usecols = (i_strain,i_stress),unpack = True)
print i_strain,i_stress
print len(strain),len(stress)
#print  strain
#print  stress
print file_flString

