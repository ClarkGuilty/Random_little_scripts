#!/usr/bin/env python3
#%%
import os
import re
import sys
from decimal import Decimal
from typing import Tuple, Union


# pattern: Tile<digits>RA<digits>DEC<rest>
_PATTERN = re.compile(r'^Tile(?P<tile>\d+)RA(?P<ra>\d+)DEC(?P<dec>.+)$', re.IGNORECASE)

def extract_parts(filename: str) -> Tuple[str, str, str]:
    """
    Extract the raw string parts from the filename.
    Returns: (tile_str, ra_str, dec_str)
    """
    m = _PATTERN.match(filename)
    if not m:
        raise ValueError(f"Filename not in expected format: {filename!r}")
    return m.group('tile'), m.group('ra'), m.group('dec')

def parse_tile(tile_str: str) -> int:
    """Convert tile string to int."""
    if not tile_str.isdigit():
        raise ValueError("Tile string must be digits")
    return int(tile_str)

def parse_ra(ra_str: str, *, use_decimal: bool = False) -> Union[float, Decimal]:
    """
    Convert RA string to degrees.
    Interpretation: first 3 digits = integer degrees, remaining digits = fractional digits.
    Example: '3585641059157' -> 358.5641059157
    If use_decimal=True returns a Decimal, otherwise a float.
    """
    if not ra_str.isdigit() or len(ra_str) < 3:
        raise ValueError("RA string must be numeric and have at least 3 digits")
    int_part = ra_str[:3]
    frac_part = ra_str[3:] or '0'
    if use_decimal:
        return Decimal(f"{int_part}.{frac_part}")
    else:
        return int(int_part) + int(frac_part) / (10 ** len(frac_part))

def parse_dec(dec_str: str, *, use_decimal: bool = False) -> Union[float, Decimal]:
    """
    Convert Dec string to signed degrees.
    Accepted sign prefixes: 'NEG'/'POS' (case-insensitive) or leading '-'/'+'.
    After sign, first 3 digits = integer degrees, remaining digits = fractional digits.
    Example: 'NEG0572495923968' -> -57.2495923968
    """
    if not dec_str:
        raise ValueError("Empty DEC string")

    ds_up = dec_str.upper()
    sign = 1
    if ds_up.startswith("NEG"):
        sign = -1
        body = dec_str[3:]
    elif ds_up.startswith("POS"): #Not necessary but doesn't hurt
        sign = 1
        body = dec_str[3:]
    elif dec_str[0] in "+-":
        sign = -1 if dec_str[0] == "-" else 1
        body = dec_str[1:]
    else:
        body = dec_str

    if not body.isdigit() or len(body) < 3:
        raise ValueError("DEC body must be numeric and have at least 3 digits after sign")

    int_part = body[:3]
    frac_part = body[3:] or '0'
    if use_decimal:
        val = Decimal(f"{int_part}.{frac_part}")
        return val.copy_negate() if sign < 0 else val
    else:
        val = int(int_part) + int(frac_part) / (10 ** len(frac_part))
        return -val if sign < 0 else val


def parse_tile_RA_Dec(string):
    tile, ra, dec = extract_parts(string)
    # return parse_tile(tile), parse_ra(ra), parse_dec(dec)
#    return tile, parse_ra(ra), parse_dec(dec) # Tile is more convenient as a string.
    return parse_ra(ra), parse_dec(dec) # Tile is more convenient as a string.


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {os.path.basename(sys.argv[0])} <Tile...RA...DEC...string>", file=sys.stderr)
        sys.exit(2)
    s = sys.argv[1]
    try:
        result = parse_tile_RA_Dec(s)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    print(*result)
