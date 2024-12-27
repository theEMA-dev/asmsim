# ASMsim: 32-bit MIPS Assembly Simulator

![Banner](img/banner.png)

ASMsim is a real-time simulator for 32-bit MIPS assembly code, developed as an educational tool to help students learn and understand MIPS assembly programming.

## Features

- Real-time assembly simulation
- Intuitive graphical user interface
- Step-by-step execution
- Register and memory monitoring
- Cross-platform support (Windows, macOS, Linux)

## Download

Get the latest version from the [Releases](https://github.com/username/asmsim/releases) page:

- Windows: `ASMsim-win-x64.zip`
- macOS: `ASMsim-macos.dmg`
- Linux: `ASMsim-linux.tar.gz`

## Building from Source

### Prerequisites

- Python 3.8 or newer
- Git
- Visual Studio Build Tools (Windows only)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/username/asmsim.git
cd asmsim
```
2. Compile from source files:
```bash
.\venv\Scripts\activate
pyinstaller --clean asmsim.spec
```
