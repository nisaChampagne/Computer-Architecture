#!/usr/bin/env python3

"""Main."""

import sys
from cpuREVISED import CPU

cpu = CPU()

cpu.load(sys.argv[1])
cpu.run()