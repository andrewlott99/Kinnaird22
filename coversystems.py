import itertools
import numpy as np
import math
from sympy import factorint
from math import factorial as fact







LCMlist_6 = [12,18,24]

LCMlist_7 = [36,48]

LCMlist_8 = [30, 54, 72, 96]

LCMlist_10 = [90,120,156,162,288,384]


def makegrid(d,n):
    Grid = []
    if d==1:
        for i in range(1,n+1):
            Grid=Grid + [[i]]
    else: 
        for q in makegrid(d-1,n):
            for i in range(1,n+1):
               p = q + [i]
               Grid = Grid + [p]
    return Grid


def remove_residues(arr,d,r):

  for k in arr:
    if k%d == r:
      arr.remove(k)


def right_div(n):
  div_arr = []
  for i in range(2,math.floor(n/2)+1):
    if n % i == 0:
      div_arr=div_arr+[i]
  div_arr=div_arr+[n]
  return div_arr


def first_n_integers(n):
  arr = []
  for i in range(1,n+1):
    arr = arr + [i]

  return arr


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

def get_listlcm(list):
  if len(list)==1:
    return list[0]
  num1 = list[0]
  num2 = list[1]
  lcm = find_lcm(num1, num2)

  for i in range(2, len(list)):
    lcm = find_lcm(lcm, list[i])

  return lcm

def RemoveResidues(m, d, r):
  residues = []
  for k in range(0, m): 
    if k % d != r:
      residues = residues + [[k,m]]
  return(residues)
print(RemoveResidues(27,3,2))

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


def make_cs_shortlist(mod_list):
  lst = []
  mod_list.sort(reverse = True)
  l=len(mod_list)


  if l==1:
    lst= lst + [[[0,mod_list[0]]]]
  else:
    m = mod_list[0]
    del mod_list[0]
    for c in make_cs_shortlist(mod_list):
      relevantresidues = []
      for x in range(0, m):
        relevantresidues = relevantresidues + [x]
      for w in c:
        if m%w[1] == 0:
          remove_residues(relevantresidues, w[1], w[0])
      for z in relevantresidues:
        u = c+[[z,m]]
        lst = lst + [u]
  return lst


lstt =  make_cs_shortlist([3,4,12])

print(lstt)

lst = lstt.copy()

for sys in lst:
  m = sys[len(sys)-1][0] 
  for e in sys:
    e[0]=(e[0]-m)%e[1]

print(lst)


'''mod_list = [3,4,12]

mod_list2 = mod_list.copy()


print(make_cs_shortlist(mod_list))

print(make_cs_shortlist_zeroed(mod_list2))'''


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

def prepartition(S,k):
  allparts = []
  r = len(S)
  if r == 1:
    for i in range(0,k):
      allparts = allparts + [[[S[0],i]]]
  else: 
    tempS = S.copy()
    del tempS[r-1]
    for part in prepartition(tempS, k):
        for i in range(0,k):
          newpart = []
          newpart = part + [[S[r-1], i]]
          allparts = allparts + [newpart]
  return allparts

def fullpartition(S,k):
  allparts = []
  key = prepartition(S,k)
  for prepart in key:  
    tracker = 0
    part = []  
    for l in range(0,k):
      D = []
      for mod in prepart:
        if mod[1] == l:
          D = D+[mod[0]]
      if len(D)==0:
          tracker = 1
      part = part + [D]
    if tracker == 0:

      allparts = allparts + [part]

  return allparts

def check_if_bad(moduli_list):
  recipsum=0
  for m in moduli_list:
    recipsum=recipsum+(1/m)
  if recipsum < 1:
    return "Bad"
  L = get_listlcm(moduli_list)
  P = factorint(L)
  s = len(P)

  if s == 1: 
    return "Don't know"

  for i in range(0,s):
    tally = 0 
    p = list(P)[i]
    a = list(P.values())[i]
    j = a
    while j>0:
      count = 0
      for m in moduli_list:
        if m % (p**j) == 0 and m % (p**(j+1)) != 0:
          count = count +1
      tally = tally + (p**(a-j))*count

      if tally < p**(a-j+1): 
        for m in moduli_list:
          if m % (p**j) == 0:
            moduli_list.remove(m)
        return check_if_bad(moduli_list)
      j = j-1
    
  for i in range(0,s):
    M_0 = []
    M_1 = []
    p = list(P)[i]
    for m in moduli_list:
      if m % p != 0:
        M_0 = M_0 + [m]
      else: 
        M_1 = M_1 + [m]

    D = fullpartition(M_1, p)

    good_partition_found = 1
    for partition in D: 
      currentcheck = 0
      for w in range(0,p):
        newmods = M_0.copy()
        for y in partition[w]:
          newmods = newmods + [int(y/p)]
        if check_if_bad(newmods) == "Bad":
          currentcheck = 1
      if currentcheck == 0:
        good_partition_found = 0
    if good_partition_found == 1:
      return "Bad"
    else: return "Don't know"

PotentialModLists = []

<<<<<<< Updated upstream
for L in LCMlist_10:
=======
for L in LCMlist_8:
>>>>>>> Stashed changes
  for k in range(8,9):
    for modlist in findsubsets(right_div(L), k):
        PotentialModLists = PotentialModLists + [modlist]

PotentialModLists = set(PotentialModLists)

PotentialModLists = [list(modlist) for modlist in PotentialModLists]

count = 0
FinalModLists = []

for modlist in PotentialModLists:
  solidmodlist = modlist.copy()
  if check_if_bad(modlist) == "Don't know":
    FinalModLists = FinalModLists + [solidmodlist]

print(FinalModLists)

for candidate in FinalModLists:
  for sys in make_cs_shortlist(candidate):
    if check_if_cs(sys) == True and check_if_minimal(sys)==True:
      print(sys)







