#!/usr/bin/env python3
# -*- coding: utf8 -*-

# Scrolling output of paconky by MaxKh

import os


size = 37
printed = 0

home = os.path.expanduser("~")
packets_path = os.path.join(home, ".cache/packets")
step_path = os.path.join(home, ".cache/step")

try:
    f_pack = open(packets_path, "r")
except:
    if os.path.isfile(step_path):
        os.remove(step_path)
    exit()

try:
    f_step = open(step_path, "r")
    step = int(f_step.readline())
    f_step.close()
except:
    step = 0

packets = f_pack.readlines()
f_pack.close()
num_packets = len(packets)

if num_packets <= size:
    step = 0

for p in packets[step:step+size]:
    print(p, end = '')
    printed += 1

if step+size > num_packets and size < num_packets:
    for p in packets[0:step+size-num_packets]:
        print(p, end = '')
        printed += 1

step = 0 if (step == num_packets or size >= num_packets)  else step+1

f_step = open(step_path, "w+")
f_step.write(str(step))
f_step.close()

while printed < size:
    print("\n")
    printed += 1
