# Lab 3 – Understand PC Components; Disassembling System Components

## Objective
Practise safe disassembly of a PC, identify each component on removal, and record its specifications.

## Safety and ESD Precautions
- Power off and unplug before opening the case.
- Wear an anti-static wrist strap connected to chassis ground.
- Handle PCBs by the edges; avoid touching gold contacts.
- Place components on an anti-static mat.

## Disassembly Order
Disassemble in the reverse of the assembly sequence:

1. Disconnect all peripherals and power.
2. Remove the side panel.
3. Unplug power connectors from components.
4. Remove GPU (release PCIe slot latch).
5. Remove storage drives (unscrew + disconnect SATA/M.2).
6. Remove RAM (press retention clips, lift straight out).
7. Remove CPU cooler (unscrew/unclip, clean thermal paste).
8. Remove CPU from socket (lift retention lever, lift chip vertically).
9. Remove motherboard standoff screws and lift board out.

### Component-Specific Notes

**Side panel** – Undo rear screws, slide panel toward the back ~1 inch, then lift off. Panel type varies by case design.

**Expansion cards** – Check for attached cables before unscrewing the bracket. Grip the card by its front and rear edges; rock it gently lengthwise to release from the slot.

**Storage drives** – Two power connector types may be present:
- *Molex* (large 4-pin): wiggle gently side-to-side while pulling outward.
- *Berg* (small 4-pin, floppy): pull straight out; some have a small locking tab requiring a flat-head screwdriver lift.

  Data cables: SATA connectors have a L-shaped latch — press the tab and pull straight back. IDE/PATA ribbon connectors have no latch; wiggle carefully sideways to avoid bending pins on the drive header.

**PSU** – Remove all internal power connectors (motherboard 24-pin, CPU 8-pin, drive leads, front-panel power) before unscrewing the four rear-panel screws.

**CPU cooler + CPU** – Unscrew or unclip the cooler; clean old thermal paste with isopropyl alcohol. Lift the ZIF socket retention lever, then lift the CPU straight up — no lateral force needed.

**Motherboard** – Disconnect all remaining headers before unscrewing standoffs. Note connector positions (or photograph) before removal for reassembly reference.

## Identification Checklist

| Component | Marking to Read | Information It Contains |
|-----------|----------------|------------------------|
| CPU | Top label | Manufacturer, model, core count, TDP, socket type |
| RAM | Side label | Capacity (GB), type (DDR4), speed (MHz), CAS latency |
| Motherboard | PCB silkscreen | Socket, chipset, DIMM slot count, PCIe version |
| GPU | Heatsink label | Model, VRAM size, VRAM type |
| Storage | Top sticker | Capacity, interface (SATA/NVMe), RPM (HDD) |
| PSU | Side label | Wattage, efficiency rating, rail outputs |

## Simulator Walkthrough

```bash
bash start-pcbuilder.sh
# open http://localhost:6080/vnc.html
```

Use the in-game disassembly mode:
1. Click on each component to select it.
2. Follow the on-screen prompt to unscrew or unclip.
3. Drag the component to the parts tray.
4. Read the spec card that appears on removal.

## Lab Tasks
1. Record the specifications of every component removed.
2. Identify the socket type used by the CPU and list one compatible alternative CPU.
3. Determine the maximum RAM capacity the motherboard supports.
4. Note which components share the PCIe bus and which use USB.

## Questions
1. Why must the CPU cooler be removed before the CPU?
2. What damage can ESD cause, and why is it invisible to the eye?
3. What does the wattage rating on a PSU represent?
4. How would you determine whether two RAM sticks are compatible with each other?
