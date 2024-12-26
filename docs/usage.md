# Usage Guide

## Supported Instructions

ASMsim supports the following MIPS32 instructions:

### R-Format Instructions
- `add $rd, $rs, $rt` - Add registers
- `sub $rd, $rs, $rt` - Subtract registers
- `and $rd, $rs, $rt` - Bitwise AND
- `or $rd, $rs, $rt` - Bitwise OR
- `slt $rd, $rs, $rt` - Set less than
- `sll $rd, $rt, shamt` - Shift left logical
- `srl $rd, $rt, shamt` - Shift right logical
- `jr $rs` - Jump register

### I-Format Instructions
- `addi $rt, $rs, imm` - Add immediate
- `lw $rt, offset($rs)` - Load word
- `sw $rt, offset($rs)` - Store word
- `beq $rs, $rt, label` - Branch if equal
- `bne $rs, $rt, label` - Branch if not equal

### J-Format Instructions
- `j label` - Jump
- `jal label` - Jump and link

## Program Features

### Code Editor
- Syntax highlighting
- Real-time error checking
- Line numbers
- File loading support

### Code Execution
1. **Step Mode**: Execute one instruction at a time
   - Shows current instruction
   - Updates registers and memory
   - Displays PC counter

2. **Run Mode**: Execute entire program
   - Runs to completion
   - Shows final state
   - Displays execution status

### Memory View
- Instruction memory display
- Data memory display
- Word-aligned addressing
- Binary/Hex display options

### Register View
- All 32 MIPS registers
- Real-time value updates
- Register naming conventions

## Code Examples

### Basic Arithmetic
```mips
# Add two numbers
addi $s0, $zero, 5    # s0 = 5
addi $s1, $zero, 3    # s1 = 3
add $s2, $s0, $s1     # s2 = 8
```

### Memory Operation
```mips
# Store and load a number
addi $t0, $zero, 100  # t0 = 100
sw $t0, 0($sp)        # Store 100 at stack pointer
lw $t1, 0($sp)        # Load value into t1
```

### Branching
```mips
# Branch example
addi $t0, $zero, 5
addi $t1, $zero, 5
beq $t0, $t1, equal    # Branch if t0 = t1
j exit
equal: 
  addi $t2, $zero, 1
exit:  
```