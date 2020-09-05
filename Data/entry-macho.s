.section __DATA, __data

stdoutchar:
   .asciz "0"

.section __TEXT, __text

.globl _main
_main:
   ret

.globl printchar
printchar:
   mov %al, (%rsi)
   mov $0x2000004, %eax
   mov stdoutchar@GOTPCREL(%rip), %rsi
   mov $100, %rdx
   syscall

   ret
