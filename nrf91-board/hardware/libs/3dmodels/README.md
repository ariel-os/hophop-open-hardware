# 3D model status

No verified models are supplied for the four custom footprints.

[KLC F9.3](https://klc.kicad.org/footprint/f9/f9.3/) explicitly requires model
references even when models do not yet exist; supplying a model is optional.
Each footprint now references a future file with its exact footprint basename:

- `${KICAD10_3DMODEL_DIR}/HopHop_Package_BGA.3dshapes/<footprint>.step`
- `${KICAD10_3DMODEL_DIR}/HopHop_Package_DFN_QFN.3dshapes/<footprint>.step`

These are documented placeholders, **not files present in the installed KiCad
libraries**. The parts will have no body in the 3D viewer until models are
provided. Scale is 1:1:1; offset and rotation are zero. Do not substitute a similar
package model without verifying dimensions and terminal orientation. The web
KLC still mentions the KiCad 9 variable; the current checker and this KiCad 10
project use `KICAD10_3DMODEL_DIR`.

The temporarily imported nRF9151 symbol uses the installed official
`Package_LGA` footprint and its upstream model reference.
