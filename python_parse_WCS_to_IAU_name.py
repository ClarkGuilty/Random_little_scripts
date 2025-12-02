#!/usr/bin/env python3


import sys
import os

from astropy.coordinates import SkyCoord
from astropy import units as u

#%%
def name_from_radec(ra,dec):
    c = SkyCoord(ra,dec,
                       frame='icrs',
                        unit="deg"
                       )
    ra, dec = c.to_string('hmsdms').split()
    return r'EUCLJ'+ra[:2]+ra[3:5]+ra[6:11]+dec[:3].replace('-','$-$')+dec[4:6]+dec[7:11] # EUCL\,J031718.38+413525.9



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {os.path.basename(sys.argv[0])} <RA Dec>", file=sys.stderr)
        sys.exit(2)
    ra = sys.argv[1]
    dec = sys.argv[2]
    try:
        result = name_from_radec(ra,dec)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    print(result)

