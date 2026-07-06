import json, os

script_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(script_dir, 'DBManager_OnStart.txt'), 'r', encoding='utf-8') as f:
    handler1_code = f.read()

with open(os.path.join(script_dir, 'DBManager_Screen.txt'), 'r', encoding='utf-8') as f:
    screen_content = f.read()

handler0_code = 'Tick()'

handler2_code = (
    "if screen then\n"
    "    screen.setRenderScript(OfflineScreenContent)\n"
    "end\n"
)

# Generate onScreenOutput handlers for all possible screen slots (0-9)
# The screen calls setOutput() in render script, which triggers this event
screen_output_handlers = []
for slot_num in range(10):
    screen_output_handlers.append({
        'code': 'HandleScreenCommand(output)',
        'filter': {'args': [{'variable': '*'}], 'signature': 'onOutputChanged(output)', 'slotKey': str(slot_num)},
        'key': str(10 + slot_num)  # keys 10-19
    })

handler3_code = 'ScreenContent = [[' + '\n' + screen_content + '\n]]'

offline_overlay = (
    "\n-- OFFLINE\n"
    "setNextFillColor(overlayLayer, 0, 0, 0, 0.6)\n"
    "addBox(overlayLayer, 0, 0, rx, ry)\n"
    "setNextFillColor(overlayLayer, 1, 0.2, 0.2, 1)\n"
    "setNextTextAlign(overlayLayer, AlignH_Center, AlignV_Middle)\n"
    "addText(overlayLayer, largefont, 'DB Manager Offline', rx * 0.5, ry * 0.5)\n"
    "setNextFillColor(overlayLayer, 0.7, 0.7, 0.7, 0.8)\n"
    "addText(overlayLayer, medfont, 'Power on the Programming Board', rx * 0.5, ry * 0.5 + 40)\n"
)

handler4_code = 'OfflineScreenContent = [[' + '\n' + screen_content + '\n' + offline_overlay + '\n]]'

def make_slot(name):
    return {'name': name, 'type': {'events': [], 'methods': []}}

pb = {
    'slots': {
        '0': make_slot('slot1'), '1': make_slot('slot2'),
        '2': make_slot('slot3'), '3': make_slot('slot4'),
        '4': make_slot('slot5'), '5': make_slot('slot6'),
        '6': make_slot('slot7'), '7': make_slot('slot8'),
        '8': make_slot('slot9'), '9': make_slot('slot10'),
        '-1': make_slot('unit'), '-2': make_slot('construct'),
        '-3': make_slot('player'), '-4': make_slot('system'),
        '-5': make_slot('library')
    },
    'handlers': [
        {
            'code': handler0_code,
            'filter': {'args': [{'value': 'tick'}], 'signature': 'tick(timerId)', 'slotKey': '-1'},
            'key': '0'
        },
        {
            'code': handler1_code,
            'filter': {'args': [], 'signature': 'onStart()', 'slotKey': '-1'},
            'key': '1'
        },
        {
            'code': handler2_code,
            'filter': {'args': [], 'signature': 'onStop()', 'slotKey': '-1'},
            'key': '2'
        },
        {
            'code': handler3_code,
            'filter': {'args': [], 'signature': 'onStart()', 'slotKey': '-5'},
            'key': '3'
        },
        {
            'code': handler4_code,
            'filter': {'args': [], 'signature': 'onStart()', 'slotKey': '-5'},
            'key': '4'
        }
    ] + screen_output_handlers,
    'methods': [],
    'events': []
}

out_path = os.path.join(script_dir, 'DBManager_PB_FULL.txt')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(pb, f, separators=(',', ':'), ensure_ascii=True)

size = os.path.getsize(out_path)
print(f'Done! File: {out_path}')
print(f'Size: {size} bytes')
print(f'Handlers: {len(pb["handlers"])}')