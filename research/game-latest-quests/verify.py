#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Rebuild the pinned PR1169 baseline and certify optional619 inventory quests.
Prepared for hexapode with substantial OpenAI Codex assistance.
No optimizer, network request, discovery mode, or existing replay is consumed.
"""
import argparse,gzip,hashlib,json,os,subprocess,sys,time
from fractions import Fraction
from pathlib import Path
HERE=Path(__file__).resolve().parent
def need(ok,message):
    if not ok:raise ValueError(message)
def read(p):return json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def main():
    need(not sys.flags.optimize,'Assertions must remain enabled')
    need(sys.version_info>=(3,13),'Python3.13+ required for unchanged upstream gzip receipt serialization')
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--work',type=Path,required=True);a=ap.parse_args()
    work=a.work.resolve();need(not work.exists() and not work.is_relative_to(HERE),'Use a fresh external work directory')
    for rel,digest in read(HERE/'MANIFEST.json').items():need(sha(HERE/rel)==digest,'Source drift: '+rel)
    baseline=HERE/'vendor/pr1169';root=HERE;source=None
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1',PYTHONINTMAXSTRDIGITS='0',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
    for k in ('PYTHONOPTIMIZE','WITNESS_DISCOVER','WITNESS_RECORD','WITNESS_SPEC','XPARAM','EXTRAH','PAIRING_RANKS','DIAG','HYBBUDGET','PR635_CODE','SW4_PIN','LEC_REASON_PINS'):env.pop(k,None)
    work.mkdir(parents=True);stages=[]
    def run(name,script,*args,portable=False,environment=None):
        cmd=[sys.executable,'-B']+([str(source/'code/run_portable.py')]if portable else[])+[str(script),*map(str,args)]
        start=time.monotonic();log=work/(name+'.log')
        with log.open('w')as f:r=subprocess.run(cmd,cwd=root,env=environment or env,stdout=f,stderr=subprocess.STDOUT)
        stages.append(dict(name=name,command=cmd,script_sha256=sha(script),exit_code=r.returncode,seconds=time.monotonic()-start,log_sha256=sha(log)));dump(work/'STAGES.json',stages)
        need(r.returncode==0,name+' failed: '+str(log)+'\n'+log.read_text()[-3000:]);print('PASS',name,flush=True)
    expected=read(HERE/'EXPECTED.json');generated=work/'construction'
    run('construct',HERE/'construct.py','--baseline',baseline,'--out',generated)
    for name,digest in expected['generated_sha256'].items():need(sha(generated/name)==digest,'Frozen construction differs: '+name)
    baselinework=work/'baseline'
    run('baseline',baseline/'verify.py','--work',baselinework)
    br=read(baselinework/'RESULT.json');need(br['status']=='PASS_T37_JOINT_ENTRANCES_NATIVE_AND_STRICT_ADMISSION' and Fraction(br['kappa'])==Fraction(expected['baseline_kappa']),'Complete pinned baseline admission')
    root=baselinework/'layout/joint1148-round45/source';source=root/'research/complex-k492-owner-repair/vendor/multicold'
    old=source/'vendor/pr558/vendor/pr552';code=baselinework/'layout/owner37-round44/source/research/r480-owner-optimum/code'
    env.update(MULTICOLD_SOURCE=str(source),GAIN_PR564_SOURCE=str(source))
    natives=work/'native';natives.mkdir();(natives/'0').symlink_to(baselinework/'native',target_is_directory=True)
    need(set(read(generated/'DISPATCH.json').values())=={0,2},'Frozen mixed provider set')
    run('native-2',root/'research/k8-eight-ends/replay_native.py',generated/'FULL-WORD-2.json.gz',natives/'2')
    run('independent-local-2',root/'research/gauge44-slots/independent/audit_local.py','--word',generated/'FULL-WORD-2.json.gz','--main',root,'--output',work/'AUDIT-LOCAL-2.json')
    run('local-controls',HERE/'controls.py','--construction',generated,'--out',work/'local-controls','--source',root)
    need(len(read(work/'local-controls/RESULT.json')['rejected'])==3,'All three changed-word controls')
    for b in (0,2):
        need(gzip.decompress((natives/str(b)/'local/FULL-WORD.json.gz').read_bytes())==gzip.decompress((generated/f'FULL-WORD-{b}.json.gz').read_bytes()),'Exact generated native provider')
        steps=read(natives/str(b)/'STEPS.json');need([x['step']for x in steps]==['native','ledgers','local-replay','wrappers','phases'] and all(x['exit_code']==0 for x in steps),'Complete native pipeline')
    glob=work/'global';mixed=dict(env,WITNESS_SPEC=str(HERE/'data/SPEC.json'))
    def g(name,script,*args):run(name,code/script,*args,portable=True,environment=mixed)
    g('bind','bind_providers_portable.py','--baseline',baselinework/'strict/parent','--provider','gauge44='+str(natives/'0/local'),'--provider','quest2='+str(natives/'2/local'),'--plan',HERE/'data/PLAN.json','--out',glob)
    g('emit','emit_allcold.py','--base',glob/'base','--owners',generated/'OWNERS.json.gz','--plan',glob/'PLAN.json','--out',glob/'hosted')
    g('audit','audit_allcold.py',glob/'base',glob/'hosted',glob/'audit/ASYNC-AUDIT.json','--mutation-controls')
    g('invoice','invoice_allcold.py','--base',glob/'base','--hosted',glob/'hosted','--audit',glob/'audit','--out',glob/'audit','--retained-invoice',old/'complex-global/vendor531/evidence/audit/PREFIX-AND-INVOICE.json')
    g('assembly','assemble.py',source,glob,work/'ASSEMBLY.json')
    for label,script in [('ADMISSION-CONTROLS','assembly_controls.py'),('BIT-CONTROLS','bit_supplier_controls.py')]:g(label,script,'--source-package',source,'--owner',glob/'audit/OWNERS-AND-PROFILE.json','--invoice',glob/'audit/PREFIX-AND-INVOICE.json','--out',work/(label+'.json'))
    run('independent',HERE/'independent.py','--candidate',generated,'--native',natives,'--parent',baselinework/'layout/demotions1148-round43/baseline-replay/parent/t16/global8/base/split-centres/GLOBAL-TEMPLATE.json.gz','--baseline',baseline,'--out',work/'INDEPENDENT.json')
    result=read(work/'ASSEMBLY.json');ind=read(work/'INDEPENDENT.json');audit=read(glob/'audit/ASYNC-AUDIT.json');invoice=read(glob/'audit/PREFIX-AND-INVOICE.json');owner=read(glob/'audit/OWNERS-AND-PROFILE.json')
    need(result['complex_profile']==ind['profile']==read(generated/'PROFILE.json'),'Independent complete profile')
    need(result['kappa']==expected['kappa'] and Fraction(result['kappa'])>Fraction(expected['baseline_kappa']),'Exact improving exponent')
    need(result['provider_counts']==expected['provider_counts'],'Complete provider dispatch')
    need(ind['rank_mass']==owner['rank_mass']==2408256,'Complete rank mass')
    need(ind['roles']==owner['hosted_residuals']==audit['complex_hosted_residuals']==159840,'Whole helper roles')
    need(ind['calls']==audit['complete_invocations']==invoice['complete_invocation_sweeps']==333,'Complete invocation inventory')
    need(ind['prefix_bits']==invoice['global_prefix_bits']==expected['prefix_bits'] and invoice['charged_prefix_bits']==1024,'Prefix invoice')
    need(ind['physical_row_coefficient']==invoice['finite']['physical_row_coefficient']==expected['physical_row_coefficient']<20161,'Physical row invoice')
    admission=read(work/'ADMISSION-CONTROLS.json');bit=read(work/'BIT-CONTROLS.json')
    controls=dict(admission=len(admission['rejected_controls']),bit=len(bit['rejected_controls']),controller=len(audit['mutations_rejected']),geometry=len(ind['controls_rejected']),dispatch=len(ind['mixed_controls_rejected']))
    need(controls==expected['controls'] and not admission['discovery_accepted_controls'],'All strict negative controls')
    need(ind['mixed_controls_rejected']==['substitute_baseline_widths_for_changed_call'],'Wrong provider rejected')
    need(ind['disjoint_pending_child_axis_checks']>0,'Disjoint pending child axes')
    need(all(invoice['strict_checks'].values()),'Finite invoice strict checks')
    need(len(result['outer'])==47 and all(Fraction(x)>0 for x in result['outer'].values()),'All47 strict outer inequalities')
    receipt=dict(status='PASS_FRESH_LATEST_T37_OPTIONAL619_COMPLETE_ADMISSION',kappa=result['kappa'],decimal=result['kappa_decimal'],baseline_kappa=expected['baseline_kappa'],delta=str(Fraction(result['kappa'])-Fraction(expected['baseline_kappa'])),controls=controls,groups=expected['groups'],roles=159840,calls=333,stages=stages,source_manifest_sha256=sha(HERE/'MANIFEST.json'),assembly_sha256=sha(work/'ASSEMBLY.json'),independent_sha256=sha(work/'INDEPENDENT.json'),scope='Fresh finite baseline local word and T37 admission (inherited parent geometry is explicitly reused), changed native scalar/frame/phase and mixed owner/controller/invoice/outer admission. All inherited all-size/compiler, realization, hosting, precision/tape, exact-recovery, analytic and bit H1-H5 assumptions remain conditional. No runtime claim.')
    dump(work/'RESULT.json',receipt);print(receipt['status'],receipt['decimal'],flush=True)
if __name__=='__main__':main()
