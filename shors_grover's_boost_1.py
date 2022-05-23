# WORK IN PROGRESS
""" Shor's Algorithm on a SHA 256 key using an n-qubit Grover's Algorithm to magnify the searched state"""

import string
import random
import hashlib
import time
import binascii
import qiskit
from qiskit import IBMQ
IBMQ.save_account('2330fa80e6cdc16978c9d943bb82b00665b18d690f370cdc8874f617a1650490dba8b1aa035e152e40a7240c7f626592c9871f4f92d65945b63eb60e85f4a99d')
from qiskit import QuantumCircuit, execute, Aer, IBMQ
from qiskit.compiler import transpile, assemble
from qiskit.tools.jupyter import *
from qiskit.visualization import *
provider = IBMQ.load_account()
import math
import matplotlib
from qiskit.tools.visualization import plot_histogram
import itertools
from random import randint
from math import gcd
from sys import argv
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import execute, BasicAer

backend = BasicAer.get_backend('qasm_simulator')

#Input Step 1 SHA 256 encryption for password       
test_password = "guessguess"
hexkey = hashlib.sha256(test_password.encode()).hexdigest()
print("Hash: %s" % hexkey)
ini_string = hexkey
j = int(ini_string, 16)  
bStr = '' 
while j > 0:
    bStr = str(j % 2) + bStr
    j = j >> 1    
    res = bStr
print("BINARY HASH SOLUTION:", str(''.join(res))) 
n = int(hexkey, 16)         
print('Value in hexadecimal:', hexkey)
print('Value in decimal:', n)

"""Shor's algorithm"""

def multiplicative_order(a, n):
    order = 1
    mod_exp = a
    while mod_exp != 1 and n != 0:
        order += 1
        mod_exp = (mod_exp * a) % n
    return order

def visualize(a, n):
    for i in range(1, len(n)):
        o = a**i % n
        print("{}^{} mod {} = {}".format(a, i, n, o))
    r = multiplicative_order(x, N)
    if x != 0 and x < len(x):
            print('Multiplicative Order of {} mod {} => {}'.format(x, n, r))
            
def shors(x):
    while True:
        
        # Step 2 in actual Shor's algorithm quantum fourier transform will be
        # implemented here.       
        r = multiplicative_order(x, n)
        if x != 0 and r < len(res):
            print('Multiplicative Order of {} mod {} => {}'.format(x, n, r))
            break
        
        # Step 3        
        if r % 2 != 0:
            print('{} is not even :( going back to first step...\n'.format(r))
            continue
        elif (x**(r//2)+1) % n == 0:
            print('{} is a multiple of n :( back to first step...\n'.format(r))
            continue
        else:
            factor1 = gcd(n, (x**(r//2)+1))
            factor2 = gcd(n, (x**(r//2)-1))
           
        # ->>  n-qubit Grover's algorithm called here  <<-       
            grovers_boost_factor1 = n.grovers(factor1)
            grovers_boost_factor2 = n.grovers(factor2)    
        return [factor1, factor2, grovers_boost_factor1, grovers_boost_factor2]
"""
A quantum oracle inverts the amplitude of the searched state. Then,
the diffuser flips all states about the mean amplitude, therefore,
magnifying the searched state.
"""
    
def main():
    if len(argv) != 2:
        print('Usage: {} <number>'.format(argv[0]))
        return
    try:
        n = int(argv[1])
    except ValueError:
        print('Invalid input')
        return
    if n <= 2:
        print('n is too small!')
        return
    factors = shors(res)
    print('Factor of {} is {} and {}\n'.format(n, factors[0], factors[1]))

if __name__ == '__main__':
    main()
    

    
"""
Grover's tasks:
Given a classical function f(x):{0,1}n→{0,1},where n is the bit-size of the
search space, find an input x_0 for which f(x_0)=1.
To implement Grover's algorithm to solve a problem, you need to:
Transform the problem to the form of a Grover's task.
For example, suppose you want to find the factors of an integer M
using Grover's algorithm. You can transform the integer factorization problem
to a Grover's task by creating a function f_M(x)=1[r],
where 1[r]=1 if r=0 and 1[r]=0 if r≠0 and r is the remainder of M/x.
This way, the integers x_i that make f_M(x_i)=1 are the factors of M
and you have transformed the problem to a Grover's task.
Implement the function of the Grover's task as a quantum oracle.
To implement Grover's algorithm, you need to implement the function f(x)
of your Grover's task as a quantum oracle.
Use Grover's algorithm with your oracle to solve the task.
Once you have a quantum oracle, you can plug it into your Grover's
algorithm implementation to solve the problem and interpret the output.
The following example shows how you would express the function
f_M(x)=1[r] of the factoring problem as a quantum operation:
Classically, you would compute the remainder of the division M/x
and see if it's equal to zero. If it is, the program outputs 1,
and if it's not, the program outputs 0. You need to:Compute the
remainder of the division. Apply a controlled operation over
the output bit so that it's 1 if the remainder is 0.
You need to calculate a division of two numbers with a quantum operation.
"""

shots = math.pi/4*math.sqrt(len(res)/2)

"""n-qubit Grover's algorithm"""    

def grovers():
    qc = QuantumCircuit(res,res)
    pi = math.pi
    qr = QuantumRegister(res, 'qc')
    qc.add_register(qr)
    qc.qregs

    cr = ClassicalRegister(4 , 'cr')
    qc.add_register(cr)

    #######################
    ######## init #########
    #######################

    for n in range(4):
         qc.h([n])

    #######################
    ### Oracle for 0010 ###
    #######################
         
    for j in range(4):
             if n != j:
                qc.x([j])
                
    for i in range(0, key_len-3, 4):
        if n!=0:
            qc.cp(pi/4, qr[i], qr[i+3])
            qc.cx(qr[i], qr[i+1])
            qc.cp(-pi/4, qr[i+1], qr[i+3])

            qc.cx(qr[i], qr[i+1])
            qc.cp(pi/4, qr[i], qr[i+3])
            qc.cx(qr[i+1], qr[i+2])
            qc.cp(-pi/4, qr[i+2], qr[i+3])
            qc.cx(qr[i], qr[i+2])
            qc.cp(pi/4, qr[i+2], qr[i+3])
            qc.cx(qr[i+1], qr[i+2])

            qc.cp(-pi/4, qr[i+2], qr[i+3])
            qc.cx(qr[i], qr[i+2])
            qc.cp(pi/4, qr[i+2], qr[i+3])

    for j in range(4):
        qc.x([j])

    #######################
    #### Amplification ####
    #######################
        
    for j in range(4):
        qc.h([j])

    for j in range(4):
        qc.x([j])

    ######## cccZ #########

    for i in range(0, key_len-3, 4):
        if n!=0:
            qc.cp(pi/4, qr[i], qr[i+3])
            qc.cx(qr[i], qr[i+1])
            qc.cp(-pi/4, qr[i+1], qr[i+3])

            qc.cx(qr[i], qr[i+1])
            qc.cp(pi/4, qr[i], qr[i+3])
            qc.cx(qr[i+1], qr[i+2])
            qc.cp(-pi/4, qr[i+2], qr[i+3])
            qc.cx(qr[i], qr[i+2])
            qc.cp(pi/4, qr[i+2], qr[i+3])
            qc.cx(qr[i+1], qr[i+2])

            qc.cp(-pi/4, qr[i+2], qr[i+3])
            qc.cx(qr[i], qr[i+2])
            qc.cp(pi/4, qr[i+2], qr[i+3])

    ####### end cccZ #######

    for j in range(4):
        qc.x(qr[j])
    for j in range(4):
        qc.h(qr[j])

    #########################################################
    ####### Measure on theoretical quantum processor ########
    #########################################################

    qc.barrier(qr)
    for i in range(0, key_len%(key_len-3), 4):
        qc.measure(qr[i], cr[i])
        qc.measure(qr[i+1], cr[i+1])
        qc.measure(qr[i+2], cr[i+2])
        qc.measure(qr[i+3], cr[i+3])
        
    # submit job #
    qc.measure_all()
    job = execute(qc, backend, shots=shots)

########################################
### ! call shors(Value in decimal) ! ###
########################################

shors(n)
