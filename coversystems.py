import itertools
import numpy as np
import math
from sympy import factorint
from math import factorial as fact


LCMlist_6 = [12,18,24]

LCMlist_7 = [36,48]

LCMlist_10 = [90,120,156,162,288,384]





def right_div(n):
  div_arr = []
  for i in range(2,math.floor(n/2)+1):
    if n % i == 0:
      div_arr=div_arr+[i]
  div_arr=div_arr+[n]
  return div_arr



#hello



def findsubsets(s, n):
    return list(itertools.combinations(s, n))


def find_lcm(num1,num2):
  if(num1>num2):
    num = num1
    den = num2
  else:
    num = num2
    den = num1
  rem = num % den
  while(rem!= 0):
    num = den
    den = rem
    rem = num % den
  gcd = den
  lcm = int(int(num1 * num2)/int(gcd))
  return lcm


def get_modlcm(system):
  num1 = system[0][1]
  num2 = system[1][1]
  lcm = find_lcm(num1, num2)

  for i in range(2, len(system)):
    lcm = find_lcm(lcm, system[i][1])

  return lcm



def check_if_cs(system):
  tracker1 = 0
  for n in range(0, get_modlcm(system)):
    tracker2 = 1
    for j in range(0, len(system)):
      if ((n - system[j][0])% system[j][1]) == 0:
        tracker2 = 0
    if tracker2 == 1:
      tracker1 = 1
  if tracker1 ==1:
    return False
  else:
    return True

def make_cs_list(mod_list):
  list = []
  l=len(mod_list)
  if l==1:
      list= list + [[[0,mod_list[0]]]]
  else:
    m = mod_list[0]
    del mod_list[0]
    for c in make_cs_list(mod_list):
      for j in range(0,m):
        d = c + [[j,m]]
        list = list + [d]
  return list


def check_if_minimal(covsys):
  T = 0
  for k in range(0,len(covsys)):
    tempcs = covsys.copy()
    del tempcs[k]
    if check_if_cs(tempcs) == True:
        T = 1
  if T == 0:
    return True
  else:
    return False






PotentialModLists = []

for L in LCMlist_6:
  for k in range(5,7):
    for modlist in findsubsets(right_div(L), k):
      recipsum=0
      for i in range(0,len(modlist)):
        recipsum=recipsum+(1/modlist[i])
      if recipsum >= 1:
        PotentialModLists = PotentialModLists + [modlist]

PotentialModLists = set(PotentialModLists)

PotentialModLists = [list(modlist) for modlist in PotentialModLists]

print(len(PotentialModLists))





total_cs_list = []
for modlist in PotentialModLists:
  for sys in make_cs_list(modlist):
    if check_if_cs(sys) == True and check_if_minimal(sys):
      total_cs_list = total_cs_list + [sys]



for i in range(0, len(total_cs_list)):
  print(total_cs_list[i])




