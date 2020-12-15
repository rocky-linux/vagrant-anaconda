# Kdump configuration common methods
#
# Copyright (C) 2014 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#
# Red Hat Author(s): David Shea <dshea@redhat.com>
#
import re
__all__ = ["getReservedMemory", "getTotalMemory", "getMemoryBounds"]

import blivet.arch

_reservedMemory = None
def getReservedMemory():
    """Return the amount of memory currently reserved for kdump in MB."""
    global _reservedMemory

    # Check if the value has already been read
    if _reservedMemory is not None:
        return _reservedMemory

    try:
        with open("/sys/kernel/kexec_crash_size", "r") as fobj:
            _reservedMemory = int(fobj.read()) / (1024*1024)
            return _reservedMemory
    except (ValueError, IOError):
        return 0

def getTotalMemory():
    """Return the total amount of system memory in MB

       This is the amount reported by /proc/meminfo plus the aount
       currently reserved for kdump.
    """
    memkb = 0
    fd = open('/proc/meminfo').read()
    matched = re.search(r'^MemTotal:\s+(\d+)', fd)
    if matched:
        memkb = int(matched.groups()[0])

    # total_memory return memory in KB, convert to MB
    availMem = memkb / 1024

    return availMem + getReservedMemory()

def getMemoryBounds():
    """Return a tuple of (lower, upper, step) for kdump reservation limits.

       If there is not enough memory available to use kdump, both lower and
       upper will be 0.
    """

    totalMemory = getTotalMemory()
    arch = blivet.arch.get_arch()

    if arch.startswith('ppc64'):
        lowerBound = 384
        minUsable = 1024
        step = 1
    elif arch == 'aarch64':
        lowerBound = 512
        minUsable = 512
        step = 1
    else:
        lowerBound = 160
        minUsable = 512
        step = 1

    upperBound = (totalMemory - minUsable) - (totalMemory % step)

    if upperBound < lowerBound:
        upperBound = lowerBound = 0

    return (lowerBound, upperBound, step)
