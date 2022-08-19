import itertools
import numpy as np
import math
from sympy import factorint
from math import factorial as fact


"input n, 5<=n<=10" 
"returns all delta primitive covering systems up to affine equivalence, cardinality at most n"
n = 9


'returns [0,n]x...[0,n], d dimensions. Used in getLCMlist_5through10'
def makegrid(d,n):
    Grid = []
    if d==1:
        for i in range(0,n+1):
            Grid=Grid + [[i]]
    else: 
        for q in makegrid(d-1,n):
            for i in range(0,n+1):
               p = q + [i]
               Grid = Grid + [p]
    return Grid


'makes minimal version of L, used in getLCMlist_5through10'
def Remove_Div(L):

  Q = L.copy()
  for a in Q:
    for i in L:
      if i != a and a%i == 0:
        L.remove(i)
  M = L.copy()
  for i in M:
    P = factorint(i)
    if len(P) == 1:
      L.remove(i)

"creates list of LCMs which satisfy proposition 2.12"
def getLCMlist_5through10(n):
  LCMlist = []
  for p in makegrid(4,10):
    s = p[0]+(2*p[1])+(4*p[2])+(6*p[3])

    if s <= (n-1):
      L = (2**p[0])*(3**p[1])*(5**p[2])*(7**p[3])
      LCMlist = LCMlist + [L]


  return LCMlist


'returns units mod n, excluding 1'
def getunits(n):
  units = []
  for i in range(2,n):
    if math.gcd(i,n) ==  1:
      units = units + [i]

  return units 


'creates dictionary which gives units of each LCM in the LCM list'
UnitDictionary = {}

for i in getLCMlist_5through10(n):
  UnitDictionary[i] = getunits(i)


"returns all divisors of n, excluding 1. Used while creating initial list of lists of moduli"
def get_div(n):
  div_arr = []
  for i in range(2,math.floor(n/2)+1):
    if n % i == 0:
      div_arr=div_arr+[i]
  div_arr=div_arr+[n]
  return div_arr


"returns all subsets of s of size n"
def findsubsets(s, n):
    return list(itertools.combinations(s, n))

"returns lcm of num1,num2"
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

"returns lcm of the moduli of a congruence system"
def get_modlcm(system):
  num1 = system[0][1]
  num2 = system[1][1]
  lcm = find_lcm(num1, num2)

  for i in range(2, len(system)):
    lcm = find_lcm(lcm, system[i][1])

  return lcm

"returns lcm of a list"
def get_listlcm(list):
  if len(list)==1:
    return list[0]
  num1 = list[0]
  num2 = list[1]
  lcm = find_lcm(num1, num2)

  for i in range(2, len(list)):
    lcm = find_lcm(lcm, list[i])

  return lcm



"Recursively constructs list of systems from a mod list. All resulting systems have the"
"property that any one of its congruence class is not entirely contained in another"
"each affine equivalence class is represented at least once"

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

      for k in range(0,m):
        tracker = 0
        for i in c:
          if (m%i[1]==0) and (k%i[1] == i[0]):
            tracker = 1
        if (tracker == 0) and (k not in relevantresidues):
          relevantresidues = relevantresidues + [k]
      for z in relevantresidues:
        u = c+[[z,m]]
        lst = lst + [u]

  newlst = []
  
  for sys in lst:
    l = sys[len(sys)-1][0] 
    newsys = []
    for e in sys:
      r = (e[0]-l)%e[1]
      mod = e[1]
      newsys = newsys + [[r,mod]]
    newlst = newlst + [newsys]

    

  newlst.sort()
      
  newnewlst = list(newlst for newlst,_ in itertools.groupby(newlst))
      
  return newnewlst



"used in fullpartition"
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

"returns all ways to place the elements of S into 1 of k lists, where each of the k lists contains at least one element of S. "
"part of the Jenk-Simpson algorithm, check_if_bad"
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


"Jenkin-Simpson algorithm. Returns bad if it detects that a list moduli cannot result in a covering system, otherwise returns dont know"
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



"returns true if system covers Z, false otherwise"
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



"returns true if covsys is minimal, false otherwise"
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

"removes covering systems which are not delta-primitive"
def FindDeltaPrimitives(SystemList):
  TempList = SystemList.copy()
  for cs in TempList:
    if cs[0] == [1,2]:
      tracker = 0
      for i in range(1,len(cs)-1):
        if cs[i][0]%2 == 1 or cs[i][1]%2 == 1:
          tracker = 1
      if tracker == 0:
        SystemList.remove(cs)


"makes list of systems unique up to translation"
def RemoveTranslationalDuplicates(SystemList):
  InitialList = SystemList.copy()
  for cs in InitialList:
    L = get_modlcm(cs)
    M = cs[len(cs)-1][1]
    W = int(L/M)
    for i in range(1,W):
      newcs = []
      for e in cs:
        r = (e[0]+(M*i))%e[1]
        mod = e[1]
        newcs = newcs + [[r,mod]]
      if (newcs in SystemList):
        if (InitialList.index(newcs)>InitialList.index(cs)):
          SystemList.remove(newcs)

"removes duplicates up to unit multiplication"
def RemoveDuplicatesUpToUnitMultiplication(cslist):
  initialcslist = cslist.copy()
  for cs in initialcslist:
    L = get_modlcm(cs)
    for u in UnitDictionary[L]:
      altcs = []
      for i in range(0,len(cs)):
        r = (u*cs[i][0])%(cs[i][1])
        mod = cs[i][1]
        altcs = altcs + [[r,mod]]
      if altcs in cslist:
        if initialcslist.index(altcs)>initialcslist.index(cs):
          cslist.remove(altcs)


"359-373 creates list of modlists cardinality at least 5 at most 10"

LCMlist = getLCMlist_5through10(n)
fullLCMlist =LCMlist.copy()
Remove_Div(LCMlist)


PotentialModLists = []

for L in LCMlist:
  for k in range(5,n+1):
    for modlist in findsubsets(get_div(L), k):
        PotentialModLists = PotentialModLists + [list(modlist)]

PotentialModLists.sort()

newPotentialModLists = list(PotentialModLists for PotentialModLists,_ in itertools.groupby(PotentialModLists))




"reduces list of modlists via Jenkin-Simpson"
FinalModLists = []

for modlist in newPotentialModLists:
  solidmodlist = modlist.copy()
  if check_if_bad(modlist) == "Don't know":
    FinalModLists = FinalModLists + [solidmodlist]

FinalSystemList = []

good_mod_list = []


"finds all minimal covering systems for each candidate modlists, includes affine duplicates and non delta primitives."
for candidate in FinalModLists:
  candidatecopy = candidate.copy()
  candidatelist = make_cs_shortlist(candidate)
  count = 0
  for sys in candidatelist:
    if check_if_cs(sys) == True and check_if_minimal(sys)==True:
      FinalSystemList = FinalSystemList + [sys]


"filters for affine equivalence, all survivors are delta primitive"
FindDeltaPrimitives(FinalSystemList)
RemoveTranslationalDuplicates(FinalSystemList)
RemoveDuplicatesUpToUnitMultiplication(FinalSystemList)


"result"
for cs in FinalSystemList:
  print(cs)

print(len(FinalSystemList))

      



