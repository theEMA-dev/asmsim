# Getting Started

## Interface Overview

ASMsim's interface is divided into several key areas:

#### Code Editor
- Write your MIPS assembly code here
- Error handling on entry
- Loading on entry
- **Load File**: Load external file into ASMsim
- **Step**: Steps the program into next line, increments program counter
- **Run**: Runs the program, shows the final result on all panels

#### Machine Code View
- Translates users code into Binary Or Hexadecimal
- Translates on-entry
- Can switch between Binary or Hex on the fly

#### Register View
- Shows current values of all 32 MIPS registers
- Updates in real-time during simulation

#### Memory View
- Displays memory contents in binary or hexadecimal
- Organized in word-aligned addresses
- Scrollable for viewing different memory regions

## Basic Workflow

1. Type or load your MIPS code in the editor
2. See any syntax or other errors real-time at entry
3. Use "Run" or "Step" to execute
4. Monitor registers and memory changes
5. Use "Reset" to start over

## Understanding Output

### Console Output (Machine Code View)
- Shows any errors and line numbers if possible
- Checks for registers and memory locations
- Prints output from syscall instructions if anything in your code is problematic

### Status Bar
- Current Program Counter
- Program Status
- Operation Code and Function Code
- $rs, $rt and $rd registers to use on next instruction

## Next Steps

For detailed instruction usage, see the [Usage Guide](usage.md).  
For installation instructions, refer to the [Installation Guide](installation.md).