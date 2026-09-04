# 3D models

No project-owned STEP, STP, or WRL files existed in the original library directories.
The two MOSFET footprints incorrectly referenced a system TI PicoStar model; that
reference was removed because the actual package is Diodes X2-DFN0806-3.

Verified models for X2-DFN0806-3, YCJ0012-C02, YBG0008-C01, and YCH0004 are not
included. Footprints intentionally have no model links until matching models are
available. This is an outstanding KLC F9.3 checker finding.

Place future models here and use `${HOPHOP_LIB_DIR}/3dmodels/<filename>.step`
in footprint model paths for global-library use. Set HOPHOP_LIB_DIR as described
in the library README. Include model source, provenance and licensing when adding
models; do not substitute a different package merely to obtain a 3D preview.
