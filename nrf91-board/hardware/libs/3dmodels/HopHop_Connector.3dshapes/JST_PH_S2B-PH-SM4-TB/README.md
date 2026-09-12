# JST PH S2B-PH-SM4-TB 3D model

Source: Mark Harris / [Celestial Altium Library](https://github.com/issus/altium-library), [`STEP/Connector/JST S2B-PH-SM4-TB.step`](https://github.com/issus/altium-library/blob/master/STEP/Connector/JST%20S2B-PH-SM4-TB.step).

Downloaded 2026-09-13. `S2B-PH-SM4-TB.step` is an unmodified copy, renamed locally. SHA-256: `9959e29738dab7ee2829e57e1514b79362d208ea8e79bf8930cc476d121c4cc8`. Its usage terms are reproduced in [LICENSE.md](LICENSE.md). Attribution does not imply endorsement.

Used by J202 and the project footprint `HopHop_Connector:JST_PH_S2B-PH-SM4-TB_1x02-1MP_P2.00mm_Horizontal`. The model is embedded in both the PCB and local footprint as `kicad-embed://S2B-PH-SM4-TB.step`, requiring no external model path configuration. The STEP file here is the original source copy.

KiCad model transform: unit scale, zero rotation, offset **(0, -1.4, 0) mm**. This puts the solder contact bottoms at the PCB surface and aligns the housing with the footprint's F.Fab outline. In model coordinates after translation, signal contact feet are at X = ±1 mm, Y = 2.2–4.2 mm; mounting feet are at X = ±3.25 mm, Y = -4.41–-1.50 mm. All four contact faces lie within their corresponding footprint pads (KiCad PCB Y is inverted relative to model Y).

Validated by importing the STEP geometry, checking contact bounds against pads, rendering the connector in KiCad, and exporting J202 from the actual board to STEP. The downloaded model geometry was not edited.
