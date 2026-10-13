# Optional group-619 demotion on the PR1169 T37 construction

This package supplies and reconstructs the conditional integer-multiplication saving

**κ = 1675657692049141 / 1000000000000000000 = 0.001675657692049141.**

It improves the independently reproduced PR1169 certificate `0.001675568675201533` by exactly `11127105951 / 125000000000000000` (`0.000000089016847608`). The comparison baseline is PR1169 head `13d02293a7af67d7e3bd2e4d7f1a2943ac20537e`, whose joint entrance word comes from PR1148. This is a comparison with that pinned conditional construction, not an assertion of perpetual frontier status or maintainer acceptance.

**Frontier status:** This is independent work, not a live-record claim. Parallel [PR1193](https://github.com/CrocSwap/integer-mult-bounds/pull/1193), pinned at `8b005a92f16730bd054416d07d3788efbf53d515`, was independently reproduced at the stronger `0.001675672695827067` with a distinct demotion and 208 changed calls. Our added value is the optional group-619 construction and its reproducible augmenting-path transcript.

The change is concrete: redistribute existing equal-width owner positions, then use an additional group-619 entrance demotion at **178 of 333 calls**. The other 155 calls use the baseline provider. The changed helpers are **619, 621, 622 and 623**, each widening from four to five occupied coordinates. Their local paid cost changes, but each altered call also fills four actual unit gaps. No scalar instruction, coefficient, instruction order, endpoint or centre interface changes. The new provider has 23 changed B-frame annotations.

The final 178-call construction passed both the complete research strict replay and a fresh standalone package replay at the stated value. Commands, stage exit codes, source hashes and log hashes are recorded in `evidence/VALIDATION.json`. The standalone publication wrapper below separately rebuilds and checks the frozen package; its generated final `RESULT.json` is authoritative for a fresh package run. `EXPECTED.json` records the exact frozen nomination, not proof by itself.

## Reproduce

Use **Python 3.13+**, a C++ compiler and Boost headers. Python 3.13 is the tested interpreter. The unchanged PR1169 wrapper compares generated gzip container hashes; Python 3.11 produces a different gzip OS byte and fails its PLAN equality even when owner payloads are identical. This package requires the compatible interpreter rather than changing upstream checks.

From repository root:

```sh
CPLUS_INCLUDE_PATH=/path/to/boost/include python3.13 -B \
  research/game-latest-quests/verify.py --work /absolute/new/output-directory
```

The Boost path must contain `boost/`. The work directory must be new and outside this package. Verification needs no network, optimization solver, prior local replay or discovery mode. `vendor/pr1169` preserves the complete pinned source package and its archived dependencies. Source and generated artifacts are hash-bound.

The verifier deterministically replays 38,931 neutral exchanges and the frozen within-call permutations, rebuilds both local words, and performs:

- The unchanged PR1169 verification, with fresh baseline native and T37 global admission. Its archived, pinned parent geometry is explicitly reused and its actual windows reconstructed; unchanged ancestry is not claimed as freshly regenerated.
- Fresh changed-provider scalar, frame, wrapper and exact phase verification, plus an independent 704-column local audit and three destructive local controls.
- Strict mixed provider binding, controller audit, complete finite invoice, exact pricing and all 47 outer inequalities.
- An independent recount of all 159,840 whole-helper roles, seven original owner controls and an additional wrong-provider dispatch control. All 114 mixed admission controls, 23 controller controls and 12 bit-supplier controls remain enabled.

Expected final status:

```text
PASS_FRESH_LATEST_T37_OPTIONAL619_COMPLETE_ADMISSION 0.001675657692049141
```

The final bounded continuation checked 94,694 breadth-first path queries through depth eight without finding another augmenting path. This is a scoped search result, not an optimality claim. All searches are stopped.

The complete profile is `{1:785910, 2:167258, 3:137908, 4:42578, 5:27306, 8:2664, 48:11374}`. The idle profile is `{1:122, 48:11374}`. Prefix bound remains 775 < 1024 and physical row coefficient remains 17,495 < 20,161. The conservative certificate is `0.001675657689206397`.

The accompanying [proof](PROOF.md) explains why the gain lies outside the baseline's fixed-inventory packing ceiling. All inherited conditional compiler, hosting, precision/tape, exact-recovery, analytic-transfer and bit-supplier obligations remain. Finite certificate success is not a formal proof of the complete asymptotic multiplication theorem and is not a measured runtime speedup. See [NOTICE](NOTICE.md) for source credits and AI assistance.
