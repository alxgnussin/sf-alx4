# -*- coding: utf-8 -*-
# Python 3.7.7 required

import json

from data import goals, teachers

with open('goals.json', 'w', encoding='utf8') as f:
    f.write(json.dumps(goals, ensure_ascii=False))

with open('teachers.json', 'w', encoding='utf8') as f:
    f.write(json.dumps(teachers, ensure_ascii=False))