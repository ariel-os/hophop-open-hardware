#!/usr/bin/env python3
"""Check datasheet pin maps, land patterns and local library references (stdlib only).

Run: python libs/validate.py
This complements, and does not replace, KiCad's KLC checkers and visual review.
"""
from pathlib import Path
import json
import math
import re
import fnmatch

ROOT = Path(__file__).resolve().parent


def parse(path):
    stack, result = [], []
    for token in re.findall(r'"(?:\\.|[^"\\])*"|\(|\)|[^\s()]+', path.read_text()):
        if token == '(':
            node = []
            (stack[-1] if stack else result).append(node)
            stack.append(node)
        elif token == ')':
            stack.pop()
        else:
            stack[-1].append(json.loads(token) if token.startswith('"') else token)
    assert not stack and len(result) == 1, path
    return result[0]


def children(node, key):
    return [n for n in node if isinstance(n, list) and n and n[0] == key]


def child(node, key):
    return next(iter(children(node, key)), None)


def pin_numbers(pin):
    return child(pin, 'number')[1].strip('[]').split(',')


def close(a, b):
    assert math.isclose(float(a), b, abs_tol=1e-8), (a, b)


EXPECTED = {
    'TPS63901YCJR': {'A1': 'LX1', 'A2': 'VIN', 'A3': 'EN', 'B1': 'GND',
                    'B2': 'CFG1', 'B3': 'SEL', 'C1': 'GND', 'C2': 'VOUT',
                    'C3': 'CFG2', 'D1': 'LX2', 'D2': 'VOUT', 'D3': 'CFG3'},
    'BQ25180YBGR': {'A1': '~{INT}', 'A2': 'IN', 'B1': 'SCL', 'B2': 'SYS',
                   'C1': 'SDA', 'C2': 'BAT', 'D1': 'TS/MR', 'D2': 'GND'},
    'TPS7A0228': {'A1': 'IN', 'A2': 'OUT', 'B1': 'EN', 'B2': 'GND'},
    'DMN2990UFA': {'G': 'G', 'S': 'S', 'D': 'D'},
    'DMP22D4UFA': {'G': 'G', 'S': 'S', 'D': 'D'},
}
# Datasheet-derived land dimensions: rows, columns, pitch, copper diameter, mask margin.
BGA = {'TPS63901YCJR': (4, 3, .35, .255, -.0375),
       'BQ25180YBGR': (4, 2, .4, .23, .04),
       'TPS7A0228': (2, 2, .35, .265, -.0325)}


def main():
    symbols = children(parse(ROOT / 'symbols/GrassHopperNymph.kicad_sym'), 'symbol')
    assert {s[1] for s in symbols} == set(EXPECTED) | {'VSYS', 'VDD_GPIO'}
    for symbol in symbols:
        name = symbol[1]
        props = {p[1]: p for p in children(symbol, 'property')}
        pins = [p for unit in children(symbol, 'symbol') for p in children(unit, 'pin')]
        assert child(props['Value'], 'hide') is None, name
        assert props['Value'][2] == name, name
        for pin in pins:
            for coordinate in child(pin, 'at')[1:3]:
                close(float(coordinate) / 1.27, round(float(coordinate) / 1.27))
        if name not in EXPECTED:
            assert child(symbol, 'power')[1] == 'global'
            assert props['Reference'][2] == '#PWR'
            assert len(pins) == 1 and pins[0][1] == 'power_in'
            assert child(pins[0], 'hide') is None
            assert child(pins[0], 'name')[1] == '~'
            assert props['Footprint'][2] == ''
            continue
        actual = {number: child(pin, 'name')[1] for pin in pins for number in pin_numbers(pin)}
        assert actual == EXPECTED[name], (name, actual)
        if name == 'BQ25180YBGR':
            types = {n: p[1] for p in pins for n in pin_numbers(p)}
            assert types['A1'] == 'open_collector' and types['C2'] == 'passive'
        nickname, fpname = props['Footprint'][2].split(':')
        assert fnmatch.fnmatchcase(fpname, props['ki_fp_filters'][2])
        fp = parse(ROOT / 'footprints' / (nickname + '.pretty') / (fpname + '.kicad_mod'))
        pads = {pad[1]: pad for pad in children(fp, 'pad') if pad[1]}
        assert set(pads) == set(actual), name
        if name in BGA:
            rows, cols, pitch, diameter, mask = BGA[name]
            for r in range(rows):
                for c in range(cols):
                    pad = pads[f'{chr(65+r)}{c+1}']
                    close(child(pad, 'at')[1], (c-(cols-1)/2)*pitch)
                    close(child(pad, 'at')[2], (r-(rows-1)/2)*pitch)
                    for value in child(pad, 'size')[1:]:
                        close(value, diameter)
                    close(child(pad, 'solder_mask_margin')[1], mask)
        else:
            # Top view rotated 180 degrees from the manufacturer pin diagram.
            expected = {'G': (-.3125, -.175, .375, .2),
                        'S': (-.3125, .175, .375, .2), 'D': (.2625, 0, .475, .45)}
            for number, dimensions in expected.items():
                values = child(pads[number], 'at')[1:3] + child(pads[number], 'size')[1:3]
                for actual_value, expected_value in zip(values, dimensions):
                    close(actual_value, expected_value)
    for folder in (ROOT, ROOT.parent):
        for kind in ('fp', 'sym'):
            for entry in children(parse(folder / f'{kind}-lib-table'), 'lib'):
                uri = child(entry, 'uri')[1]
                uri = uri.replace('${HOPHOP_LIB_DIR}', str(ROOT))
                uri = uri.replace('${KIPRJMOD}', str(ROOT.parent))
                assert Path(uri).exists(), uri
    print('PASS: 7 symbols; datasheet pin maps; 4 land patterns; pin/pad compatibility; both table sets.')


if __name__ == '__main__':
    main()
