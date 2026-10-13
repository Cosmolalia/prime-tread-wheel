"""Sparse, exact one-hot phase MILP for the Prime Tread Wheel J1c object A.
Each prime p has one phase c in [0,p-1]. A chosen phase covers tick k
iff (T(m-1)+k) % p == c. Minimize nonzero phases, optionally fix ring 2.
This builds O(m*pi(B)+sum(p)) sparse matrix entries, not a dense matrix.
Requires numpy, scipy. No repo dependency. Designed for independent audits.
"""
import sys, math, time
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import coo_matrix

def primes_to(n):
    a=bytearray(b'\x01')*(n+1); a[:2]=b'\x00\x00'
    for p in range(2,math.isqrt(n)+1):
        if a[p]: a[p*p::p]=b'\x00'*((n-p*p)//p+1)
    return [i for i in range(n+1) if a[i]]

def solve(m, ring2=None, time_limit=25.0):
    T=m*(m-1)//2; B=math.isqrt(T)
    primes=primes_to(B)
    offsets=[]; nvar=0
    for p in primes:
        offsets.append(nvar); nvar+=p
    nrows=len(primes)+m
    row=[]; col=[]
    for i,p in enumerate(primes):
        base=offsets[i]
        for r in range(p):
            row.append(i); col.append(base+r)
        for k in range(1,m+1):
            row.append(len(primes)+k-1)
            col.append(base+(T+k)%p)
    A=coo_matrix((np.ones(len(row),dtype=np.float64), (row,col)),shape=(nrows,nvar)).tocsr()
    lo=np.empty(nrows); hi=np.empty(nrows)
    lo[:len(primes)]=1;hi[:len(primes)]=1
    lo[len(primes):]=1;hi[len(primes):]=np.inf
    c=np.ones(nvar)
    for base in offsets: c[base]=0
    lb=np.zeros(nvar); ub=np.ones(nvar)
    if ring2 is not None:
        assert primes[0]==2
        if ring2=='home': lb[0]=ub[0]=1; lb[1]=ub[1]=0
        elif ring2=='flipped': lb[0]=ub[0]=0; lb[1]=ub[1]=1
        else: raise ValueError(ring2)
    st=time.perf_counter()
    result=milp(c=c, integrality=np.ones(nvar),bounds=Bounds(lb,ub),
                constraints=LinearConstraint(A,lo,hi),
                options={'time_limit':time_limit,'mip_rel_gap':0.0})
    elapsed=time.perf_counter()-st
    summary={'m':m,'rings':len(primes),'vars':nvar,'nnz':A.nnz,'seconds':round(elapsed,2),
             'mode':ring2 or 'free','status':int(result.status),'message':result.message,
             'objective':None if result.fun is None else result.fun,
             'best_bound':getattr(result,'mip_dual_bound',None),'gap':getattr(result,'mip_gap',None)}
    if result.x is not None:
        chosen=[int(np.argmax(result.x[base:base+p])) for p,base in zip(primes,offsets)]
        summary['phase2']=chosen[0]
        summary['displacements']=sum(v!=0 for v in chosen)
        uncovered=[k for k in range(1,m+1) if not any((T+k)%p==phase for p,phase in zip(primes,chosen))]
        summary['uncovered']=len(uncovered)
    return summary

if __name__=='__main__':
    import json
    m=int(sys.argv[1]) if len(sys.argv)>1 else 263
    limit=float(sys.argv[2]) if len(sys.argv)>2 else 25
    mode_arg=sys.argv[3] if len(sys.argv)>3 else 'free'
    modes=(None,'home','flipped') if mode_arg=='all' else (None if mode_arg=='free' else mode_arg,)
    for mode in modes:
        print(json.dumps(solve(m,mode,limit),default=str),flush=True)
