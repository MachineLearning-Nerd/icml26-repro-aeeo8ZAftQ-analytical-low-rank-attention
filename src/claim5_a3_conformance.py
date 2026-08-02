#!/usr/bin/env python3
"""Clean-room finite conformance of the three A3 linear-algebra components.
Pinned source: sections/03_method.tex, Theorem 2, Theorem 3, Lemma 4.
This is not a LLaMA perplexity reproduction.
"""
import argparse, csv, hashlib, json, platform, sys, time
from pathlib import Path
import numpy as np

def spd_sqrt(a):
    w,v=np.linalg.eigh(a)
    w=np.maximum(w,1e-10)
    return (v*np.sqrt(w))@v.T, (v*(1/np.sqrt(w)))@v.T

def tsvd(a,r):
    u,s,vt=np.linalg.svd(a,full_matrices=False)
    return (u[:,:r]*s[:r])@vt[:r]
def rel(a,b): return float(np.linalg.norm(a-b,'fro')**2/(np.linalg.norm(a,'fro')**2+1e-15))
def run(seed, d=12, r=4, nq=96, nk=80):
    g=np.random.default_rng(seed)
    # non-isotropic calibration makes activation-aware solution meaningfully distinct
    xq=g.normal(size=(nq,d)) @ np.diag(np.linspace(.25,2,d))
    xk=g.normal(size=(nk,d)) @ np.diag(np.linspace(2,.25,d))
    wqk=g.normal(size=(d,d))
    rq=xq.T@xq/nq; rk=xk.T@xk/nk
    sq,iq=spd_sqrt(rq); sk,ik=spd_sqrt(rk)
    qk_a=iq@tsvd(sq@wqk@sk,r)@ik
    qk_raw=tsvd(wqk,r)
    qk_a_err=rel(xq@wqk@xk.T,xq@qk_a@xk.T)
    qk_raw_err=rel(xq@wqk@xk.T,xq@qk_raw@xk.T)
    # per-head OV theorem: P autocorrelation weighted SVD
    p=g.normal(size=(nq,d))@np.diag(np.linspace(.2,2.4,d)); wov=g.normal(size=(d,d))
    sp,ip=spd_sqrt(p.T@p/nq)
    ov_a=ip@tsvd(sp@wov,r); ov_raw=tsvd(wov,r)
    ov_a_err=rel(p@wov,p@ov_a); ov_raw_err=rel(p@wov,p@ov_raw)
    # A3-MLP diagonal CUR-style channel keep: retain r highest weighted output-energy channels
    xdown=g.normal(size=(nq,d))@np.diag(np.linspace(.15,2.5,d)); wd=g.normal(size=(d,d))
    # Per-intermediate-channel retained output energy for diagonal CUR-style selection.
    scores=np.sum((xdown[:, :, None] * wd[None, :, :])**2,axis=(0,2))
    keep=np.argsort(scores)[-r:]; U=np.zeros((d,d));U[keep,keep]=1
    mlp=U@wd
    # destructive control selects lowest energies
    bad=np.argsort(scores)[:r]; Ub=np.zeros((d,d));Ub[bad,bad]=1
    mlp_bad=Ub@wd
    mlp_err=rel(xdown@wd,xdown@mlp); mlp_bad_err=rel(xdown@wd,xdown@mlp_bad)
    return dict(seed=seed,d=d,rank=r,qk_activation_aware_error=qk_a_err,qk_raw_svd_error=qk_raw_err,
                ov_activation_aware_error=ov_a_err,ov_raw_svd_error=ov_raw_err,
                mlp_cur_keep_error=mlp_err,mlp_low_energy_control_error=mlp_bad_err,
                qk_rank=int(np.linalg.matrix_rank(qk_a)),ov_rank=int(np.linalg.matrix_rank(ov_a)),mlp_channels=','.join(map(str,keep.tolist())))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--seeds',nargs='+',type=int,default=[11,23,47,89,131]);a=ap.parse_args()
 out=Path(a.out);out.mkdir(parents=True,exist_ok=True); start=time.time(); rows=[run(s) for s in a.seeds]
 fields=list(rows[0]);
 with (out/'results.csv').open('w',newline='') as f: w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
 summary={'method':'clean-room finite A3-QK/A3-OV activation-aware SVD and A3-MLP channel CUR-style conformance','source_location':'sections/03_method.tex Theorem 2, Theorem 3, Lemma 4','seeds':a.seeds,'mean_qk_activation_aware_error':float(np.mean([x['qk_activation_aware_error'] for x in rows])),'mean_qk_raw_svd_error':float(np.mean([x['qk_raw_svd_error'] for x in rows])),'mean_ov_activation_aware_error':float(np.mean([x['ov_activation_aware_error'] for x in rows])),'mean_ov_raw_svd_error':float(np.mean([x['ov_raw_svd_error'] for x in rows])),'mean_mlp_keep_error':float(np.mean([x['mlp_cur_keep_error'] for x in rows])),'mean_mlp_low_energy_error':float(np.mean([x['mlp_low_energy_control_error'] for x in rows])),'runtime_seconds':time.time()-start,'python':sys.version,'platform':platform.platform(),'verdict':'toy'}
 (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 (out/'config.json').write_text(json.dumps({'d':12,'rank':4,'qk_tokens':96,'kv_tokens':80,'seeds':a.seeds,'compute':'local CPU numpy'},indent=2)+'\n')
 (out/'run.log').write_text(' '.join(sys.argv)+'\nexit_code=0\n')
 for p in sorted(out.iterdir()):
  if p.name!='SHA256SUMS': print(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name)
if __name__=='__main__': main()
