'''
Parses list of mouse positions from two files:
- mouse-positions-huge.txt
- mouse-times-huge.txt

- Performed these commands on the output of ACT-R's (get-mouse-trace) command
(mapcar #'car '((t (x y)),.....) // gets the times
(mapcar #'cdr '((t (x y)),.....) // gets the positions
'''

import re

# Get mouse times file
mousetimes = open('data/mouse-times.txt', 'r')
in_mousetimes = re.findall("\d*\.\d+|\d+", mousetimes.read())
# Get mouse positions file
pos = open('data/mouse-positions.txt', 'r')
output = open('data/mouse-positions-and-times.csv', 'w')
output.write('time, x, y\n')
split = pos.read().split("#(")
m_times = []
x_values = []
y_values = []
for s in range(len(split)-1, 0, -1):
    mouse_time_int = int(float(in_mousetimes[s-1])*1000)
    positions = (re.findall("\d*\.\d+|\d+", split[s]))
    output.write(str(mouse_time_int)+","+positions[0]+","+positions[1]+"\n")

mousetimes.close()
pos.close()
output.close()
