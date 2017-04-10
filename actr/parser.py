'''
* Description *

This parser is an example script used to extract specific module information from the
productions from a concentration game model. 

This file parses two files: speed-productions.txt and mouse-positions-and-times.csv

The speed-productions.txt has the production events and the mouse-positions-and-times.csv file
has the positions of the cursor for each second (see parse_mouse.py)

* ACT-R notes *

QUESTIONS:

How should we classify cognitive operators?

- General method to parse the productions might not be possible since it depends on the 
production rules of the model; however, you can copy the general structure of the 
- The operators gathered for the Concentration model here is specific to the rules in the model

** MOUSE **

- Note that move cursor lasts from MOTOR's move cursor until before the click
production fires:

    0.100   MOTOR                  MOVE-CURSOR OBJECT NIL LOC VISUAL-LOCATION1-0-0 (move cursor begin)
    0.100   PROCEDURAL             CONFLICT-RESOLUTION
    0.140   PROCEDURAL             CONFLICT-RESOLUTION
    0.150   PROCEDURAL             CONFLICT-RESOLUTION
    0.185   VISION                 Encoding-complete VISUAL-LOCATION1-0-0 NIL
    0.185   VISION                 SET-BUFFER-CHUNK VISUAL TEXT0
    0.185   PROCEDURAL             CONFLICT-RESOLUTION
    0.214   PROCEDURAL             CONFLICT-RESOLUTION
    0.224   PROCEDURAL             CONFLICT-RESOLUTION (move cursor end)
    0.274   PROCEDURAL             PRODUCTION-FIRED CLICK-FIRST-TILE

- To get the mouse trace, turn on :incremental-mouse-moves t and :trace-mouse t via 'sgp'
- :incremental-mouse-moves updates mouse location every 50ms by default or can be specified as it is
for this example (t = 0.0001ms)
- :trace-mouse will maintain a record of where the model moved the mouse
- After the model runs, run the (get-mouse-trace) command to get the time and positions

** BOARD **

- Note the tiles are denoted 2-8 for {A, B, C, E, H, I, P, Q}
- The board in the given screenshot board.png, and production_sample files is:

4   2   4   8
6   9   7   5
2   3   7   3
6   9   5   8

Helvetica Neue LT Std 65 Medium typeface

C   A   C   P
H   Q   I   E
A   B   I   B
H   Q   E   P

** JSON FORMATS **

- Cursor movement format (from mouse-positions-and-times.csv):
- For now, we specify the mouse movement as gaze as we can make use of the gaze processor
for visualizing the cursor movements.

"gaze": {
    "x": 200,
    "y": 150,
    "duration": 60
}

- There's also a more generic move JSON for indicating when mouse is moving

"mouse": {
    "type": move,
    "start": 200,
    "duration": 60
}

- However, we can use the format above along with the finer-grained times and
exact positions for visualization

- Click format:

"click": {
    "type": "click",
    "x": 200,
    "y": 150,
    "duration": 60
}

- Cognitive format:

"cognitive": {
    "type": "click", // Type is the event that this operator is for
    "action": "start-find-unattended" // production action
    "request": "perceptual" // module(s) to satisfy action
    "summary": "Look for a tile to click" // short description of event/action
    "duration": 50 // duration is usually 50ms
}

- (For now sticking with only counting production fire events, i.e the procedure
the model executes to play concentration)

- Vision format:

"visual": {
    "type": find-location / move-attention
    "x": 200 // can't get these with vanilla ACT-R, might be possible with EMMA
    "y": 150
    "duration": 50/85 // find-location is usually 50ms, and move-attention 85ms
}

- (For now visual events are simply finding locations and moving visual attention)
- However, we could use something more fine-grained and precise like EMMA, Eye
Movement and Movement Attention module.

'''

import re
import json
from collections import OrderedDict

board = {"2":"A", "3":"B", "4":"C", "5":"E", "6":"H", "7":"I", "8":"P", "9":"Q",}
# Utility function for determining row/col based on x or y position
def determine_target(x, y):
    x = int(x)
    y = int(y)
    row = None
    col = None
    if(x < 100):
        col =  1
    if(x > 100 and x < 200):
        col = 2
    if(x > 200 and x < 300):
        col = 3
    elif(x > 300):
        col = 4
    if(y < 100):
        row =  1
    if(y > 100 and y < 200):
        row = 2
    if(y > 200 and y < 300):
        row = 3
    elif(y > 300):
        row = 4
    return row, col

# Creates a conflict resolution event
def end_conflict_resolution(start, end):
    if(start != None and start < end):
        event_type = "" # Leave this blank for now for a less cluttered timeline
        request = "None"
        summary = "Conflict resolution"
        data['data'][str(start)]['conflict'] = OrderedDict([
            ('type', event_type),
            ('action', "Conflict Resolution"),
            ('request', request),
            ('summary', summary),
            ('duration', end - start)
        ])

# Go through productions to gather timestamp data and operators in each timestamp
f = open('data/speed-productions.txt','r')
prod_times = []
for line in f:
    relevant = line.split()
    if(relevant[0] != "***" and relevant[0] != "#|Warning:"):
        # Event timestamps
        int_time = int(float(relevant[0])*1000)
        string_time = str(int(float(relevant[0])*1000))
        prod_times.append(int_time)

# Create a JSON for the dataset's "data"
data = OrderedDict()
# Construct json for settings
data['settings'] = OrderedDict([
    ("title", "Concentration Game Level 1"),
    ("start", prod_times[0]),
    ("end", prod_times[len(prod_times)-1]),
    ("level", 0), # this is temporary to make it work with typing example
    ("startOffset", 100),
    ("endOffset", 200)
    ])
data['data'] = OrderedDict()
for t in range(0, prod_times[len(prod_times)-1]+1):
    data['data'][str(t)] = OrderedDict()
# Gather all the mouse cursor movement
cursor_data = open('data/mouse-positions-and-times.csv', 'r')
cursor_data.readline()
movement = cursor_data.read().split()
init_x = 45
init_y = 44
last_time = 0
for line in movement:
    point =  line.split(",")
    if(init_x == 0 and point[1] != 0):
        init_x = init_x + float(point[1])
        # print init_x
    if(init_y == 0 and point[2] != 0):
        init_y = init_y + float(point[2])
        # print init_y
    # print str(point[0])
    data['data'][point[0]]["gaze"] = OrderedDict([
        # ("type", "move"),
        ("start", point[0]),
        ("x", str(float(point[1])+45)),
        ("y", str(float(point[2])+44)),
        ("duration", int(point[0]) - last_time),
        ("fixated", "false")
    ])
    last_time = int(point[0])
mouse_times = OrderedDict()
# Finally, parse production event file to gather timestamps, and durations of events
click_durations = []
down_click = 0
up_click = 0
prev_mouse_x = init_x
prev_mouse_y = init_y
prev_mouse_time = 0
conflict_resolution_start = None
last_event = ""
f.seek(0)
# TODO Clean this section to make it more readable
for line in f:
    relevant = line.split()
    if(relevant[0] != "***" and relevant[0] != "#|Warning:"):
        # Event timestamps
        int_time = int(float(relevant[0])*1000) 
        string_time = str(int(float(relevant[0])*1000))
        event = relevant[1]
        # Go through and collect different 'processor' events
        ''' MOTOR '''
        # Collect start and end times for clicks
        # print last_event
        if(event == "MOTOR"):
            if(relevant[2] == "CLICK-MOUSE"):
                down_click = int_time
                duration = down_click - mouse_start
                data['data'][str(mouse_start)]['mouse'] = OrderedDict([
                    ('type', 'move'),
                    ('start', str(mouse_start)),
                    ('duration', duration)
                ])
            elif(relevant[2] == "OUTPUT-KEY"):
                up_click = int_time
            if(last_event == "CONFLICT-RESOLUTION"):
                end_conflict_resolution(conflict_resolution_start, int_time)
            last_event = "MOTOR"
        if("gaze" in data['data'][string_time]):
            prev_mouse_x = data['data'][string_time]['gaze']['x']
            prev_mouse_y = data['data'][string_time]['gaze']['y']
        ''' VISUAL '''
        # Currently, there is no direct use of the visual events (perhaps later with EMMA)
        if(event == "VISION"): 
            if(last_event == "CONFLICT-RESOLUTION"):
                end_conflict_resolution(conflict_resolution_start, int_time)
            last_event = "VISION"
        ''' IMAGINAL '''
        # Currently, there is no direct use of the imaginal events
        if(event == "IMAGINAL"): 
            if(last_event == "CONFLICT-RESOLUTION"):
                end_conflict_resolution(conflict_resolution_start, int_time)
            last_event = "IMAGINAL"
        ''' COGNITIVE and/or PERCEPTUAL '''
        if(event == "PROCEDURAL"):
            if(relevant[2] == "PRODUCTION-FIRED"):
                event_type = relevant[3].lower()
                request = "None"
                summary = ""
                if("unattended" in event_type or "find-random" in event_type): # visual
                    event_type = "P"
                    request = "Perceptual"
                    summary = "Look for a tile to click"
                elif("attend" in event_type or "find-matching" in event_type): # visual and motor
                    event_type = "P, M"
                    request = "Perceptual and Motor"
                    summary = "Attend to or find the matching tile"
                    # Add a pair of perceptual for attend, for both finding a location
                    # and a visual attention shift
                    data['data'][string_time]['perceptual'] = OrderedDict([
                        ('type', "visual"),
                        ('action', "Find location"),
                        ('duration', 50)
                    ])
                    move_attention_time = str(int(string_time)+50);
                    # if(move_attention_time not in data['data']):
                    #     data['data'][move_attention_time] = OrderedDict()
                    data['data'][move_attention_time]['perceptual'] = OrderedDict([
                        ('type', "visual"),
                        ('action', "Move attention"),
                        ('duration', 85)
                    ])
                    mouse_start = int(string_time)+50
                elif("read-first" in event_type or "check" in event_type): # working memory
                    event_type = "WM"
                    request = "Working Memory"
                    summary = "Store or retrieve chunk from memory"
                elif("click" in event_type): # motor
                    event_type = "M"
                    request = "Motor"
                    summary = "Click on a tile"
                elif("read-second-tile" in event_type):
                    event_type = "C" # "pure" meaning no request needed to other modules
                    summary = "Read a matching second tile"
                elif("match-found-restart" in event_type):
                    event_type = "C" # "pure" meaning no request needed to other modules
                    summary = "Tiles were a match, start over"
                elif("start-with" in event_type):
                    event_type = "C" # "pure" meaning no request needed to other modules
                    summary = "Start with random tile"
                data['data'][string_time]['cognitive'] = OrderedDict([
                    ('type', event_type),
                    ('action', relevant[3].lower()),
                    ('request', request),
                    ('summary', summary),
                    ('duration', 50)
                ])
                data['data'][string_time]["gaze"] = OrderedDict([
                    # ("type", "move"),
                    ("start", string_time),
                    ("x", prev_mouse_x),
                    ("y", prev_mouse_y),
                    ("duration", int_time - prev_mouse_time),
                    ("fixated", "true")
                ])
                prev_mouse_time = int_time
            elif(relevant[2] == "CONFLICT-RESOLUTION"):
                # No conflict resolution events yet
                if(last_event != "CONFLICT-RESOLUTION" or conflict_resolution_start == None):
                    conflict_resolution_start = int_time
                last_event = "CONFLICT-RESOLUTION"
            if(relevant[2] != "CONFLICT-RESOLUTION"):
                end_conflict_resolution(conflict_resolution_start, int_time)
                last_event = "COGNITIVE"
    # Note where the click location was
    elif(relevant[0] == "***" and relevant[2] == "Clicked"):
        duration = up_click - down_click
        # print duration
        x = relevant[4].split("#(")[1] 
        y = relevant[5].split(").")[0]
        location = determine_target(x, y)
        data['data'][str(down_click)]['click'] = OrderedDict([
            ('type', 'click'),
            ('x', x),
            ('y', y),
            ('target', board[relevant[3]]),
            ('row', location[0]),
            ('col', location[1]),
            ('duration', duration)
        ])

# Output JSON to a file when running with redirect "python parser.py > file"
json_data = json.dumps( data, indent=4, separators=(',', ': '))
print json_data

f.close()
cursor_data.close()
