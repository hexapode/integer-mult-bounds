# CLAIM — P104 three-stage commuting-contact cascade on the PR #5580 word

Base: canonical main `5e0052ca0aa3036a3afa8b0438927377c8d97d53`, priority revision 7.
Exact construction input: [PR #5580](https://github.com/CrocSwap/integer-mult-bounds/pull/5580) at `6efa248cf456d6101d757e9d09ba29711d18a13a` (`research/p104-event-contact-step`, conditional $\kappa = 0.00308189$).

Question: PR #5580 and PR #5590 proved that `#5580` attains the exact price floor `(0.00308189496866, 0.00308189496867)` when the scalar instruction sequence and contact charts are held fixed, and left open whether reordering scalar events within commuting windows can improve the complete paid profile.

Result:
1. **Stage A (Fixed-Endpoint Supporting Word `WORD-FIXED-ENDPOINTS.json.gz`, $\kappa = 0.00308415$):** Commuting `13625, 13628, 13631, 13634` (`198 += ±1/2 * 648/649/650/652`) before `13528` (`MOVE 198: 3 -> 597`) to frame `3` (`0D`) vacates frame `597` (`1D`) on all four helpers `648, 649, 650, 652`, collapsing `3 (0D) -> 597 (1D) -> 120 (5D)` (`H1 + H4`) into `3 (0D) -> 120 (5D)` (`H5`). All 735 `initial` and `final` frames and all 527 helper targets remain identical to PR #5580. Local paid delta: `-4 H1 - 4 H4 + 4 H5` (`-72` complete paid calls, `66,852 -> 66,780`), raising the raw crossing to `(0.00308415555080, 0.00308415555081)` (`+2.26058214e-6` over PR #5580).
2. **Stage B (Commuting-Write Domino Cascade on `113, 531, 197, 319, 507`):** Commuting `13806` (`113 += 531`) before `13524` (`MOVE 113: 3 -> 597`) to frame `3` (`0D`) allows all three initial read contacts of helper `531` (`13806` with `113`, `13843` with `197`, and `14404` with `507`) to execute at frame `3` (`0D`) with `initial[531] = 3`. Because `197` remains at `3` (`0D`) after `13843`, its next contact `13846` (`197 += 319`) demotes from 3-plane `617` (`[30, 44, 76]`) to 2-plane `355` (`[30, 44]`), vacating `617` on both `197` and `319` and vacating `597` on `531, 197, 507` (`-4 H1 - H3 + 2 H4` paid, `-H8 + H9` target, raising the raw crossing to `0.00308521055201..0.00308521055202`).
3. **Stage C (Triangular Uncompute Commutation on `341, 345, 712`, Headline Word `WORD.json.gz`, $\kappa = 0.00308534$):** Helper `341` completes all lower-dimensional work at event `11161` in 4-plane `240` (`[13, 19, 70, 416]`), where $\text{row}(341)|_{11161} = -\{341: 1\} + \text{row}(345)|_{11066}$. In PR #5580, `341` jumped `240 (4D) -> 127 (9D)` (`16652`) only to execute `16654: 341 += -345`, `16655: 341 *= -1`, and `16915: 341 += 4 * 712`, because `345` added `-4 * row(712)` at `13569` (for readers `170` at `13809` and `347` at `14444`) before uncomputing `16920: 345 += 4 * 712` after `16654`. Since $\text{span}(391)\,(2\text{D}) \subsetneq \text{span}(739)\,(3\text{D}) \subsetneq \text{span}(240)\,(4\text{D}) \subsetneq \text{span}(127)\,(9\text{D})$, commuting `16920: 345 += 4 * 712` before `16654: 341 += -345` to frame `739` (`3D`) right after `14444` cancels `16915: 341 += 4 * 712` identically (`-1` scalar `ADD`) and retires `341` directly at `final[341] = 240` (`4D`, deleting `16652: MOVE 341: 240 -> 127`). Combined Stage A+B+C local paid delta vs PR #5580: `-6 H1 - H3 - 2 H4 + 4 H5 - H7` (`-108` complete paid calls, `66,852 -> 66,744`), with local helper target delta `+H4 - H8` (productive fields `12,814` and rank-mass surplus `760` unchanged), raising the raw crossing to `(0.00308534541177, 0.00308534541178)` and certifying **conditional $\kappa = 0.00308534$** at `TESTED = 0.0030853405` (`+3.45044311e-6` raw over PR #5580).

```json
{
  "schema": "integer-mult-coordination/v1",
  "kind": "CLAIM",
  "task": "scalar-to-moment",
  "scope": "P104 three-stage commuting-contact cascade on the PR5580 word; complete paid-profile step",
  "base": "5e0052ca0aa3036a3afa8b0438927377c8d97d53",
  "expiry": "2026-10-25T23:59:59+00:00",
  "artifact": "research/p104-commuting-contact"
}
```
