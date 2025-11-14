Components
==========

Note that this is an early design sketch:
Most components are up for discussion if they prove to be overly complicated or costly;
alternative suggestions are always welcome.

Can we fit this in about 7x13cm?

Main cores
----------

* nRF9151, with DECT radio core firmware flashed on before shipping
  * Antenna, 4x antenna selector GPIO and I2C master routed to Antenna domain
  * SPI master and UART with HW flow control to nRF54

    UART may not technically be necessary because we can frame SPI as we like,
    but it can be convenient for some development scenarios.

  * I2S bi-directional (plus any GPIO we need there) routed to audio domain with off-by-default solder jumpers.

  * Co-exist pin to nRF54
  * SWD 10-pin header and 6-pin Tag-Connect

  * Any pins needed for the Peripherals group.

* nRF54H20 (or nRF54LM20A, if H20 is not available?)
  * SPI slave and UART to 9151
  * Co-exist from nRF9151
  * The full set of USB connectivity, including PD (but see also Power domain)
  * SWD 10-pin header and 6-pin Tag-Connect

  * I2S bi-directional (plus any GPIO we need there) routed to audio domain with on-by-default solder jumpers.

  * 2.4GHz chip antenna

  * Any pins needed for the Peripherals group.

* Mutual RST connections.

TBD:
We might also want some minimal connectivity between the nRF54 and the nRF91
when the latter is mostly wired into a PC --
even if it's just so the 91 can tell the 54 that it's under PC control now,
or to relay data to non-solder-jumpered peripherals.
(Or would those just be under the nRF54's and thus USB control, viewe by the host as separate from the SPI parts?)
Maybe the I2C to the antenna could also be wired to the nRF54, which can then also inspect the antennas?

Antenna domain
--------------

* Direct line to 1.9GHz chip antenna,
  broken only by on-by-default solder jumpers.
* Solder jumpers allow diverting the signal into a pair of (spring-loaded?) connectors instead.

  When switched to this configuration,
  it provides several options to be explored later:

  * A dummy load between the two connectors can be inserted into the transmit path to emulate obstacles when doing testing between nodes in physical proximity.
  * The signal from the chip can be fed into a spectrum analyzer;
    in this configuration, the channel back into the antenna is unused.
  * Antenna diversity can be explored:
    The 2nd board can contain more directional antennas
    or antennas for different bands,
    with an antenna selector (up to 4 channels) feeding into those and/or back into the main antenna.

* Screw terminals that allow any of the above to be put in place on the board,
  rather than setting up flimsy wires.

* 4 GPIOs and one I2C (plus GND/VCC) for antenna selection and metadata.

  These could be connected by an 8-pin IDC block, or anything that works both for screw-on daughter boards
  and for wiring up the external antenna components separately.

  The purpose of the I2C is to allow having a cheap simple I2C storage component on the radio boards,
  which then tell the radio MCU which antenna selection options are available,
  and which antennas are connected.

Ideally, I'd like to sense on the radio MCU whether or not the solder bridges are configured this or that way,
so that a situation of the bridges set to external connection but no external board being present can be detected.
Without some genius idea,
this could just as well be one more set of solder bridges taking a GPIO to GND or VCC,
with strict instructions to only change all three solder bridges or risk damage to the radio.

Peripherals
-----------

* Break-out of the nRF91 SPI bus (on a dedicated CS) and UART with HW flow control (ideally separate, otherwise shared with protection against nRF54 and external sending at the same time) line at 3.3V level.

  Which connectors do we best pick to go into a SPI and UART capable Linux system such as a RasPi?
  
* Break-out connectors.

  If we have pins to spare, solder-jumpered between nRF91 and nRF54 (defaulting to the latter),
  otherwise only nRF54.
  Assigning to different pins is preferred, but if they share an SPI or I2C bus, that's OK too.

  * 2x Grove
  * 1x UEXT (don't share I2C, those are often also used as GPIO)
  * 1x mikroBUS (especially the analog pin is really best-effort)

  We could also consider Arduino shield, feather modules, but at some point it gets too much.
  What are your favorite form factors?

* "The usual buttons and LEDs":
  all connected to the nRF54,
  optionally (LEDs via solder jumpers) to the nRF54 core
  (TBD: Really the nRF54? Those might make sense on the nRF91 as well, because they make sense even when connected to a PC; not sure what's best here.)

  * 4 user LEDs
  * 4 user buttons

    TBD: front? edge? 2 front, 2 edge?

  * Boot mode button (or buttons? TBD; Need to look into bootloader plans)

Audio domain
------------

* DAC from I2S, output strong enough to drive headphones.

  TBD: Stereo? Probably that's in all chips anyway.

* ADC into I2S, suitable for headsets.

  TBD: Do we need to do any gain control?

* 3.5mm TRRS connector, with insertion detection

  TBD: Theose have different pinouts used in different environments (CTIA vs. OMTP);
  can we cater for both, if so, how do we route it,
  and can we auto-detect it?

  TBD: Should we have another TRS to have split mic/phone headsets, are they still a thing?

TBD: There are headsets with PTT; how is that signalled?

TBD: Do we want to add PDM, typically from an on-board microphone?

Power domain
------------

* Connector to Li(Fe?)Po battery

* Power inputs
  (not sure if best going into main power domain, or if fed into charge controller;
  if the latter, can this still run without a battery connected?)

  * 6-48V DC input ("works with any power adapter you may have lying around"). Screw terminal?

  * MPP tracker to connect solar modules.

* Charge controller 

  * Managing battery

  * Providing VCC to nRF54 and nRF91

  * Sending and receiving power via USB-C. Up to … TBD, maybe 500mA?

  TBD:
  Are charge controllers that do bi-directional USB generally taking the PD lines?
  (In which case: can we get some information about SoC, and control, back into the nRF54?)
  Or do they need an MCU to talk PD and tell the charge controller?
  The former would be preferred.

Other features
--------------

Many test points don't hurt.

This is an evaluation and testing tool.
Other similar boards have labels such as "For evaluation only; not FCC approved for resale".

Open questions
--------------

This is all a lot of solder jumpers going to either nRF core.
Is this practical?
Alternatives:

* Just route it to the nRF54.

  There will be users who want to do as much as possible on the nRF91,
  but those may just need to limit themselves to fewer hardware options.

* If there's a cheap many-pin component that can do fan-out pins that don't need tri-stating or bidirectionality
  (LEDs, MOSI, TX; buttons and RX/MISO don't need jumpering necessarily),
  it might be an option to switch them all through this.

We should check if the Thingy:91X has anything cool that we'd like to have too,
especially on MCU-MCU connections.
