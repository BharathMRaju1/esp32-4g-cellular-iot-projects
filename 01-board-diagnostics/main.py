import os
import gc
import esp
import machine

print("=" * 40)
print(" GRIDBox-4G Board Diagnostics")
print("=" * 40)

info = os.uname()

print("Board        :", info.machine)
print("Chip         :", info.sysname)
print("Firmware     :", info.release)
print("Version      :", info.version)

print()

print("CPU Frequency:", machine.freq() // 1000000, "MHz")
print("Flash Size   :", esp.flash_size() // (1024 * 1024), "MB")
print("Free RAM     :", gc.mem_free(), "Bytes")

print()

print("Reset Cause  :", machine.reset_cause())
print("Wake Reason  :", machine.wake_reason())

print("=" * 40)