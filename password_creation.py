#!/usr/bin/env python3

from string import ascii_lowercase, ascii_uppercase, digits
from secrets import choice
from random import shuffle
import os
import sys


def create_password(length=10, spec_chars=''):

    lower = list(ascii_lowercase)
    upper = list(ascii_uppercase)
    nums = list(digits)

    if (spec_chars == ''):
        all_chars = (lower + upper + nums)

        holder = []
        holder.append(choice(lower) + choice(upper) + choice(nums))

        while (len(holder) != length):
            holder.append(choice(all_chars))

    else:
        spec_chars = list(spec_chars)

        all_chars = (lower + upper + nums + spec_chars)

        holder = []
        holder.append(choice(lower) + choice(upper) + choice(nums) +
                      choice(spec_chars))

        while (len(holder) != length):
            holder.append(choice(all_chars))

    shuffle(holder)
    password = ''.join([str(x) for x in holder])

    return password
