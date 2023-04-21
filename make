#!./venv/bin/python
import hiker
from pathlib import Path
import os

os.system('rm *.pkl')

it = hiker.example_itinerary()
hiker.dump_itinerary(it)
print(f'http://127.0.0.1:5000/overview/{it.id}')
