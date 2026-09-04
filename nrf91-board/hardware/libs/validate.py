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
import hashlib

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
    'TPS63901YCJ': {'A1': 'LX1', 'A2': 'VIN', 'A3': 'EN', 'B1': 'GND',
                    'B2': 'CFG1', 'B3': 'SEL', 'C1': 'GND', 'C2': 'VOUT',
                    'C3': 'CFG2', 'D1': 'LX2', 'D2': 'VOUT', 'D3': 'CFG3'},
    'BQ25180YBG': {'A1': '~{INT}', 'A2': 'IN', 'B1': 'SCL', 'B2': 'SYS',
                   'C1': 'SDA', 'C2': 'BAT', 'D1': 'TS/MR', 'D2': 'GND'},
    'TPS7A0228YCH': {'A1': 'IN', 'A2': 'OUT', 'B1': 'EN', 'B2': 'GND'},
    'DMN2990UFA': {'G': 'G', 'S': 'S', 'D': 'D'},
    'DMP22D4UFA': {'G': 'G', 'S': 'S', 'D': 'D'},
}
# Datasheet-derived land dimensions: rows, columns, pitch, copper diameter, mask margin.
BGA = {'TPS63901YCJ': (4, 3, .35, .255, -.0375),
       'BQ25180YBG': (4, 2, .4, .23, .04),
       'TPS7A0228YCH': (2, 2, .35, .265, -.0325)}


def main():
    libraries = {p.stem: children(parse(p), 'symbol')
                 for p in (ROOT / 'symbols').glob('*.kicad_sym')}
    symbols = [s for group in libraries.values() for s in group]
    assert {s[1] for s in symbols} == set(EXPECTED) | {'nRF9151-LAxx'}
    upstream = ROOT / 'symbols/HopHop_MCU_Nordic.kicad_sym'
    assert hashlib.sha256(upstream.read_bytes()).hexdigest() == (
        '1b0259f782029a0e144c33bf886970b0c4c023394163aa20060c97aab993ba28')
    for symbol in symbols:
        name = symbol[1]
        props = {p[1]: p for p in children(symbol, 'property')}
        pins = [p for unit in children(symbol, 'symbol') for p in children(unit, 'pin')]
        assert child(props['Value'], 'hide') is None, name
        assert props['Value'][2] == name, name
        for pin in pins:
            for coordinate in child(pin, 'at')[1:3]:
                close(float(coordinate) / 1.27, round(float(coordinate) / 1.27))
        if name == 'nRF9151-LAxx':
            assert {child(p, 'number')[1] for p in pins} == {str(n) for n in range(1, 114)}
            assert props['Footprint'][2] == (
                'Package_LGA:Nordic_nRF9151-LAxx_LGA-80-33EP_12.1x11.1mm_P0.5mm')
            continue
        actual = {number: child(pin, 'name')[1] for pin in pins for number in pin_numbers(pin)}
        assert actual == EXPECTED[name], (name, actual)
        if name == 'BQ25180YBG':
            types = {n: p[1] for p in pins for n in pin_numbers(p)}
            assert types['A1'] == 'open_collector' and types['C2'] == 'passive'
        nickname, fpname = props['Footprint'][2].split(':')
        assert fnmatch.fnmatchcase(fpname, props['ki_fp_filters'][2])
        fp = parse(ROOT / 'footprints' / (nickname + '.pretty') / (fpname + '.kicad_mod'))
        model = child(fp, 'model')
        assert model[1] == f'${{KICAD10_3DMODEL_DIR}}/{nickname}.3dshapes/{fpname}.step'
        for key, expected in [('offset', 0), ('rotate', 0), ('scale', 1)]:
            assert all(float(v) == expected for v in child(child(model, key), 'xyz')[1:])
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
    for path in ROOT.parent.glob('*.kicad_sch'):
        schematic = parse(path)
        cached = {s[1] for s in children(child(schematic, 'lib_symbols'), 'symbol')}
        for placed in children(schematic, 'symbol'):
            lib_id = child(placed, 'lib_id')[1]
            assert not lib_id.startswith('GrassHopperNymph:'), (path, lib_id)
            if lib_id.startswith('HopHop_'):
                nickname, name = lib_id.split(':')
                assert name in {s[1] for s in libraries[nickname]}, (path, lib_id)
                assert lib_id in cached, (path, lib_id)
            props = {p[1]: p[2] for p in children(placed, 'property')}
            footprint = props.get('Footprint', '')
            assert not footprint.startswith('GrassHopperNymph:'), (path, footprint)
            if footprint.startswith('HopHop_'):
                nickname, name = footprint.split(':')
                assert (ROOT / 'footprints' / f'{nickname}.pretty' / f'{name}.kicad_mod').exists()
    print('PASS: 5 custom symbols; exact upstream nRF9151; 4 land patterns; '
          'model references; pin/pad compatibility; tables; project references.')


if __name__ == '__main__':
    main()
