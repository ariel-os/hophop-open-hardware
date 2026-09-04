# Library audit — 2026-09-10

Scope: project-owned symbols and footprints, plus the requested upstream nRF9151
symbol. Replacements were checked against installed KiCad 10.0.4 and current
official upstream sources; [PROVENANCE.md](PROVENANCE.md) pins the snapshots and
[README.md](README.md) lists the resulting library IDs.

## Current KLC results

- Five retained custom physical symbols: **zero checker errors or warnings**.
  Functional libraries replace the mixed library (G1.3/S1.1); packaging-only
  suffixes are removed and the LDO package is explicit (S2.2/S2.3).
- Four retained custom footprints: **zero checker errors or warnings**.
  BGA and DFN footprints are grouped separately (F1.1); all now have F9.3 STEP
  references with matching library/basename, unit scale, and zero transforms.
  Models themselves are unavailable; F9.3 explicitly allows this. See
  [3dmodels/README.md](3dmodels/README.md).
- `VSYS` and `VDD_GPIO`: removed unused duplicates in favor of stock `power:VDD`
  with edited Value, supported by KiCad 10. Existing schematic global labels are
  unchanged. This also eliminates the old checker's power-symbol diagnostics.
- Vendored nRF9151: kept byte-for-byte as requested. The checker reports S4.2
  for power-pin grouping and S4.3 for its legacy GND stack. The MR explicitly
  documents the S4.2 grouping decision; the current checker also requests native
  stacks. Neither is silently corrected in this temporary upstream copy.

Raw results: [custom symbols](klc-symbols.txt), [footprints](klc-footprints.txt),
[upstream nRF9151](klc-nrf9151.txt). The custom-library checks pass without rule
exclusions. This does not claim the unchanged upstream symbol is KLC-clean.
Manufacturer mask/paste overrides below remain intentional under F4.1.

## Validation and schematic impact

- `python libs/validate.py`: custom pin maps, four land patterns, pin/pad identity,
  model references, library tables, placed project references and exact nRF9151
  source hash pass.
- KiCad rendered all six library symbols and loaded all four footprints with
  the expected 3/4/8/12 pads. The Python footprint loader emitted enum-choice
  assertions during initialization but returned all four footprints successfully.
- KiCad 10.0.4 exported the project netlist before and after migration:
  **151 of 151 connectivity groups unchanged**, with **107 component Values
  unchanged**. Library IDs and footprint assignments changed; pin identifiers,
  wire geometry, instance UUIDs and BOM values did not.
- Existing wired U1/U2 retain their cached drawings. Replacing those with the
  library drawings requires rerouting their changed pin positions.
- nRF9151 is imported into the chooser only; its existing Nordic-library
  placement is unchanged. See provenance for later migration/removal.
- Pre-existing project renames and schematic edits were preserved. This is not
  a full circuit/ERC or PCB manufacturing review; the board has no placements.

## Reproduce external checks

Set `KICAD_LIBRARY_UTILS` to the checkout recorded in provenance:

```sh
python "$KICAD_LIBRARY_UTILS/klc-check/check_symbol.py" --nocolor -vv --footprints libs/footprints libs/symbols/HopHop_Battery_Management.kicad_sym libs/symbols/HopHop_Regulator*.kicad_sym libs/symbols/HopHop_Transistor_FET.kicad_sym
python "$KICAD_LIBRARY_UTILS/klc-check/check_footprint.py" --nocolor -vv libs/footprints/*/*.kicad_mod
python "$KICAD_LIBRARY_UTILS/klc-check/check_symbol.py" --nocolor -vv --footprints /usr/share/kicad/footprints libs/symbols/HopHop_MCU_Nordic.kicad_sym
```

## Retained manufacturer audit

The following dimensional/pin-map findings predate this replacement pass. Part
numbers below retain manufacturer ordering codes; current symbol IDs are in
README.md. Geometry and electrical maps remain unchanged in this pass.

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
