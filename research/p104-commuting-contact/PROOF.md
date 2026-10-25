# Proof of the P104 Three-Stage Commuting-Contact Cascade ($\kappa = 0.00308534$)

This package modifies the [PR #5580](https://github.com/CrocSwap/integer-mult-bounds/pull/5580) P104 word (`research/p104-event-contact-step`, pinned at `6efa248cf456d6101d757e9d09ba29711d18a13a`) in three algebraic stages:
- **Stage A (Fixed-Endpoint Commuting Writes on Port `198`):** Reorders four independent `ADD` writes into `198` (from `648, 649, 650, 652`) before `13528` to frame `3` (`0D`), vacating `597` (`1D`) on `648, 649, 650, 652` with all `initial` and `final` frames unchanged (`WORD-FIXED-ENDPOINTS.json.gz`, $\kappa = 0.00308415$).
- **Stage B (Commuting-Write Domino Cascade on `113, 531, 197, 319, 507`):** Reorders `13806` (`113 += 531`) before `13524` to frame `3` (`0D`) with `initial[531] = 3` (`0D`), vacating `597` (`1D`) on `531, 197, 507` and demoting `13846` (`197 += 319`) from `617` (`3D`) to `355` (`2D`) ($\kappa = 0.00308520$).
- **Stage C (Triangular Uncompute Commutation on `341, 345, 712`):** Commutes `345`'s uncompute `16920` (`345 += 4 * 712`) before `16654` (`341 += -345`) to 3-plane `739` right after `14444` (`347 += 345`), cancelling `16915` (`341 += 4 * 712`) by transitivity of `ADD` and retiring helper `341` at 4-plane `240` (`final[341] = 240`, deleting `16652: MOVE 341: 240 -> 127`) (`WORD.json.gz`, **conditional $\kappa = 0.00308534$**).

---

## 1. Stage A: Fixed-Endpoint Commuting Writes on Port `198` and Helpers `648, 649, 650, 652`

In the PR #5580 word, main port `198` stays at the 0-dimensional origin chart `3` (`[]`) from initialization through event `13527`, receiving only `ADD` writes (`198 += c * s`). At events `13528..13634`, the relevant events on `198` and helpers `648, 649, 650, 652` are:

```text
13528: ['MOVE', 198, 3, 597, False]
13529: ['ADD', 198, 710, '2', 597]
13623: ['ADD', 205, 648, '-1/2', 3]
13624: ['MOVE', 648, 3, 597, False]
13625: ['ADD', 198, 648, '1/2', 597]
13626: ['ADD', 205, 649, '-1/2', 3]
13627: ['MOVE', 649, 3, 597, False]
13628: ['ADD', 198, 649, '-1/2', 597]
13629: ['ADD', 205, 650, '-1/2', 3]
13630: ['MOVE', 650, 3, 597, False]
13631: ['ADD', 198, 650, '1/2', 597]
13632: ['ADD', 205, 652, '1/2', 3]
13633: ['MOVE', 652, 3, 597, False]
13634: ['ADD', 198, 652, '1/2', 597]
13770: ['MOVE', 648, 597, 120, False]
13772: ['MOVE', 649, 597, 120, False]
13774: ['MOVE', 650, 597, 120, False]
13778: ['MOVE', 652, 597, 120, False]
```

### Commutativity and Subspace Nesting (Stage A)
1. **Write-epoch commutativity on `198`:** Between `13528` and `13634`, register `198` is never read or scaled; its only operations are `13529` (`198 += 2 * 710`) and `13625, 13628, 13631, 13634` (`198 += ±1/2 * r` for `r in {648, 649, 650, 652}`). Additions into a common destination register commute with each other and with chart transport of that destination register.
2. **Read-epoch invariance on `648, 649, 650, 652`:** Each helper `r in {648, 649, 650, 652}` is initialized at chart `3` (`[]`, $\dim 0$) and is only read (never written or scaled) prior to event `13771`. Thus at event `13528`, each `r in {648, 649, 650, 652}` already holds its unmodified initial symbol at chart `3`.
3. **Elimination of chart `597` on `648, 649, 650, 652`:** Executing `13625, 13628, 13631, 13634` at chart `3` immediately before `13528: ['MOVE', 198, 3, 597, False]` eliminates the four climbs `3 -> 597` (`13624, 13627, 13630, 13633`) and replaces the four climbs `597 -> 120` (`13770, 13772, 13774, 13778`, where `120` has 5-dimensional basis `[7, 25, 75, 160, 288]`) with direct climbs `3 -> 120`.
4. **Stage A Paid Delta:** On each of `648, 649, 650, 652`, the paid itinerary `3 (0D) -> 597 (1D) -> 120 (5D)` (`H1 + H4`) becomes `3 (0D) -> 120 (5D)` (`H5`). All 735 `initial` and `final` frames and all 527 helper targets remain unchanged. The Stage A local paid delta is:
   $$\Delta P_{\text{Stage A}} = -4 H_1 - 4 H_4 + 4 H_5$$
   which reduces complete paid calls by $72$ (`66,852 -> 66,780`) and raises the raw moment crossing from `(0.00308189496866, 0.00308189496867)` to `(0.00308415555080, 0.00308415555081)`. This supporting word is shipped as `WORD-FIXED-ENDPOINTS.json.gz`.

---

## 2. Stage B: Commuting-Write Domino Cascade on `113, 531, 197, 319, 507`

In the PR #5580 word, main port `113` stays at chart `3` (`0D`) up to event `13524`, where it moves `3 -> 597` (`[82]`, $\dim 1$) for `13525: ['ADD', 113, 710, '2', 597]`, followed by `13806: ['ADD', 113, 531, '1', 597]`. Because PR #5561's fixed-order solver could not commute `13806` before `13525`, helper `531` was forced to start at `597` (`1D`), which in turn forced `197` and `507` to climb `3 -> 597` for `13843: ['ADD', 197, 531, '-1', 597]` and `14404: ['ADD', 507, 531, '-1', 597]`:

| Frame | Basis | Dimension |
| --- | --- | --- |
| `3` | `[]` | 0 |
| `355` | `[30, 44]` | 2 |
| `597` | `[82]` | 1 |
| `617` | `[30, 44, 76]` | 3 |
| `728` | `[30, 44, 76, 391]` | 4 |
| `741` | `[13, 19, 65, 423]` | 4 |
| `788` | `[13, 19, 33, 65, 390]` | 5 |

Note that $30 = 13 \oplus 19 \in \text{span}(788)$ and $44 = 13 \oplus 33 \in \text{span}(788)$, so $\text{span}(3) \subset \text{span}(355) \subset \text{span}(788)$ and $\text{span}(355) \subset \text{span}(728)$ are strict subspace chains.

### Domino Cascade Steps (Stage B)
1. **Commute `13806` before `13524` at chart `3` (`0D`):** Between `13524` and `13806`, register `113` receives only `ADD` writes (`13525` and `13806`), and helper `531` is in its initial read-only epoch (unmodified until `14478`). Setting `initial[531] = 3` (`0D`) and executing `13806: ['ADD', 113, 531, '1', 3]` immediately before `13524: ['MOVE', 113, 3, 597, False]` preserves `113`'s itinerary `3 (0D) -> 597 (1D) -> 614 (3D)`.
2. **Vacate `597` (`1D`) on `531, 197, 507`:** Because `531` is now at chart `3` (`0D`) during its initial read epoch, `13843: ['ADD', 197, 531, '-1', 3]` and `14404: ['ADD', 507, 531, '-1', 3]` execute at chart `3` (`0D`). Helper `507` skips `597` (`1D`) and climbs directly `3 (0D) -> 728 (4D)` (`H4` instead of `H1 + H3`), and helper `531` climbs `3 (0D) -> 741 (4D)` (`H4` instead of `H3`) while its helper target credit increases from `H8` (`9 - 1`) to `H9` (`9 - 0`).
3. **Demote `13846` (`ADD 197 += 319`) from `617` (`3D`) to `355` (`2D`):** Because `197` stays at `3` (`0D`) after `13843` instead of climbing to `597` (`[82]`, which is not in `span(355) = span([30, 44])`), `197` now climbs directly `3 (0D) -> 355 (2D)` to meet `319` at `355` (`2D`) for `13846: ['ADD', 197, 319, '1', 355]`, and then climbs `355 (2D) -> 788 (5D)`. This vacates `617` (`3D`) on both `197` (`H2 + H3` instead of `H1 + 2 H2`) and `319` (`355 (2D) -> 728 (4D)`, `H2` instead of `2 H1`).

---

## 3. Stage C: Triangular Uncompute Commutation on `(341, 345, 712)`

In the PR #5580 word, helper `341` (`initial[341] = 3` (`0D`), `final[341] = 127` (`9D`)) finishes all of its lower-dimensional work at event `11161` in 4-plane `240` (`[13, 19, 70, 416]`), where its symbolic value is:
$$\text{row}(341)\big|_{11161} = -\{341: 1\} + \text{row}(345)\big|_{11066}$$
and `341` is never read again after `11161`. In PR #5580, `341, 345, 712` execute:

```text
13568: ['MOVE', 712, 598, 391, False]
13569: ['ADD', 345, 712, '-4', 391]
13809: ['ADD', 170, 345, '-1/2', 391]
14443: ['MOVE', 345, 391, 739, False]
14444: ['ADD', 347, 345, '1', 739]
...
16652: ['MOVE', 341, 240, 127, False]
16653: ['MOVE', 345, 739, 127, False]
16654: ['ADD', 341, 345, '-1', 127]
16655: ['SCALE', 341, '-1', 127]
...
16899: ['MOVE', 712, 391, 127, False]
16915: ['ADD', 341, 712, '4', 127]
16920: ['ADD', 345, 712, '4', 127]
```

### Why `341` Was Trapped at `127` (`9D`) and How Triangular Commutation Frees It
1. **Triangular pollution of `341` via `345`:** Between `11066` and `16920`, register `345` is modified only at `13569` (`345 += -4 * 712` at 2-plane `391`), read by `170` at `13809` (`391`) and by `347` at `14444` (3-plane `739`), read by `341` at `16654` (`341 += -345`), and restored at `16920` (`345 += 4 * 712`). Because `16654` (`341 += -345`) executed *before* `16920` (`345 += 4 * 712`), `341` inherited $+4 \cdot \text{row}(712)$ at `16654` (flipped to $-4 \cdot \text{row}(712)$ by `16655: SCALE 341 *= -1`) and therefore needed `16915: ['ADD', 341, 712, '4', 127]` to cancel it!
2. **Strict nested subspace chain:** The four charts on `(712, 345, 341)` form a strict nested subspace chain:

| Frame | Basis | Dimension | Subspace Verification |
| --- | --- | --- | --- |
| `391` | `[30, 491]` | 2 | $30 \in \text{span}(739)$ and $491 = 30 \oplus 70 \oplus 429 \in \text{span}(739)$ |
| `739` | `[30, 70, 429]` | 3 | $30 = 13 \oplus 19 \in \text{span}(240)$, $70 \in \text{span}(240)$, $429 = 13 \oplus 416 \in \text{span}(240)$ |
| `240` | `[13, 19, 70, 416]` | 4 | $\text{span}(240) \subsetneq \text{span}(127) = \mathbb{F}_2^9$ |
| `127` | `[1, 2, 4, 8, 16, 32, 64, 128, 256]` | 9 | Full 9-space |

3. **Triangular uncompute commutation:** Since `345` has no operations between `14444` and `16654`, and `712` has no operations between `13570` (in `391`, `2D`) and `16899`:
   - Right after `14444: ['ADD', 347, 345, '1', 739]`, `712` climbs `391 (2D) -> 739 (3D)` (`H1` paid) and `345` executes `['ADD', 345, 712, '4', 739]` at `739` (`3D`), restoring $\text{row}(345) = \text{row}(345)|_{11066}$.
   - `345` then climbs `739 (3D) -> 240 (4D)` (`H1` paid), where `341` (already at `240` since `11161`) executes `['ADD', 341, 345, '-1', 240]` and `['SCALE', 341, '-1', 240]` at `240` (`4D`).
   - Because $-4 \cdot \text{row}(712)$ was already cancelled in `345` before `341` read `345`, `341` is immediately restored to $\{341: 1\}$ at `240` (`4D`)! Thus `16915: ['ADD', 341, 712, '4', 127]` cancels out identically and is deleted (`-1` scalar `ADD`), `16652: ['MOVE', 341, 240, 127, False]` (`-H5` paid) is deleted, and `341` retires at `final[341] = 240` (`4D` instead of `9D`, target delta $+H_4 - H_9$).
   - Finally, `345` climbs `240 (4D) -> 127 (9D)` (`H5` paid, replacing `739 -> 127` `H6`), and `712` climbs `739 (3D) -> 127 (9D)` (`H6` paid, replacing `391 -> 127` `H7`).
4. **Stage C Delta:**
   $$\Delta P_{\text{Stage C}} = (-H_5) + (H_1 + H_5 - H_6) + (H_1 + H_6 - H_7) = +2 H_1 - H_7, \qquad \Delta T_{\text{Stage C}} = +H_4 - H_9$$
   At $\kappa \approx 0.00308521$, $\Delta(T - P)_{\text{Stage C}} = (H_4 - H_9) - (2 H_1 - H_7) = -4.948276 - (-4.950110) = +0.00183337 > 0$.

---

## 4. Combined Stage A+B+C Invoice and Strict Concave Gain

Combining Stages A, B, and C across each of the 18 forward local calls gives:
- **Local paid delta:** $\Delta P_{\text{local}} = -6 H_1 - H_3 - 2 H_4 + 4 H_5 - H_7$ (`-6` local `MOVE` instructions, `-1` scalar `ADD`, `25,140 -> 25,133` events).
- **Global paid delta (18 calls):** $\Delta P = -108 H_1 - 18 H_3 - 36 H_4 + 72 H_5 - 18 H_7$ (`-108` paid calls, `66,852 -> 66,744`).
- **Local target delta:** $\Delta T_{\text{local}} = (-H_8 + H_9) + (H_4 - H_9) = +H_4 - H_8$ (`+18 H_4 - 18 H_8` globally, keeping `12,814` productive fields and rank-mass surplus `760` invariant).

The exact rational interval engines enclose the raw moment crossings:

| Word | Lower endpoint | Upper endpoint |
| --- | --- | --- |
| PR #5580 (`p104-event-contact-step`) | `0.00308189496866` | `0.00308189496867` |
| Stage A (`WORD-FIXED-ENDPOINTS.json.gz`) | `0.00308415555080` | `0.00308415555081` |
| Stage A+B (intermediate cascade) | `0.00308521055201` | `0.00308521055202` |
| Stage A+B+C (`WORD.json.gz`, headline) | `0.00308534541177` | `0.00308534541178` |

The raw gain over PR #5580 is strictly between `0.00000345044310` and `0.00000345044312`. The claimed conditional saving is **$\kappa = 0.00308534$**, tested at `0.0030853405` with raw headroom `5.41177e-9 .. 5.41178e-9`.
