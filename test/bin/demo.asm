# Test file for MIPS instruction formats
# R-Format Tests
test_r_format:
  # Test add
  addi $s0, $zero, 5    # s0 = 5
  addi $s1, $zero, 3    # s1 = 3
  add $s2, $s0, $s1     # s2 should be 8

  # Test sub
  sub $s3, $s0, $s1     # s3 should be 2

  # Test and
  addi $s0, $zero, 12   # s0 = 1100
  addi $s1, $zero, 10   # s1 = 1010
  and $s4, $s0, $s1     # s4 should be 8 (1000)

  # Test or
  or $s5, $s0, $s1      # s5 should be 14 (1110)

  # Test slt
  slt $s6, $s1, $s0     # s6 should be 1 (10 < 12)

  # Test shifts
  addi $s0, $zero, 8    # s0 = 8
  sll $s7, $s0, 2       # s7 should be 32
  srl $t0, $s7, 1       # t0 should be 16

# I-Format Tests
i_format_test:
  # Test addi
  addi $t1, $zero, 100  # t1 = 100

  # Test load/store
  sw $t1, 0($sp)        # Store 100 at stack pointer
  lw $t2, 0($sp)        # Load it back to t2

  # Test branches
  addi $t3, $zero, 5
  addi $t4, $zero, 5
  beq $t3, $t4, branch_target  # Should branch
  bne $t3, $t4, branch_skip    # Should not branch

branch_target:
  addi $t5, $zero, 1    # t5 = 1
  j j_format_test       # Jump to J-Format tests

branch_skip:
  addi $t6, $zero, 2    # t6 = 2

# J-Format Tests
j_format_test:
  j end        # Jump to target
  addi $t7, $zero, 1    # Should skip

end:
  addi $t8, $zero, 20   # t8 = 20