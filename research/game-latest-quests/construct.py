#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Reproduce the frozen PR1169 optional619 inventory quest without an optimizer.

The GF(2) span and chain recount are adapted from BlockInvert (Claude Code
research agent), gauge44 build_promotion.py (Apache-2.0). The retained slots
construction, PR1169 joint-entrance owner construction and demotion construction are credited in the
package NOTICE/README. Substantial implementation assistance: OpenAI Codex.
"""
import argparse
from collections import Counter, defaultdict
import copy
import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIELDS = ('owner_replica', 'child', 'port', 'copy', 'family', 'offset')

def need(value, message):
    if not value:
        raise ValueError(message)

def read(path):
    raw = path.read_bytes()
    return json.loads(gzip.decompress(raw) if path.suffix == '.gz' else raw)

def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()

def digest(value):
    return hashlib.sha256(encoded(value)).hexdigest()

def filehash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(path, value):
    raw = encoded(value)
    if path.suffix == '.gz':
        packed = bytearray(gzip.compress(raw, mtime=0))
        packed[9] = 255  # Normalize the platform-dependent gzip OS byte.
        path.write_bytes(packed)
    else:
        path.write_bytes(raw+b'\n')

def span(vs):
    p = {}
    for x in vs:
        for k in sorted(p, reverse=True):
            if x >> k & 1:
                x ^= p[k]
        if x:
            k = x.bit_length()-1
            for j in list(p):
                if p[j] >> k & 1:
                    p[j] ^= x
            p[k] = x
    return tuple(p[k] for k in sorted(p, reverse=True))

def registers(e):
    return [e[1]] + ([e[2]] if e[0] == 'add' else [])

def chains(word):
    v, R = word['report']['v'], word['report']['R']
    current = [()]*(2*v+R)
    for i, port in enumerate(word['ports']):
        current[i] = span([port])
    for q, frame in word['start_extra'].items():
        current[int(q)] = span(frame)
    paid = Counter()
    def climb(q, frame):
        need(span(current[q]+frame) == frame, 'nonmonotone frame chain')
        if len(frame)>len(current[q]):
            paid[len(frame)-len(current[q])] += 1
        current[q] = frame
    for section in ('A', 'B'):
        for e in word[section]:
            for q in registers(e):
                climb(q, span(e[-1]))
    for i, frame in word.get('early_cleanup', []):
        for q in registers(word['cleanup'][i]):
            climb(q, span(frame))
    full = span([1 << i for i in range(9)])
    for q in range(2*v+R):
        if v<=q<2*v:
            frame = span([x for x in range(1,512) if (x & word['ports'][q-v]).bit_count()%2==0])
        else:
            frame = span(word['helper_final'].get(str(q), full))
        climb(q, frame)
    return paid

def widths(word):
    full = [1 << i for i in range(9)]
    return [len(span(word['helper_final'].get(str(q),full)))-len(span(word['start_extra'].get(str(q),[])))
            for q in range(224,224+word['report']['R'])]

def words(base, recipes):
    result = {0:base}
    original_chains = chains(base)
    for bit, recipe in recipes.items():
        b = int(bit)
        word = copy.deepcopy(base)
        for q, before, after in recipe['entrances']:
            need(word['start_extra'][str(q)] == before, 'entrance recipe source')
            need(len(span(before)) == len(span(after))+1 and span(before+after)==span(before), 'one-rank entrance demotion')
            word['start_extra'][str(q)] = after
        for section, i, before, after in recipe['frames']:
            need(section=='B' and word[section][i][-1]==before, 'frame recipe source')
            word[section][i][-1] = after
        for section in ('precondition','A','cut','B','cleanup'):
            need([e[:-1] for e in word[section]]==[e[:-1] for e in base[section]], 'retained scalar program')
        paid = Counter({int(k):v for k,v in base['report']['local_profile'].items()})
        paid.subtract(original_chains)
        paid.update(chains(word))
        need(min(paid.values())>=0, 'nonnegative profile')
        paid = +paid
        word['report'].update(local_profile={str(k):v for k,v in sorted(paid.items())},
            local_rank_mass=sum(k*v for k,v in paid.items()),
            width_inventory={str(k):v for k,v in sorted(Counter(widths(word)).items())})
        need(digest(word)==recipe['expected_word_sha256'], 'frozen derived raw word')
        result[b]=word
    return result

def bank(role):
    return role['owner_replica'],role['child'],role['port']

def check(roles, original, plan, dispatch, wordset):
    N,T = len(plan['order']),plan['T']
    need(len(roles)==len(original)==N*480, 'complete role count')
    expected_widths={b:widths(w) for b,w in wordset.items()}
    seen=set();families=defaultdict(set);cells=defaultdict(set)
    for r,old in zip(roles,original):
        identity=(r['stage'],r['replica'],r['helper'])
        need(identity==(old['stage'],old['replica'],old['helper']) and identity not in seen, 'whole role identity')
        seen.add(identity);t=r['time'];need(t==old['time'] and plan['order'][t]==[r['stage'],r['replica']], 'call order')
        need(r['width']==expected_widths[dispatch[t]][r['helper']], 'whole helper width')
        o,c,p=bank(r);need(0<=o<T and 0<=p<112, 'owner coordinates')
        cap,times=plan['windows'][f'{o},{c}'];need(t in times, 'idle window')
        family=o*896+(2*plan['pairs'][str(c)]+plan['sides'][str(c)])*112+p
        need(r['family']==family and r['copy']==112*o+p and family not in families[t], 'family or copy')
        families[t].add(family);lo=r['offset'];hi=lo+r['width'];need(0<=lo<hi<=cap, 'owner capacity')
        occupied=set(range(lo,hi));need(not cells[o,c,p]&occupied, 'owner overlap');cells[o,c,p]|=occupied
    need(len(families)==N and all(len(fs)==480 for fs in families.values()), 'complete invocations')
    idle=Counter()
    for key,(cap,_) in plan['windows'].items():
        o,c=map(int,key.split(','))
        for p in range(112):
            cell=cells[o,c,p];need(cell==set(range(len(cell))), 'gap in prefix')
            if len(cell)<cap:idle[cap-len(cell)]+=1
    return idle

def neutral(original, plan, moves):
    roles=[dict(r) for r in original];families=defaultdict(set)
    for r in roles:families[r['time']].add(r['family'])
    for i,j in moves:
        a,b=roles[i],roles[j];t,u=a['time'],b['time'];fa,fb=a['family'],b['family']
        need(t!=u and a['width']==b['width']==4, 'neutral whole equal-width exchange')
        need(fa!=fb and fb not in families[t] and fa not in families[u], 'neutral family collision')
        need(t in plan['windows'][f"{b['owner_replica']},{b['child']}"][1] and u in plan['windows'][f"{a['owner_replica']},{a['child']}"][1], 'neutral literal windows')
        for f in FIELDS:a[f],b[f]=b[f],a[f]
        families[t].remove(fa);families[t].add(fb);families[u].remove(fb);families[u].add(fa)
    return roles

def mixed(roles, plan, moves, recipes):
    original=roles;roles=[dict(r) for r in original];dispatch={t:0 for t in range(len(plan['order']))}
    used=Counter()
    for r in original:used[bank(r)]+=r['width']
    rem={b:plan['windows'][f'{b[0]},{b[1]}'][0]-v for b,v in used.items()}
    times=set()
    for move in moves:
        t,b=move['time'],move['bits'];need(t not in times and str(b) in recipes,'distinct recipe dispatch');times.add(t);dispatch[t]=b
        perm={int(k):v for k,v in move['permutation'].items()};need(set(perm)==set(perm.values()),'within-call bijection')
        for i,j in perm.items():
            need(original[i]['time']==original[j]['time']==t and original[i]['width']==original[j]['width']==4,'within-call whole-helper permutation')
            for f in FIELDS:roles[i][f]=original[j][f]
        selected=move['widened'];helpers={h-224 for h,_,_ in recipes[str(b)]['entrances']}
        need(len(selected)==len(set(selected))==len(helpers) and {roles[i]['helper'] for i in selected}==helpers,'complete recipe helpers')
        need(all(roles[i]['time']==t and i in perm for i in selected),'widened call identities')
        for i in selected:
            need(roles[i]['width']==4 and rem[bank(roles[i])]==1,'literal unit gap')
            roles[i]['width']=5;rem[bank(roles[i])]-=1
    bins=defaultdict(list)
    for i,r in enumerate(roles):bins[bank(r)].append(i)
    for b,ids in bins.items():
        offset=0
        for i in sorted(ids,key=lambda i:(roles[i]['time'],roles[i]['helper'])):
            roles[i]['offset']=offset;offset+=roles[i]['width']
        need(offset<=plan['windows'][f'{b[0]},{b[1]}'][0],'repacked capacity')
    return roles,dispatch

def main(baseline, out):
    need(__debug__, 'normal Python required')
    need(not out.exists(), 'fresh output required')
    pins=read(HERE/'inputs/PINS.json')
    for name,sha in pins['files'].items():need(filehash(HERE/name)==sha,'package input hash: '+name)
    for name,sha in pins['baseline_files'].items():need(filehash(baseline/name)==sha,'baseline source hash: '+name)
    base=read(HERE/'inputs/BASE-WORD.json.gz');need(hashlib.sha256(gzip.decompress((HERE/'inputs/BASE-WORD.json.gz').read_bytes())).hexdigest()==pins['base_word_content_sha256'],'raw source hash')
    recipes=read(HERE/'data/DEMOTION-RECIPES.json');wordset=words(base,recipes);plan=read(baseline/'PLAN.json');original=read(baseline/'OWNERS.json.gz');N=len(plan['order'])
    need(plan['T']==37 and N==333 and plan['live']==37*896,'pinned PR1169 T37 construction')
    need(widths(base)==plan['provider_registry']['gauge44']['widths'],'baseline width interface')
    need(base['report']['local_profile']==plan['provider_registry']['gauge44']['actual_paid_profile'],'baseline paid interface')
    idle0=check(original,original,plan,{t:0 for t in range(N)},wordset)
    moves=read(HERE/'data/NEUTRAL-MOVES.json.gz');need(len(moves)==38931,'frozen transcript length')
    routed=neutral(original,plan,moves);need(digest(routed)==pins['neutral_content_sha256'],'frozen neutral result')
    need(check(routed,original,plan,{t:0 for t in range(N)},wordset)==idle0,'neutral full recount')
    roles,dispatch=mixed(routed,plan,read(HERE/'data/MIXED-MOVES.json.gz'),recipes)
    idle=check(roles,original,plan,dispatch,wordset);profile=Counter(idle)
    for b in dispatch.values():profile.update({int(k):v for k,v in wordset[b]['report']['local_profile'].items()})
    need(sum(k*v for k,v in profile.items())==73*plan['live']-plan['deficit'],'complete rank mass')
    for name,value in [('OWNERS.json.gz',roles),('PROFILE.json',{str(k):v for k,v in profile.items()}),('DISPATCH.json',{str(k):v for k,v in dispatch.items()})]:
        need(value==read(HERE/'inputs/expected'/name),'decoded frozen candidate: '+name)
    controls=[]
    try:neutral(original,plan,[[moves[0][0],moves[0][0]]])
    except ValueError as e:need(str(e)=='neutral whole equal-width exchange','neutral control predicate');controls.append('self exchange')
    else:raise ValueError('self exchange accepted')
    for name,field,value in [('width','width',3),('family','family',-1),('offset','offset',999),('copy','copy',-1)]:
        bad=[dict(roles[0],**{field:value})]+roles[1:]
        try:check(bad,original,plan,dispatch,wordset)
        except ValueError:controls.append(name)
        else:raise ValueError('corruption accepted: '+name)
    out.mkdir(parents=True)
    for name,value in [('OWNERS.json.gz',roles),('PROFILE.json',dict(sorted(profile.items()))),('DISPATCH.json',dispatch)]:write(out/name,value)
    for b,w in wordset.items():
        if b==0:(out/'FULL-WORD-0.json.gz').write_bytes((HERE/'inputs/BASE-WORD.json.gz').read_bytes())
        else:write(out/f'FULL-WORD-{b}.json.gz',w)
    receipt=dict(status='PASS_FROZEN_OPTIONAL619_QUEST_CONSTRUCTION',roles=len(roles),calls=N,neutral_swaps=len(moves),groups=sum(b.bit_count() for b in dispatch.values()),dispatch_counts=dict(Counter(dispatch.values())),profile=dict(profile),global_profile=dict(profile),idle=dict(idle),changed_calls=sum(b!=0 for b in dispatch.values()),controls_rejected=controls,source_pins_sha256=filehash(HERE/'inputs/PINS.json'),constructor_sha256=filehash(Path(__file__)),outputs={p.name:filehash(p) for p in out.iterdir() if p.is_file()},scope='Deterministic generator and exact owner/frame accounting; full native/controller/phase/invoice/outer admission is performed by verify.py.')
    write(out/'CONSTRUCTED.json',receipt);write(out/'RESULT.json',receipt);print(receipt['status'],receipt['roles'],receipt['groups'])

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--baseline',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();main(a.baseline.resolve(),a.out.resolve())
