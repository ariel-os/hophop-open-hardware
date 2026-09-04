# HopHop KiCad libraries

For KiCad 10.0 or newer. The project-root tables use `${KIPRJMOD}/libs`, so no
additional path configuration is needed when opening this project.

## Replacement results and library contents

Checked installed KiCad 10.0.4 and current official upstream libraries on
2026-09-10. [PROVENANCE.md](PROVENANCE.md) records the source revisions.

| Previous custom symbol | Replacement / retained library ID |
| --- | --- |
| `VSYS`, `VDD_GPIO` | Use stock `power:VDD`, setting its **Value** to `VSYS` or `VDD_GPIO`. KiCad 10 derives the global power net from Value. Removed unused custom duplicates; existing global labels remain. |
| `BQ25180YBGR` | No exact stock symbol: `HopHop_Battery_Management:BQ25180YBG` |
| `TPS63901YCJR` | No exact stock symbol: `HopHop_Regulator_Switching:TPS63901YCJ` |
| `TPS7A0228` | No exact stock symbol: `HopHop_Regulator_Linear:TPS7A0228YCH` |
| `DMN2990UFA`, `DMP22D4UFA` | No exact stock symbols: `HopHop_Transistor_FET:DMN2990UFA` / `DMP22D4UFA` |
| nRF9151 | Exact requested upstream symbol temporarily vendored as `HopHop_MCU_Nordic:nRF9151-LAxx`; [source and removal instructions](PROVENANCE.md). |

Tape/reel-only suffixes were removed from library symbol names; the LDO name now
specifies its YCH package. Existing placed component Values (including ordering
codes) are preserved. Schematic library IDs and custom footprint references have
been migrated to the functional library names.

The four custom footprints have no exact stock replacement and remain in
`HopHop_Package_BGA.pretty` and `HopHop_Package_DFN_QFN.pretty`. Similar stock BGAs
have different body, pitch or land dimensions. Generic MOSFET symbols omit these
parts' gate protection and use numeric pins; the custom MOSFETs and shared
footprint consistently use manufacturer terminal names **G/S/D**.

**Placed U1/U2 drawings retain their existing pin positions**, as do all other
wired components. New library drawings are available for new placements; updating
U1/U2 from the library requires rerouting. **The placed nRF9151 is also unchanged**;
the requested upstream symbol is installed in the library only, because its pin
layout differs substantially from that existing placement.

## Include the tables globally

1. In **Preferences → Configure Paths**, set `HOPHOP_LIB_DIR` to this `libs` directory.
2. In **Manage Symbol Libraries → Global Libraries**, add `libs/sym-lib-table` as a
   nested **Table**, named `HopHop`.
3. Similarly add `libs/fp-lib-table` in **Manage Footprint Libraries**.

The entries inside existing global tables are:

```scheme
(lib (name "HopHop") (type "Table") (uri "${HOPHOP_LIB_DIR}/sym-lib-table") (options "") (descr "HopHop symbols"))
```

```scheme
(lib (name "HopHop") (type "Table") (uri "${HOPHOP_LIB_DIR}/fp-lib-table") (options "") (descr "HopHop footprints"))
```

Keep KiCad's default library entries. These are
[KiCad 10 nested tables](https://docs.kicad.org/10.0/en/eeschema/eeschema.html#_nested_library_tables).
No user-wide configuration is modified by this repository.

## Validation and attribution

Run `python libs/validate.py`. It checks pin maps, land dimensions, pin/pad
compatibility, model-reference conventions, table and schematic references, and
the exact upstream nRF9151 checksum. See [KLC_AUDIT.md](KLC_AUDIT.md) for checker
results and [3dmodels/README.md](3dmodels/README.md) for unavailable models.

The custom IC drawings derive from KiCad's `Regulator_Switching:TPS63900` and
`Battery_Management:BQ25173DSG`; MOSFET drawings derive from
`Transistor_FET:DMG1012T`, with P-channel polarity adapted. These are graphical
templates, not electrically interchangeable devices. Adapted and vendored
symbols are distributed under KiCad's CC-BY-SA 4.0 library license with its
electronic-design exception; see [LICENSE-KiCad.md](LICENSE-KiCad.md) and the
[KiCad symbol libraries](https://gitlab.com/kicad/libraries/kicad-symbols).
