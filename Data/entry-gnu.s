.data

stdoutchar:
   .asciz "0"

.text

.globl main
main:
   ret

.globl printchar
printchar:
   mov stdoutchar@GOTPCREL(%rip), %rsi
   mov %al, (%rsi)
   mov $1, %rax
   syscall

   ret
