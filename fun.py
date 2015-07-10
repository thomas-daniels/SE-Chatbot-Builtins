#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from Module import Command
import random
import upsidedown


eyes = ['°', '゜', 'ಥ', "'", '•', '^']
mouths = ['□', 'Д', '益', 'ᴥ', '.']

def exec_flip(cmd, bot, args, msg, event): # cmd refers to the Command you assign this function to
    global eyes
    global mouths
    if len(args) == 0:
        return 'Not enough arguments'
    eye = random.choice(eyes)
    mouth = random.choice(mouths)
    face = eye + mouth + eye

    flipped = upsidedown.transform(' '.join(args))

    return '(╯%s)╯︵%s' % (face, flipped)


commands = [
    Command( 'flip', exec_flip, 'This command will flip anything you throw at it. Syntax: `>>flip <something>`')
    # Command( '<command name>', <command exec name>, '<help text>' (optional), <needs privilege> (= False), <owner only> (= False), <char check>(*) (= True), <special arg parsing method>(**) (= None) ),
    # ...
]

module_name = "fun"
