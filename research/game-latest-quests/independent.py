"""Independent many-provider admission using a statically derived PR1129 many-provider geometry checker.
Apache-2.0; derived from the credited PR1042/1111 audit; OpenAI Codex assistance.
The checker imports no inventory-search or owner-constructor functions.
"""
import argparse,collections,importlib.util,json,os,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--candidate',type=Path,required=True);p.add_argument('--native',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--parent',type=Path,required=True);p.add_argument('--baseline',type=Path,required=True);a=p.parse_args()
C=a.candidate.resolve();N=a.native.resolve();base=N/'0/local'
parent=a.parent.resolve()
spec=json.loads((a.baseline.resolve()/'SPEC.json').read_text());result=json.loads((C/'RESULT.json').read_text())
os.environ['T16_EXPECTED_IDLE']=json.dumps(result['idle']);os.environ['T16_EXPECTED_WIDTHS']=json.dumps(spec['providers']['gauge44']['inventory'])
source=Path(__file__).with_name('geometry.py')
s=importlib.util.spec_from_file_location('inherited_geometry',source);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
m.EXPECTED_IDLE={int(k):v for k,v in result['idle'].items()};m.EXPECTED_WIDTHS={int(k):v for k,v in spec['providers']['gauge44']['inventory'].items()}
read,need=m.read,m.require
roles=read(C/'OWNERS.json.gz');dispatch={int(t):b for t,b in read(C/'DISPATCH.json').items()}
need(set(dispatch)==set(range(333)),'complete explicit dispatch')
need(set(dispatch.values())=={0,2},'baseline and optional619 provider')
word=read(base/'CANONICAL-WORD.json.gz');replay=read(base/'INDEPENDENT-LOCAL-REPLAY.json');canonical=read(parent.parent/'CANONICAL-WORD.json.gz');phasepath=parent.parent.parent/'work/complex-nine-native/DATA-PHASES.json'
need(replay['status']=='PASS_INDEPENDENT_LOCAL_SCALAR_FRAME_AND_WRAPPER_REPLAY','baseline native status')
need(set(replay['local'])=={'forward','backward'},'baseline both native orientations')
need(word['ports']==canonical['ports'],'baseline/controller ports')
need(len(word['center_frames'])==len(canonical['center_frames'])==8,'eight centre interfaces')
need([m.basis(word['frames'][f])for f in word['center_frames']]==[m.basis(canonical['frames'][f])for f in canonical['center_frames']],'baseline ordered centre interface')
need(replay['canonical_word_sha256']==m.filehash(base/'CANONICAL-WORD.json.gz'),'baseline native hash')
context=m.make_context(read(parent),read(phasepath),canonical['ports'],word,replay,roles)
planpath=a.baseline.resolve()/'PLAN.json'
need(context['order']==[tuple(x)for x in read(planpath)['order']],'pinned T37 call order')
groups=((),(619,621,622,623))
widths={0:context['widths']};paid={0:context['paid']};replays={0:replay};pins={str(source):m.filehash(source)}
for bits in sorted(set(dispatch.values())-{0}):
 local=N/str(bits)/'local';wp=local/'CANONICAL-WORD.json.gz';rp=local/'INDEPENDENT-LOCAL-REPLAY.json';w,r=read(wp),read(rp)
 need(r['status']=='PASS_INDEPENDENT_LOCAL_SCALAR_FRAME_AND_WRAPPER_REPLAY','provider native status')
 need(r['canonical_word_sha256']==m.filehash(wp),'provider native hash')
 need(set(r['local'])=={'forward','backward'},'both native orientations')
 need((w['v'],w['h'],w['R'],w['ports'])==(word['v'],word['h'],word['R'],word['ports']),'provider dimensions/ports')
 need([m.basis(w['frames'][f])for f in w['center_frames']]==[m.basis(word['frames'][f])for f in word['center_frames']],'ordered centre interface')
 expected=list(widths[0])
 for j,group in enumerate(groups):
  if bits>>j&1:
   for h in group:need(expected[h-224]==4,'original demotion width');expected[h-224]=5
 m.EXPECTED_WIDTHS=dict(collections.Counter(expected));widths[bits],paid[bits]=m.local_inventory(w,r)
 need(widths[bits]==expected,'only recipe helpers widen')
 want=collections.Counter(paid[0]);g=bits.bit_count()
 for k,v in {1:-8,2:8,3:4,4:-4}.items():want[k]+=g*v
 need(paid[bits]==want,'independently recounted exact local delta')
 replays[bits]=r;pins.update({str(wp):m.filehash(wp),str(rp):m.filehash(rp)})
context['per_call_widths']={call:widths[dispatch[t]] for t,call in enumerate(context['order'])}
context['per_call_paid']={call:paid[dispatch[t]] for t,call in enumerate(context['order'])}
context['provider_replays']=list(replays.values());context['provider_paid']=list(paid.values());context['provider_widths']=list(widths.values())
pending=m.check_pending_axes(context)
receipt=m.check_roles(context,roles);receipt['disjoint_pending_child_axis_checks']=pending;receipt['controls_rejected']=m.controls(context,roles)
need({str(k):v for k,v in receipt['profile'].items()}==read(C/'PROFILE.json'),'independent fullprofile')
# Additional mixed-dispatch corruption: replace one widened provider with baseline widths.
t=next(t for t,b in dispatch.items()if b);bad=dict(context);bad['per_call_widths']=dict(context['per_call_widths']);bad['per_call_widths'][context['order'][t]]=widths[0]
try:m.check_roles(bad,roles)
except ValueError as e:need(str(e)=='whole-helper residual width','dispatch control predicate')
else:raise ValueError('wrong provider dispatch accepted')
receipt['mixed_controls_rejected']=['substitute_baseline_widths_for_changed_call']
receipt['dispatch_counts']=dict(collections.Counter(dispatch.values()))
for f in [planpath,parent,parent.parent/'CANONICAL-WORD.json.gz',phasepath,base/'CANONICAL-WORD.json.gz',base/'INDEPENDENT-LOCAL-REPLAY.json',C/'OWNERS.json.gz',C/'DISPATCH.json',Path(__file__)]:pins[str(f)]=m.filehash(f)
receipt['input_sha256']=pins;a.out.write_text(json.dumps(receipt,indent=2)+'\n');print(receipt['status'],receipt['roles'],receipt['calls'])
