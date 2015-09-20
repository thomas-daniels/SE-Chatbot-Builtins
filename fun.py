#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from Module import Command
import random
from . import upsidedown


eyes = ['°', '゜', 'ಥ', "'", '•', '^', '⇀', 'ಠ', '๑']
mouths = ['□', 'Д', '益', 'ᴥ', '.', 'ʖ', 'ل͜', '³', 'ਊ']
arms = ['╯', 'ง', '┛', 'づ']


def exec_flip(cmd, bot, args, msg, event):
    global eyes
    global mouths
    if len(args) == 0:
        return 'Not enough arguments'
    left_eye = random.choice(eyes)
    right_eye = random.choice(eyes + [left_eye] * 20)
    mouth = random.choice(mouths)
    left_arm = random.choice(arms)
    right_arm = random.choice(arms + [left_arm] * 3)
    face = left_eye + mouth + right_eye

    flipped = upsidedown.transform(' '.join(args))

    return '(' + left_arm + face + ')' + right_arm + '︵' + flipped


commands = [
    Command('flip', exec_flip, 'This command will flip anything you throw at it. Syntax: `$PREFIXflip something`', False, False, None, None, None, None)
]

module_name = "fun"
