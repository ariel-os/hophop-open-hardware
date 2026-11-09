Grasshopper Nymph
=================

Summary
-------

This is a small development board for using hophop.
It fits in 21x56mm, and can be used standalone,
or with optional pin headers,
or soldered onto a larger PCB on account of being populted only on one side.

Components
----------

Hardware is described in [`./hardware/`](./hardware/).

A laser cut wooden encasing is described in [`./layered-case/`](./layered-case/).

Software is under development.

Lineage
-------

This board is mostly a clone of the [makerdiary nRF9151 Connect Kit](https://makerdiary.com/products/nrf9151-connectkit):
It uses the same pinout and the same major components.

For practical purposes, it differs by:

* the choice of battery connector, going with the more popular JST-PH.
* removing all components that are irrelevant or unusable when using the DECT firmware
  (no SIM slot, no GPS antenna connector)
* having an extra yellow LED on nRF9151 (P0.10, also part of the edge connectors),
  in order to simplify demos and functionality checks.

License
-------

As the schematics of this board are derived from the [makerdiary nRF9151 Connect Kit](https://makerdiary.com/products/nrf9151-connectkit).

Therefore, for the schematics and the full PCB, the applicable license statement is:

* These documents are licensed by Makerdiary and the hophop contributers under the terms of [Creative Commons Attribution Share-Alike License (ver. 4)](https://creativecommons.org/licenses/by-sa/4.0/).

For the individual components (such as custom part drawings and concrete layouting) and all parts not derived from the schematic (such as documentation in this repositry or the cases), the applicable license statement is:

* Published by the hophop contributors under the terms of  [CERN-OHL-P-2.0](https://ohwr.org/cern_ohl_p_v2.pdf).
