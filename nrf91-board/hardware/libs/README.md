# HopHop KiCad libraries

For KiCad 10.0 or newer. The project-root tables use `${KIPRJMOD}/libs`, so no additional path config is needed when opening this project.

# Attribution

`symbols/HopHop_MCU_Nordic.kicad_sym` is an unmodified, byte-for-byte copy of `MCU_Nordic.kicad_symdir/nRF9151-LAxx.kicad_sym` from [KiCad symbols merge request !4932](https://gitlab.com/kicad/libraries/kicad-symbols/-/merge_requests/4932), “Add Nordic nRF9151 SiP”, merged 2026-09-07. This copy bridges the gap until the distributed official symbol libraries contain MCU_Nordic:nRF9151-LAxx.

The power drawings are derived from KiCad's `power:VDD`. The custom IC drawings are derived from KiCad's `Regulator_Switching:TPS63900` and `Battery_Management:BQ25173DSG`; MOSFET drawings are derived from `Transistor_FET:DMG1012T`, with P-channel polarity adapted.

Adapted and vendored symbols are distributed under KiCad's CC-BY-SA 4.0 library license with its electronic-design exception; see [LICENSE-KiCad.md](LICENSE-KiCad.md) and the [KiCad symbol libraries](https://gitlab.com/kicad/libraries/kicad-symbols).