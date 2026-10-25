# Conditional kappa 0.00308534 from a three-stage P104 commuting-contact cascade

This construction increases complete conditional kappa from `0.00308189` in [PR #5580](https://github.com/CrocSwap/integer-mult-bounds/pull/5580) to **0.00308534** (`+3.45e-6`, raw crossing gain `+3.45044311e-6`). It also ships the fixed-endpoint supporting word `WORD-FIXED-ENDPOINTS.json.gz` reaching **0.00308415** (`+2.26058214e-6` raw over PR #5580) with all 735 `initial` and `final` frames and all 527 helper targets unchanged. The selected record remains `0.003027288235`.

PR #5561, PR #5569, PR #5580, and PR #5590 kept the linear execution order and instruction set of all 21,686 scalar operations fixed. By combining:
1. **Stage A:** commuting four independent `ADD` writes into port `198` (from `648, 649, 650, 652`) before `13528` to frame `3` (`0D`),
2. **Stage B:** commuting `13806` (`113 += 531`) before `13524` to frame `3` (`0D`) with `initial[531] = 3` and demoting `13846` (`197 += 319`) from `617` (`3D`) to `355` (`2D`), and
3. **Stage C:** commuting `345`'s uncompute `16920` (`345 += 4 * 712`) before `16654` (`341 += -345`) to 3-plane `739`, cancelling `16915` (`341 += 4 * 712`) by transitivity of `ADD`, and retiring helper `341` at 4-plane `240` (`final[341] = 240`),

this package eliminates six local `MOVE` transports and one redundant `ADD` per call (`-108` paid calls globally, `66,852 -> 66,744`) while preserving all 208 main endpoints, all 12,814 productive fields, rank-mass surplus `760`, and all eight owned lifetimes.

Read [the proof](PROOF.md), [the construction](construct.py), [the complete receipt](RESULT.json), [the source pins](SOURCES.json), and [the verification record](VALIDATION.md). The exact raw crossing of the headline word lies in `(0.00308534541177, 0.00308534541178)` and is tested at `0.0030853405`.

## Reproduction

Python 3.10+ and the standard library suffice. No external solver is needed to reconstruct or verify both published words:

```sh
python3 -B scripts/research_package.py --package research/p104-commuting-contact
```

Both registered modes print:

```text
PASS_P104_COMMUTING_CONTACT_KAPPA_00308534
```

and the launcher prints `PASS_REGISTERED_RESEARCH_PACKAGE`. It authenticates all 33 retained PR #5545 source payloads and the pinned PR #5580 inputs, regenerates both `WORD-FIXED-ENDPOINTS.json.gz` and `WORD.json.gz` from `construct.py`, runs forward arbitrary-input replay on the base, fixed-endpoint, and headline words, verifies all 552,049 dense transpose coefficients, checks all 2,918 signed native Pauli maps, runs the full physical caller, verifies both rational moment engines (`(0.00308415555080, 0.00308415555081)` for Stage A and `(0.00308534541177, 0.00308534541178)` for Stage A+B+C), and checks the compiler, all 58 outer predicates, and negative controls.

## Open next questions

- Can higher-order triangular or diamond uncompute chains (where a helper partner `p` is polluted by a 6D or 7D helper `q` that visits an 8D sub-chart prior to `127`) be commuted jointly across multiple helpers so that two or more `H9` helpers share a single `8D` split?
- Can the zero-contact spectator register `711` (`MOVE 711: 3 -> 626`, noted in PR #5590) or unused low-dimensional helper slots absorb a split uncompute chain without increasing the native map census?

## Credits

- Ali Romman (`@aliromman`) supplied [PR #5580](https://github.com/CrocSwap/integer-mult-bounds/pull/5580) (`research/p104-event-contact-step`) and the complete caller/source closure in [PR #5544](https://github.com/CrocSwap/integer-mult-bounds/pull/5544) and [PR #5545](https://github.com/CrocSwap/integer-mult-bounds/pull/5545).
- Joel Pulikkan (`@GamingPuzzled`) supplied [PR #5569](https://github.com/CrocSwap/integer-mult-bounds/pull/5569) (`research/p104-priced-handoff`).
- `@DreamingOfClouds` supplied [PR #5561](https://github.com/CrocSwap/integer-mult-bounds/pull/5561), [PR #5568](https://github.com/CrocSwap/integer-mult-bounds/pull/5568), and [PR #5590](https://github.com/CrocSwap/integer-mult-bounds/pull/5590).
- `@thu-nmrc` supplied [PR #5551](https://github.com/CrocSwap/integer-mult-bounds/pull/5551).
- Retained source notices credit Gareth Davidson, David Arias, Cinna Davis, Jacob Alan Sussman, zxv, and Cao Yifan.
- Three-stage commuting-contact cascade construction, proof, and verification by Pierre-Loic Doulcet (`@hexapode`). Apache-2.0.
