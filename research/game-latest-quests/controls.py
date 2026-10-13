#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Three destructive controls against the unchanged independent local auditor."""
import argparse,copy,gzip,hashlib,json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
def read(p):return json.loads(gzip.decompress(p.read_bytes()))
def main():
    if sys.flags.optimize:raise ValueError('Assertions must remain enabled')
    p=argparse.ArgumentParser();p.add_argument('--construction',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--source',type=Path,required=True);a=p.parse_args()
    root=a.source.resolve();honest=read(a.construction/'FULL-WORD-2.json.gz');base=read(a.construction/'FULL-WORD-0.json.gz');a.out.mkdir(parents=True,exist_ok=False);rows=[]
    for name in ('undo_one_entrance','false_profile','bad_scalar'):
        w=copy.deepcopy(honest)
        if name=='undo_one_entrance':w['start_extra']['619']=base['start_extra']['619']
        elif name=='false_profile':w['report']['local_profile']['2']+=1
        else:
            i=next(i for i,e in enumerate(w['B'])if e[0]=='add' and 112<=e[1]<224);w['B'][i][3]+=1
        path=a.out/(name+'.json.gz');path.write_bytes(gzip.compress(json.dumps(w,sort_keys=True,separators=(',',':')).encode(),mtime=0))
        cmd=[sys.executable,'-B',str(root/'research/gauge44-slots/independent/audit_local.py'),'--word',str(path),'--main',str(root),'--output',str(a.out/(name+'-AUDIT.json'))]
        log=a.out/(name+'.log')
        with log.open('w')as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
        text=log.read_text()
        predicate={'undo_one_entrance':'RuntimeError: frame not monotone','false_profile':'RuntimeError: paid profile mismatch','bad_scalar':'RuntimeError: nonzero entrance response'}[name]
        if r.returncode==0 or predicate not in text:raise ValueError('Control did not fail at its mathematical predicate: '+name)
        rows.append(dict(name=name,exit_code=r.returncode,log_sha256=hashlib.sha256(log.read_bytes()).hexdigest()))
    (a.out/'RESULT.json').write_text(json.dumps(dict(status='PASS_DESTRUCTIVE_LOCAL_CONTROLS',rejected=rows),indent=2)+'\n')
if __name__=='__main__':main()
