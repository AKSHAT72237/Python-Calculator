"""Utility functions for Scientific Calculator"""
import math

def factorial(n:int)->int:
    if n<0: raise ValueError('factorial() not defined for negative')
    return math.factorial(n)

def nPr(n:int,r:int)->int:
    if r<0 or n<0 or r>n: raise ValueError('Invalid values for nPr')
    return math.factorial(n)//math.factorial(n-r)

def nCr(n:int,r:int)->int:
    if r<0 or n<0 or r>n: raise ValueError('Invalid values for nCr')
    return nPr(n,r)//math.factorial(r)
