# Temporary upstream nRF9151 symbol

`symbols/HopHop_MCU_Nordic.kicad_sym` is an **unmodified, byte-for-byte copy** of
`MCU_Nordic.kicad_symdir/nRF9151-LAxx.kicad_sym` from
[KiCad symbols merge request !4932](https://gitlab.com/kicad/libraries/kicad-symbols/-/merge_requests/4932),
“Add Nordic nRF9151 SiP”, merged 2026-09-07.

- MR head commit: `4af520f0311b78308fcd575a1670fb9cb7364658`.
- [Pinned source](https://gitlab.com/kicad/libraries/kicad-symbols/-/blob/4af520f0311b78308fcd575a1670fb9cb7364658/MCU_Nordic.kicad_symdir/nRF9151-LAxx.kicad_sym).
- Retrieved 2026-09-10 from the MR's added-file diff; compared byte-for-byte with current upstream master.
- SHA-256: `1b0259f782029a0e144c33bf886970b0c4c023394163aa20060c97aab993ba28`.
- Attribution: KiCad library contributors; distributed under KiCad's CC-BY-SA 4.0 license with electronic-design exception, reproduced in [LICENSE-KiCad.md](LICENSE-KiCad.md).
- Local chooser ID: `HopHop_MCU_Nordic:nRF9151-LAxx`.
- Default footprint: `Package_LGA:Nordic_nRF9151-LAxx_LGA-80-33EP_12.1x11.1mm_P0.5mm`, already present in the installed KiCad 10.0.4 footprints.

This copy bridges the gap until the installed official symbol libraries contain
`MCU_Nordic:nRF9151-LAxx`. It does not shadow the official `MCU_Nordic` library.
The existing wired `nordic-lib-kicad-nrf9:nRF9151-LAXX` schematic placement is
unchanged: the upstream symbol has different pin positions, so replacing that
placement also requires reworking its connections. The imported symbol is ready
for selection from the project library.

## Remove after updating the installed libraries

1. Verify the local official library actually contains `MCU_Nordic:nRF9151-LAxx`
   and its footprint resolves; checking only the KiCad application version is insufficient.
2. Change any placed `HopHop_MCU_Nordic:nRF9151-LAxx` references to the official ID,
   checking the installed symbol's pin locations before updating cached drawings.
   The old Nordic placement mentioned above requires a separate layout migration.
3. Remove `symbols/HopHop_MCU_Nordic.kicad_sym` and its entries from both
   `sym-lib-table` files. Remove the temporary checksum assertion/nRF9151 branch
   from `validate.py`, and update its expected symbol set.
4. Rerun library validation and compare exported schematic connectivity.
   This temporary provenance note can then be removed.

## Replacement search snapshot

Compared all five custom physical symbols, both power symbols, and four custom
footprints against installed KiCad libraries `10.0.4~ubuntu24.04.1` and official
master archives retrieved on 2026-09-10. Part-number searches included package and
ordering variants; footprint candidates were checked for body size, array,
pitch, land dimensions and terminal identifiers, not just similar names.

Two close footprint candidates were rejected:

- `Package_CSP:WLCSP-4_0.64x0.64mm_Layout2x2_P0.35mm` has the same four-ball
  pitch but uses 0.21 mm copper and default mask settings, whereas the retained
  YCH footprint implements TI's preferred 0.265 mm copper / 0.2 mm mask opening.
- `Package_BGA:Texas_DSBGA-8_0.705x1.468mm_Layout2x4_P0.4mm` has the same array
  and pitch as YBG, but a different body and 0.2 mm copper versus 0.23 mm.

Neither is an exact replacement for the selected manufacturer land pattern.

| Official repository | Master revision reported at audit |
| --- | --- |
| [Symbols](https://gitlab.com/kicad/libraries/kicad-symbols/-/tree/80757d1fb319be4960c4989ca48dacc05b31f6e4) | `80757d1fb319be4960c4989ca48dacc05b31f6e4` |
| [Footprints](https://gitlab.com/kicad/libraries/kicad-footprints/-/tree/aacb3557f95ff3b55d3948f6ae34affec801ff9d) | `aacb3557f95ff3b55d3948f6ae34affec801ff9d` |
| [KLC checker](https://gitlab.com/kicad/libraries/kicad-library-utils/-/tree/90b0af91eaffcd91552027c3bfd166896f78c7de) | `90b0af91eaffcd91552027c3bfd166896f78c7de` |

Downloaded master archive SHA-256 values (archives were fetched before the revision query):

- Symbols: `1cab3316d546f44a9718307b60653901b7449cadd8abb2a95f3723f788668801`.
- Footprints: `8fd28961c00bc07fe9cba2fcc83a1088a0d9259b4092dd5c1c46a3722a72c3bd`.
