# Library audit — 2026-09-10

Scope: the project's custom symbol and footprint libraries. KiCad 10.0.4 was used to load/render the files and export validation netlists. This is not a full schematic electrical-design review or PCB manufacturing signoff; the project PCB contains no placed footprints.

## Manufacturer checks and corrections

| Part | Result and source |
| --- | --- |
| TPS63901YCJR | Rebuilt from the TPS63900 drawing with its **12-ball** pin map. A1 LX1, A2 VIN, A3 EN; B1 GND, B2 CFG1, B3 SEL; C1 GND, C2 VOUT, C3 CFG2; D1 LX2, D2 VOUT, D3 CFG3. Native `[B1,C1]` and `[C2,D2]` pin stacks. The previous 0.5 mm-pitch footprint was wrong. New YCJ0012-C02 footprint: nominal body 1.15 × 1.50 mm, 3 × 4 array, 0.35 mm pitch. TI's preferred mask-defined land: 0.18 mm opening, 0.255 mm copper, 0.18 mm paste. [TI datasheet, pp. 3, 28–30](https://www.ti.com/lit/ds/symlink/tps63901.pdf). |
| BQ25180YBGR | Rebuilt using the BQ25173DSG centered charger drawing style; these devices are **not pin-compatible**. A1 interrupt, A2 IN, B1 SCL, B2 SYS, C1 SDA, C2 BAT, D1 TS/MR, D2 GND. Interrupt is open-drain (`open_collector` in KiCad); BAT is passive because current flows both ways. SCL/SDA and TS/MR retain TI's I/O classification. Correct YBG0008-C01 footprint: nominal 1.04 × 1.59 mm body, 2 × 4 array, 0.4 mm pitch, 0.23 mm copper/paste circles, 0.04 mm mask expansion. Previous body dimensions and footprint metadata were wrong. [TI datasheet, pp. 4, 52–54](https://www.ti.com/lit/ds/symlink/bq25180.pdf). |
| DMN2990UFA / DMP22D4UFA | N-channel / P-channel polarity and body-diode directions were correct. Gate ESD protection was missing and has been added using KiCad's protected-MOSFET drawing. Both parts share X2-DFN0806-3. The copied TI PicoStar land patterns, descriptions, and model links were wrong. [Diodes DMN2990UFA, pp. 1, 5](https://www.diodes.com/assets/Datasheets/DMN2990UFA.pdf); [Diodes DMP22D4UFA, pp. 1, 5](https://www.diodes.com/assets/Datasheets/DMP22D4UFA.pdf). |
| TPS7A0228 | Existing library symbol also needed a centered body, visible fields, metadata and a valid default footprint. Preserved its existing short symbol name. A1 IN, A2 OUT, B1 EN, B2 GND. YCH0004: nominal 0.637 mm square body, 2 × 2 array, 0.35 mm pitch. Existing 0.2 mm NSMD copper land was a documented option; changed to TI's preferred mask-defined option: 0.265 mm copper with 0.2 mm mask/paste opening. [TI datasheet, YCH pin table and package drawing 4224061/A](https://www.ti.com/lit/ds/symlink/tps7a02.pdf). |

### Shared MOSFET footprint and symbol reuse

In the manufacturer's **top view**, drain is left, source upper right, gate lower right. The new footprint rotates that view 180°: gate upper left, source lower left, drain right. Its body is 0.8 × 0.6 mm in that orientation.

| Terminal / pad ID | Center X, Y (mm) | Pad width × height (mm) |
| --- | --- | --- |
| G | −0.3125, −0.175 | 0.375 × 0.200 |
| S | −0.3125, +0.175 | 0.375 × 0.200 |
| D | +0.2625, 0 | 0.475 × 0.450 |

These follow the [Diodes package land-pattern drawing](https://www.diodes.com/assets/Package-Files/X2-DFN0806-3.pdf): 1.0 mm total span, 0.35 mm small-pad pitch, and 0.15 mm gap between drain and the small pads. Pads have KLC rounded corners. The geometric package drawing labels a feature “Pin#1”, while the device connection diagram labels terminals by function without a full numbered map. Named **G/S/D** identifiers avoid inventing a manufacturer numeric mapping. The old `1=G, 2=S, 3=D` identifiers were changed consistently in the symbols, placed copies, and footprint.

Stock `Q_NMOS_GSD` / `Q_PMOS_GSD` can represent the basic transistor if deliberately paired with a numeric GSD footprint, but they omit the internal ESD network and cannot directly use this named-pad footprint. The existing DMG1012T drawing is a suitable **graphical template**, not a substitute part or footprint.

## KLC findings

Checked against the [current KLC](https://klc.kicad.org/), with [KiCad library-utils](https://gitlab.com/kicad/libraries/kicad-library-utils) master downloaded on the audit date. Raw output is in [klc-symbols.txt](klc-symbols.txt) and [klc-footprints.txt](klc-footprints.txt).

| Area | Status |
| --- | --- |
| Five physical component symbols | Automated symbol checks pass after fixing geometry, fields, filters, and electrical types. |
| Two power symbols | Manually verified against [current S7.1](https://klc.kicad.org/symbol/s7/s7.1/): global power definition, hidden `#PWR`, one visible zero-length `power_in` pin named `~`, visible matching value, no footprint. Both produce the correct global nets in an actual KiCad export. The checker still requires an invisible pin named after the rail and flags `#PWR` in this project library; those legacy S7.1/S6.1 diagnostics conflict with current power-symbol requirements. |
| Footprint geometry and metadata | All four pass the automated checks except F9.3. Reviewed pad positions, paste/mask layers, nominal fab bodies, identification marks, 0.12 mm silk, 0.10 mm fab and 0.05 mm courtyard lines. Courtyards use a 0.01 mm grid and at least 0.25 mm package/pad clearance. |
| 3D models, F9.3 | **Outstanding for all four footprints.** No verified local models were present. Removed incorrect PicoStar links; no fictional/missing model paths were added. |
| Library organization, G1.3/S1.1/F1.1 | **Project convention retained:** one mixed-function `GrassHopperNymph` library for compatibility. Upstream KiCad submissions should instead use functional libraries. |
| Symbol naming, S2.2 | **Requested names retained:** TPS63901YCJR and BQ25180YBGR include tape/reel ordering suffixes. Upstream submissions should omit packaging-only suffixes. TPS7A0228 remains a compatibility name and would need explicit package naming for upstream use. |
| Manufacturer overrides | Negative mask/paste margins on YCJ/YCH implement TI's documented preferred SMD lands; they are intentional departures from default local settings under [F4.1](https://klc.kicad.org/footprint/f4/f4.1/). |

**Verdict:** corrected and validated project libraries, with the listed exceptions; not an unconditional claim of full upstream KLC compliance.

## Validation and project impact

- `python libs/validate.py`: seven symbols, datasheet pin maps, native stack membership, all four land-pattern dimensions, pin/pad identity, footprint filters, visible values, power definitions and both table sets pass.
- KiCad symbol SVG export: all seven symbols loaded and rendered; drawings visually reviewed.
- KiCad footprint loader: all four footprints loaded with 3/8/4/12 pads as expected; a temporary board exported successfully.
- A separate KiCad netlist fixture verified that TPS63901 stacks expand to **all 12 physical balls** and the new power symbols produce **VSYS** and **VDD_GPIO** global nets.
- Before/after project netlist comparison: **151 of 151 net connectivity groups unchanged**, accounting only for the intentional MOSFET terminal-ID migration. All project custom footprint assignments resolve.
- MOSFET placed copies include the corrected drawing and named pins. U1/U2 retain their existing cached drawing positions, with corrected footprint/data references and relevant electrical types. Replacing those cached drawings with the rebuilt library layouts requires rerouting their wires; it was not part of the library reorganization. The original separate TPS63900 placement remains unchanged.
- Existing VSYS/VDD_GPIO global labels were preserved. New power symbols are available for placement.
- Pre-existing edits to the project and unrelated sheets were preserved. No ERC-clean or production-ready claim is made for the wider circuit.

To rerun the external checks (set `KICAD_LIBRARY_UTILS` to your checkout):

```sh
python "$KICAD_LIBRARY_UTILS/klc-check/check_symbol.py" --nocolor -vv --footprints libs/footprints libs/symbols/GrassHopperNymph.kicad_sym
python "$KICAD_LIBRARY_UTILS/klc-check/check_footprint.py" --nocolor -vv libs/footprints/GrassHopperNymph.pretty/*.kicad_mod
```
