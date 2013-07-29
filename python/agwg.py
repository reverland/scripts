#! /bin/env python
# -*- coding: utf-8 -*-

import os
import re
import random


def parse(lines, reg, dg):
    new_lines = []
    for line in lines:
        new_lines += xor_match(line, reg, dg)
    return new_lines


def xor_match(directive, reg, dg, iteration=2):
    """Too much iteration may cause jmp false immediate overflow :i8 0c4h """
    m = re.search(r'xor\s+' + reg + ',\s*' + reg, directive)
    ins = dg.method
    if m:
        new_directive = []
        for i in range(iteration):
            i = random.randrange(0, len(ins))
            if ins[i] == 'push_pop':
                new_directive += dg.push_pop(reg)
            elif ins[i] == 'mov_to_reg':
                new_directive += dg.mov_to_reg(reg)
            elif ins[i] == 'save_other_reg':
                new_directive += dg.save_other_reg(reg)
            elif ins[i] == 'inc_reg':
                new_directive += dg.save_other_reg(reg)
            elif ins[i] == 'dec_reg':
                new_directive += dg.save_other_reg(reg)
            else:
                pass
        new_directive += [directive]
    else:
        new_directive = [directive]
    return new_directive


class DG(object):
    """generate instructions"""
    def __init__(self):
        super(DG, self).__init__()
        self.regs = ["eax", "ebx", "ecx", "edx", "esi", "edi"]
        self.method = ["push_pop", "mov_to_reg", "save_other_reg", "inc_reg", "dec_reg"]

    def push_pop(self, reg):
        directive = [
            "    push " + reg + '\n',
            "    pop " + reg + '\n']
        return directive

    def mov_to_reg(self, reg):
        i = random.randrange(0, len(self.regs))
        if self.regs[i] != reg:
            directive = ["    mov " + reg + ', ' + self.regs[i] + '\n']
        else:
            directive = self.mov_to_reg(reg)
        return directive

    def save_other_reg(self, reg):
        i = random.randrange(0, 5)
        if self.regs[i] != reg:
            directive = [
                "    mov " + reg + ', ' + self.regs[i] + '\n',  # move some random reg into reg
                "    xor " + self.regs[i] + ", " + self.regs[i] + '\n',  # zero out reg
                "    mov " + self.regs[i] + ', ' + reg + '\n']
        else:
            directive = self.save_other_reg(reg)
        return directive

    def inc(self, reg):
        directive = "    inc " + reg + '\n'
        return [directive]

    def dec(self, reg):
        directive = "    dec " + reg + '\n'
        return [directive]


if __name__ == "__main__":
    filename = os.sys.argv[1]
    with open(filename, 'rb') as f:
        lines = f.readlines()
    dg = DG()
    # Iterate lines for specific reg
    new_lines = lines
    for reg in dg.regs:
        new_lines = parse(new_lines, reg, dg)
    # Once you’ve finished mangling your ASM code you need to add the following two lines to the top of
    # the file for it to build correctly.
    new_lines = [
        ".section '.text' rwx\n",
        ".entrypoint\n"] + new_lines
    with open(filename.split('.')[0] + "_gw." + filename.split('.')[-1], 'wb') as f:
        f.writelines(new_lines)
