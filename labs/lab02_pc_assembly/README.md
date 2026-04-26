# Lab 2 – Understand How PC Components Are Connected; Assembling System Components

## Objective
Understand the physical and logical connections between PC components, then assemble a complete system inside the simulator.

## Theory

### System Buses
A bus is a shared communication path. The 8086/PC architecture defines three buses:

| Bus | Width | Purpose |
|-----|-------|---------|
| Address Bus | 20-bit (8086) | CPU sends memory addresses |
| Data Bus | 16-bit (8086) | Bidirectional data transfer |
| Control Bus | Variable | Read/Write signals, interrupts, DMA |

The address bus width determines the maximum addressable memory:
- 20-bit → 2²⁰ = 1 MB (8086 real mode)
- 32-bit → 4 GB (80386+)

### Component Connections
```
        ┌─────────────┐
        │     CPU     │
        │  (8086)     │
        └──────┬──────┘
      Address/Data/Control Bus
       ┌───────┼────────┐
       ▼       ▼        ▼
   ┌──────┐ ┌──────┐ ┌──────┐
   │  RAM │ │  ROM │ │  I/O │
   │      │ │ BIOS │ │ Ctrl │
   └──────┘ └──────┘ └──────┘
```

### Assembly Order (Physical)
1. Mount CPU in socket (match pin 1 marker)
2. Seat RAM sticks in DIMM slots
3. Connect power supply (ATX 24-pin + CPU 8-pin)
4. Install GPU in PCIe x16 slot
5. Connect storage via SATA / M.2
6. Route front-panel headers (power button, reset, USB)
7. Connect I/O peripherals

### Key Assembly Notes
- **CPU socket** – Modern boards use ZIF (Zero Insertion Force) sockets; lower the retention lever, drop the CPU in without pressing, then lock. Forcing risks bent pins.
- **Heat sink** – Mount directly on top of CPU after applying a pea-sized dot of thermal paste; attach the fan power connector to the CPU_FAN header on the motherboard.
- **Motherboard seating** – Stand the board vertically in the tower, align I/O shield, and fasten standoff screws from the back of the PCB.
- **PSU placement** – Fits at the top-rear of the case; secure with four screws; route 24-pin ATX, 8-pin CPU, and any drive Molex/SATA power leads before closing cables.
- **Drive installation** – Mount optical and hard drives in front bays; use SATA cable + SATA power for modern drives, IDE ribbon + Molex for legacy PATA devices; configure master/slave jumpers on PATA.
- **Expansion cards** – Match card to correct slot (PCIe x16 for GPU, PCIe x1 / PCI for smaller cards); press firmly until the slot latch clicks.
- **RAM alignment** – Align the notch on the DIMM to the slot key, press down evenly until both side retention tabs click into place.

## Simulator Walkthrough

```bash
bash start-pcbuilder.sh
# open http://localhost:6080/vnc.html
```

Follow the in-game build guide:
1. Select a compatible motherboard and CPU.
2. Match RAM type (DDR4/DDR5) to the board specification.
3. Install each component in the correct slot.
4. Power on – the simulator validates connections and reports errors.

## Lab Tasks
1. List every cable/connector used and what it carries (power, data, control).
2. Identify which components share the same bus segment.
3. Record what happens if RAM is placed in the wrong slot.
4. Draw a connection diagram for the system you assembled.

## Questions
1. What is the difference between the address bus and the data bus?
2. Why must the CPU and RAM have matching bus speeds?
3. What does DMA (Direct Memory Access) allow, and why is it useful?
4. What is the function of the BIOS/UEFI during the boot sequence?
