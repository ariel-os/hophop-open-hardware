# HopHop KiCad libraries

For KiCad 10.0 or newer. Library nickname: `GrassHopperNymph`.

```text
libs/
  sym-lib-table
  fp-lib-table
  symbols/GrassHopperNymph.kicad_sym
  footprints/GrassHopperNymph.pretty/
  3dmodels/
```

The project-root library tables already reference these files using `${KIPRJMOD}/libs`; opening this project requires no additional path configuration.

## Include the tables globally

1. In **Preferences → Configure Paths**, set `HOPHOP_LIB_DIR` to the absolute path of this `libs` directory.
2. In **Manage Symbol Libraries → Global Libraries**, use the arrow next to the add-existing-library folder button, select **Table**, and select `libs/sym-lib-table`.
3. In **Manage Footprint Libraries → Global Libraries**, similarly select **Table** and `libs/fp-lib-table`.

Use `HopHop` as the nickname of each nested table. The individual symbol and footprint library nicknames inside those tables remain `GrassHopperNymph`. Keep KiCad's existing default library entries.

The equivalent entries to add inside your existing global tables are:

```scheme
(lib (name "HopHop") (type "Table") (uri "${HOPHOP_LIB_DIR}/sym-lib-table") (options "") (descr "HopHop symbols"))
```

```scheme
(lib (name "HopHop") (type "Table") (uri "${HOPHOP_LIB_DIR}/fp-lib-table") (options "") (descr "HopHop footprints"))
```

These are [KiCad 10 nested library tables](https://docs.kicad.org/10.0/en/eeschema/eeschema.html#_nested_library_tables). Global tables use `HOPHOP_LIB_DIR`, so they also work when another project is open. This repository does not modify your user-wide KiCad configuration.

## Symbols and assignments

| Symbol | Footprint family |
| --- | --- |
| `VSYS`, `VDD_GPIO` | Global power symbols; no footprint |
| `TPS63901YCJR` | TI YCJ0012-C02, 12 balls, 0.35 mm pitch |
| `BQ25180YBGR` | TI YBG0008-C01, 8 balls, 0.4 mm pitch |
| `DMN2990UFA`, `DMP22D4UFA` | Shared Diodes X2-DFN0806-3, **named G/S/D pads** |
| `TPS7A0228` | TI YCH0004, 4 balls, 0.35 mm pitch |

The misspelled library symbol `TPS63901YCR` is now `TPS63901YCJR`. The MOSFETs use named G/S/D terminals and pads, matching the datasheet's functional pin diagram rather than assuming a numeric package pinout. Their placed schematic copies and pin identifiers have been updated together.

**Existing wired U1/U2 placements retain their original drawing and pin locations.** Their footprint assignments, datasheets, and relevant pin electrical types have been repaired. The newly drawn BQ25180/TPS63901 library symbols are available for new placements. Updating U1/U2 from the library changes pin locations and requires rerouting the affected wires; this library reorganization does not perform that schematic-layout change. Existing VSYS/VDD_GPIO global labels remain valid; the new power symbols are available in the chooser.

See [KLC_AUDIT.md](KLC_AUDIT.md) for verified dimensions, remaining exceptions, and validation results. There were no project-owned 3D files to move; [3dmodels/README.md](3dmodels/README.md) records the model status.

## Validation and attribution

Run `python libs/validate.py` from the hardware directory, or run the script by absolute path. It checks manufacturer pin maps, pad dimensions and orientation, symbol-to-footprint compatibility, visible values, and table paths.

The IC drawings derive from the installed KiCad `Regulator_Switching:TPS63900` and `Battery_Management:BQ25173DSG`. The MOSFET drawings derive from `Transistor_FET:DMG1012T` with the P-channel arrow/body diode reversed where appropriate. Power drawings derive from `power:VDD`. These adapted drawings are distributed under KiCad's CC-BY-SA 4.0 library license with its electronic-design exception; see [LICENSE-KiCad.md](LICENSE-KiCad.md). Sources: [KiCad symbol libraries](https://gitlab.com/kicad/libraries/kicad-symbols).
