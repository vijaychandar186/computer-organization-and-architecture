# Lab 1 – Recognize Various Components of a PC

## Objective
Identify and describe the role of the main hardware components inside a personal computer, categorised into Input/Output systems, Processing units, and Memory units.

## Theory

### Processing Unit
| Component | Function |
|-----------|----------|
| CPU (Central Processing Unit) | Executes instructions; contains ALU, Control Unit, and registers |
| ALU (Arithmetic Logic Unit) | Performs arithmetic (+, −, ×, ÷) and logical (AND, OR, NOT) operations |
| Control Unit | Fetches, decodes, and coordinates execution of instructions |
| Registers | Ultra-fast on-chip storage (AX, BX, CX, DX, IP, FLAGS on 8086) |

### Memory Units
| Component | Type | Volatile? | Purpose |
|-----------|------|-----------|---------|
| Cache (L1/L2/L3) | SRAM | Yes | Bridge between CPU registers and RAM |
| RAM | DRAM | Yes | Working memory for running programs |
| ROM / BIOS | Flash | No | Firmware, boot code |
| Hard Disk / SSD | Magnetic / Flash | No | Persistent mass storage |

### Input/Output Systems
| Component | Direction | Examples |
|-----------|-----------|---------|
| Input devices | → CPU | Keyboard, mouse, microphone, scanner |
| Output devices | CPU → | Monitor, printer, speakers |
| I/O controllers | Bridge | USB controller, NIC, GPU |
| NIC (Network Interface Card) | Bridge | Wired Ethernet adapter; operates at OSI layers 1–2; connects via PCI/PCIe slot |
| Wireless NIC (WNIC) | Bridge | Wi-Fi / Bluetooth adapter; uses antenna instead of cable; also layers 1–2 |
| Optical Drive | I/O | Reads/writes CDs, DVDs, Blu-ray via laser; burner models can write once (R) or rewrite (RW) |
| Floppy Disk Drive (FDD) | I/O | Legacy magnetic removable storage; ~1.44 MB capacity; largely obsolete |

### Power and Cooling
| Component | Function |
|-----------|----------|
| PSU (Power Supply Unit) | Converts AC mains to regulated DC rails (+12 V, +5 V, +3.3 V); most desktops use ATX standard; always supplies 5 VSB standby when plugged in |
| Heat Sink + Fan (HSF) | Active CPU cooling: heat sink (passive fin array) conducts heat from die; attached fan forces airflow over fins |

### Storage Interfaces
| Interface | Type | Max Bandwidth | Typical Use |
|-----------|------|---------------|-------------|
| SATA (Serial ATA) | Serial point-to-point | ~600 MB/s (SATA III) | Modern HDD, SSD, optical drives |
| PATA (Parallel ATA / IDE) | Parallel ribbon cable | ~133 MB/s (UDMA/133) | Legacy HDD and optical drives; retroactively renamed from ATA when SATA emerged |

## PC Building Simulator
Labs 1, 2, and 3 use the **PC Building Simulator** included in this repository.

Start it with:
```bash
bash start-pcbuilder.sh
# then open http://localhost:6080/vnc.html
```

## Lab Tasks
1. Launch the simulator and identify every component on the main board view.
2. Hover over each part and record its name and category (Input / Output / Processing / Memory).
3. Note the data bus width and clock speed shown for the CPU.
4. Sketch a block diagram showing how CPU, RAM, and I/O are interconnected via the system bus.

## Questions
1. What is the difference between volatile and non-volatile memory?
2. Where does the CPU store intermediate results during a calculation?
3. Why is cache memory faster than main RAM?
4. What is the role of the northbridge/southbridge in a traditional chipset?
