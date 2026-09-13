# HopHop KiCad libraries

For KiCad 10.0 or newer. The project-root tables use `${KIPRJMOD}/libs`, so no additional path config is needed when opening this project.

# Attribution

The project-local `JST_PH_S2B-PH-SM4-TB_1x02-1MP_P2.00mm_Horizontal` footprint is copied from KiCad's `Connector_JST` library, with its 3D model path and offset adapted. Its geometry remains under the KiCad library license below. The matching STEP model comes from Mark Harris's Celestial Altium Library; see its [source, alignment and separate license](3dmodels/HopHop_Connector.3dshapes/JST_PH_S2B-PH-SM4-TB/README.md).

`symbols/HopHop_MCU_Nordic.kicad_sym` is an unmodified, byte-for-byte copy of `MCU_Nordic.kicad_symdir/nRF9151-LAxx.kicad_sym` from [KiCad symbols merge request !4932](https://gitlab.com/kicad/libraries/kicad-symbols/-/merge_requests/4932), “Add Nordic nRF9151 SiP”, merged 2026-09-07. This copy bridges the gap until the distributed official symbol libraries contain MCU_Nordic:nRF9151-LAxx.

The power drawings are derived from KiCad's `power:VDD`. The custom IC drawings are derived from KiCad's `Regulator_Switching:TPS63900` and `Battery_Management:BQ25173DSG`; MOSFET drawings are derived from `Transistor_FET:DMG1012T`, with P-channel polarity adapted.

Adapted and vendored symbols are distributed under KiCad's CC-BY-SA 4.0 library license with its electronic-design exception; see [LICENSE-KiCad.md](LICENSE-KiCad.md) and the [KiCad symbol libraries](https://gitlab.com/kicad/libraries/kicad-symbols).

The project-local `HopHop_LED:LED_Kingbright_APTF1616LSEEZGKQBKC` footprint is drawn from Kingbright's recommended soldering pattern, with its top view rotated 180 degrees and the original electrical pin numbering retained. See [component selection and pinout verification](../component-selection-notes.md).

`HopHop_Package_SON:Texas_DPY0002A_0.6x1mm_P0.65mm` is a project-local copy of KiCad's `Package_SON` footprint for editing the pin 1 marker. It is covered by the KiCad library license linked above.
