# Hardware Requirements

# DECT-2020 NR+ Development Board: Requirements & Architecture

## 1. General System Goals


1. **Open Mobile Communications:** Support development of **DECT-2020 NR+** applications (1.9 GHz) with 

   Nordic nRF9151 as the radio core.
2. **Dual-Band Connectivity:** Provide a secondary 2.4 GHz radio via Nordic nRF54 (BLE/Bluetooth 5.5) for BLE audio or other wireless protocols.
3. **Portable Use:** Operate from battery and external power (e.g. 6-48 V DC or USB-C) including solar MPP input. This allows developers to easily test a mobile mesh (power controller has USB Power Delivery and board can also charge the battery)
4. **I/O & Expansion:** Include robust audio interfaces (headset, mic, PDM mic), multiple debug and breakout connectors (SWD, SPI/UART-to-PC, Grove/UEXT/mikroBUS), and user controls (LEDs, buttons).
5. **Modular Antenna Testing:** Flexible antenna domain for on-board and external antennas, dummy loads, analyzers, and diversity tests (via jumper configuration and connectors).
6. **Open Hardware & Branding:** Board designed for development/evaluation only (will not be CE/FCC/etc.-certified). Silk-screen with **Ariel-OS** logo, "open source hardware" label, and evaluation disclaimers. Tentative color scheme: black PCB with white silkscreen and signature orange LEDs (Ariel-OS branding).

## 2. Core Processors

**nRF9151 (DECT Radio MCU):**


1. I/O: 4x antenna-select GPIOs (to Antenna Domain), I²C master (to Board Control Bus), SPI master and UART (with HW flow control) to nRF54.
2. Audio: I²S in/out (optionally routed to Audio Domain via off-by-default solder jumpers).
3. Control: COEXIST pin to nRF54 for RF coordination. Mutual reset lines between nRF9151 and nRF54.
4. Debug: SWD 10-pin "Cortex Debug" header and 6-pin Tag-Connect footprints.


**nRF54xx (Host/Peripheral MCU):**


1. Choose nRF54H20 (if available) or nRF54LM20A as alternate (USB-capable). The nRF54 provides BLE 5.5 radio, USB host/device (with PD), and application processing.
2. I/O: SPI slave and UART (to nRF9151), I²C (Board Control Bus), I²S in/out (to Audio Domain via on-by-default jumpers), COEXIST pin from nRF9151.
3. Antenna: Dedicated 2.4 GHz chip antenna on PCB.
4. Debug: SWD 10-pin header and 6-pin Tag-Connect.


**Inter-Processor Bus (Board Control Bus):**


1. **I²C bus** shared among nRF9151, nRF54, antenna control circuits, and peripherals. Enables any controller or PC interface to address components (e.g. antenna board, sensors).
2. **SPI / UART links:** Primary data exchange between nRF9151 and nRF54 via SPI (framed protocol) and optional UART. If nRF9151 is in PC-controlled mode, the nRF54 can serve as a USB-UART bridge as needed.
3. **GPIO signals:** Status or mode-selection GPIOs between MCUs (e.g. to indicate bus ownership or boot modes).

## 3. RF & Antenna Domain

**1.9 GHz Antenna (DECT-2020 NR+):**


1. **On-board Antenna:** Primary 1.9 GHz chip antenna connected to nRF9151 by default.
2. **Selectable External RF Path:** Solder jumpers break the on-board antenna line. When opened, RF can instead connect to one of a pair of RF connectors (e.g. MMCX) for external connections. This allows extensibility and improved testing possibilities, e.g. insertion of dummy loads, connection to spectrum analyzer, or connection to external antennas on a second board.
3. **Antenna Control Interface:** An 8-pin header for 4x GPIO and I²C SDA + SCL +GND + VCC) to interface with second board.
4. **Jumper-State Sensing:** Include a set of sensing jumpers or pull-ups that let the nRF9151 detect if the antenna path is set to the on-board antenna or external connectors. (E.g. tie a GPIO to GND/VCC through a jumper, with documentation clearly stating that inconsistent jumper settings can damage the board.) 
5. **2.4 GHz Antenna (BLE/Bluetooth):** Dedicated 2.4 GHz chip antenna on PCB for the nRF54's radio.
6. **RF Front-End:** Use RF-optimized and impedance matched PCB layout and connectors.

## 4. Power Domain

**Battery:**


1. Connector for one Li-ion/LiFePo₄ battery pack (e.g. 1-2 cell). The system must be able to operate from battery alone. The charge controller should allow operation without a battery if external power is present.

**External Power Inputs:**


1. **DC Input:** 6-48 V DC via a XT60 connector or robust screw terminal. Input goes through buck regulator into main power domain.
2. **Solar Input:** MPP (Maximum Power Point) tracker input for solar panels (voltage range TBD). The MPP input should supply the battery/rail through the charge controller.
3. **USB-C Power Delivery:** Full-featured USB-C port supporting PD up to TBD W. TBD: Same rating in both sink and source modes?

**Power Management & Charging:**


1. **Charge Controller:** A dedicated battery charge IC (or IC pair) that handles charging from DC/USB, battery management, and supplies 3.3 V/5 V to the nRF54 and nRF9151.
2. **USB PD Implementation:** Use PD/charger companion ICs (e.g. STUSB series or TI's PD controllers) so that USB-C negotiation does not require an extra MCU. The nRF54 should be able to query charge/bus status via I²C if possible.
3. **Power Path & Monitoring:** Include reverse-current protection and provision for a current-sense resistor (with solder jumper or connector) on the battery line for monitoring load and charge current. Consider an inrush-current limiter (e.g. series resistor + bypass MOSFET) for the DC input, to allow connection of low ESR batteries.
4. **Power Switching:** The system must safely handle plug/unplug of battery and external power. Provide indicators or logic (via nRF54) for power source status.

## 5. Audio Domain

**Headphone Output:**


1. **DAC/I²S Output:** Stereo? I²S audio from either nRF54 or nRF9151 (jumper-selectable source) feeding an audio DAC/amplifier. The amplifier must drive headphones or speakers to sufficient loudness (TBD - what output level is desired?). Include analog volume control (Potentiometer or digital via User Buttons).

**Microphone Input:**


1. **ADC/I²S Input:** Stereo or mono I²S ADC for line-level or microphone input. Support standard mic/headset jacks. Possibly use separate ADC inputs for each channel of a TRRS jack. TBD: Amplification/preamp needed.
2. **On-board PDM MIC:** Include a PDM MEMS microphone (e.g. MP34DB02) on the board. Power and data lines routed through an on-by-default solder jumper (allows hardware disable). The nRF (whichever is handling I²S) should sample this.

**Headset Connector:**


1. **TRRS Jack:** One 3.5 mm TRRS connector with mechanical detection (switch) that senses plug insertion.
2. **CTIA/OMTP Compatibility:** The design should allow use of both CTIA and OMTP headsets. This may require either two jacks or an auto-sensing switching circuit (e.g. a small IC or MCU logic). **(TBD)**.
3. **Split Jack (Optional):** Consider an optional second jack (TRS or TRRS) for headsets that separate mic and headphone. **(TBD).**
4. **PTT (Push-to-Talk):** Provide connectivity for headsets with a PTT switch. Many ham radio headsets use separate connectors. Some options:

   
   1. Kenwood standard with 3.5 mm and 2.5 mm plugs
   2. Allow USB-C SBU pins to capture PTT from digital headsets (as in some USB headsets)
   3. Route a GPIO a separate connector for external PTT.
   4. **Requirement:** At minimum, support a basic PTT line (tied to a user input on the MCU) and note the headset type expected.


11. **Analog Amplifiers:** Provide a stereo headphone amplifier with sufficient output power (power TBD). Provide a microphone preamp with appropriate bias (TBD: for what kind of microphone?) or level shifting as needed.
12. **Noise Handling:** (Future work) Explore noise cancellation or filtering for mic audio in high-echo environments. At minimum, ensure input can handle expected mic impedance and noise levels. On-board mic can capture background noise, maybe that is already sufficient.

## 6. User Interface & Debug


1. **LEDs:** 4× user-programmable LEDs. Connect by default to nRF54 GPIOs (with option via solder jumpers to connect some LEDs to nRF9151 if needed). Color: orange LED recommended.
2. **Buttons:** 4× user buttons (TBD placement: e.g. 2 front, 2 side). Connected to nRF54 (with software debounce).
3. **Boot/Reset:** One dedicated "Boot" mode button (or button combination) for selecting bootloader/firmware mode on nRF54 or nRF9151. Also ensure a means to reset each MCU (shared reset or separate).
4. **Console & Expansion Connector:** Provide a breakout to PC via Molex KK 254 (3.96 mm pitch) or similar for SPI (with dedicated CS) and UART (with flow control) lines. This connector carries I/O at 3.3 V TTL level for direct connection to e.g. Raspberry Pi or other board. Include an extra GPIO signal on this connector to coordinate bus ownership **(TBD)**.
5. **Board Control Bus (I²C):** Expose the I²C bus for external attachments (through screw terminals or header) so that a PC or external module can communicate with on-board peripherals (antenna boards, sensors, etc.). **(TBD).**
6. **Debug Access:** SWD headers as above for each MCU. Separate connectors so that both cores can be debugged independently or simultaneously.

## 7. Expansion Interfaces


1. **Grove/UEXT/mikroBUS:** Include standard expansion connectors for modular sensors and modules: Number TBD, Maybe something like this: 2× Grove ports (I²C/UART capable), 1× UEXT (I²C+UART, no shared I²C), and 1× mikroBUS (with I²C/UART/SPI + analog pin).
2. **Arduino Uno Headers (TBD):** If board space allows, include Arduino Uno-compatible headers for shields (20×2 pin header), providing 5 V/GND, SPI, I²C, and GPIO pins.
3. **nRF7002 Wi-Fi Companion:** Provide a connector or footprint for the Nordic nRF7002 Wi-Fi/BLE chip (as seen on Thingy:91X) to enable Wi-Fi location experiments. This could be a pin header carrying SPI/UART, power, and control lines.
4. **Other Breakouts:** Allow breakout of remaining GPIOs (zero-ohm-jumper-selectable between nRF9151 and nRF54). Use silk-screen labeling and maybe solder jumper/DIP select switches to assign extra pins to either core for flexibility.

## 8. Mechanical & Environmental


1. **Size & Form Factor:** Target PCB outline roughly **\~7×13 cm** so that the board stays portable.
2. **PCB Stackup:** Define (TBD) number of layers (likely 4-layer) and overall thickness (\~1.6 mm standard). Ensure copper and dielectric specs meet RF and current requirements. Stackup is TBD.
3. **Fiducials & Alignment:** Include ~~at least~~ exactly 3 reference fiducials in an asymmetric pattern for PCB fabrication alignment. Add mounting holes (size TBD, likely M3 in 4-5 locations) for securing in enclosures or test rigs. Add 2-3 tooling holes if manufacturer doesn't already place them on the panel. Diameter and placement to be coordinated with manufacturer.
4. **Enclosure Considerations:** Keep tall components (e.g. antennas, connectors) away from board edges where possible. If pogo/spring connectors are used (for RF or pogo pads), ensure mechanical support.
5. **DFM:** Stick to DFM best practices: A small excerpt: If possible, keep assembly single-sided and stick to SMT components. Keep MLCCs away from edges so they don't break from stress when the board is V-scored or the edge outline is milled. If double-sided assembly is needed keep component that can only be reflowed once at one side. Treat all heavy components (e.g. inductors) as "can only be reflowed once", because they tend to fall off in the second reflow run when upside-down.
6. **Thermal:** Ambient operating range **-30°C to +50°C**. Choose components and materials rated for this range. Ensure heat dissipation for power components if required (e.g. switchers, amplifiers).

## 9. Sourcing & Compliance


1. **Components Supply :** Where possible, ensure pin-compatibility across at least two manufacturers, document alternate part numbers in KiCad via Field Names.
2. **Open Hardware Licenses:** Mark board for evaluation/development only. Include text: *"For evaluation only - not FCC approved for resale."* Use open source hardware symbols and **Ariel-OS** logo (color and placement TBD by marketing team).
3. **Test Points:** Provide extensive test points (TPs) for power rails, critical signals (SPI, I²C, UART, clocks), and debugging. Label TPs clearly.
4. **Regulatory:** The board is for internal testing. Regulatory certification (FCC, CE) is **not** in scope.

##