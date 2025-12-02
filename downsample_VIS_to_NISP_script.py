#!/usr/bin/env python
import os
import numpy as np
import argparse
import glob
from tqdm import tqdm
from astropy.io import fits
from reproject import reproject_exact
from astropy.wcs import WCS
import pandas as pd
import matplotlib.pyplot as plt


def mag(flux, zp):
    return -2.5*np.log10(flux) + zp

def downsample_vis_to_nisp(vis_file,
                           nisp_file,
                           vis_zeropoint=30.132,
                           nisp_zeropoint=30.000):

    # get header from the nisp image
    nisp_header = fits.getheader(nisp_file)

    with fits.open(vis_file, memmap=False) as hdu_list:
        vis_header = hdu_list[0].header
        vis_data = hdu_list[0].data

        vis_pixel_size = np.sqrt(np.prod(np.abs(np.diag(WCS(vis_header).pixel_scale_matrix))))*3600
        vis_pixel_area = vis_pixel_size**2
        # vis_pixel_area = 1

        # convert to surface brightness
        # see note documentation : https://reproject.readthedocs.io/en/stable/celestial.html
        vis_data_SB = vis_data / vis_pixel_area

        # reproject
        vis_data_SB_resampled = reproject_exact((vis_data_SB, vis_header),
                                                nisp_header,
                                                return_footprint=False)

        nisp_pixel_size = np.sqrt(np.prod(np.abs(np.diag(WCS(nisp_header).pixel_scale_matrix))))*3600
        nisp_pixel_area = nisp_pixel_size**2

        # convert back to flux
        # scaling = (nisp_pixel_size/vis_pixel_size)**2
        vis_data_resampled = vis_data_SB_resampled * nisp_pixel_area
        # vis_data_resampled = (vis_data_SB_resampled *
        #                       nisp_pixel_area) *
        #                        10**(0.4*(vis_zeropoint - nisp_zeropoint))
        #                        )

        zeropoint_conversion = 10**(0.4*(nisp_zeropoint-vis_zeropoint))
        # print(mag(vis_data_resampled.sum(),vis_zeropoint),
        #       mag(vis_data.sum(), vis_zeropoint))
        
        # cut = 0.1
#         relative_error = np.abs(vis_data_resampled.sum() - vis_data.sum() ) / vis_data.sum()*100
        # np.abs(vis_data_resampled.sum()*scaling - vis_data.sum() ) / vis_data.sum() > cut
        # if :
        #     print(vis_data_resampled.sum()*scaling,
        #       vis_data.sum(),
        #       np.abs(vis_data_resampled.sum()*scaling - vis_data.sum() ) / vis_data.sum() * 100)
    return (vis_data_resampled,
            nisp_header,
#             relative_error,
            vis_data_resampled * zeropoint_conversion
            )


# if __name__ == "__main__":

parser = argparse.ArgumentParser(description = 'Downsample VIS cutouts to NISP pixel size')
parser.add_argument('vis_dir', type=str, help='VIS cutouts directory')
parser.add_argument('nisp_dir', type=str, help='NISP cutouts directory')
# parser.add_argument('output_dir', type=str, help='output directory')
parser.add_argument('output_dir_nisp_zeropoint', type=str, help='output directory')
args = parser.parse_args()

os.makedirs(args.output_dir_nisp_zeropoint,exist_ok=True)
#print(f"Resampled images saved at {args.output_dir} ")
print(f"Resampled images wit NISP zero point saved at {args.output_dir_nisp_zeropoint} ")

filenames = glob.glob("*.fits", root_dir=args.vis_dir)


# relative_errors = []


for i,filename in tqdm(enumerate(filenames)):
    
    vis_file = os.path.join(args.vis_dir, filename)
    nisp_file = os.path.join(args.nisp_dir, filename)

    out = downsample_vis_to_nisp(vis_file, nisp_file)
#    vis_data_resampled, header, relative_error, vis_data_resampled_nisp_zeropoint = out
#    relative_errors.append(relative_error)
    vis_data_resampled, header, vis_data_resampled_nisp_zeropoint = out
    
    # output_file = os.path.join(args.output_dir, filename)
    output_file_nisp_zeropoint = os.path.join(args.output_dir_nisp_zeropoint, filename)
    # fits.writeto(output_file, vis_data_resampled, header, overwrite=True)
    fits.writeto(output_file_nisp_zeropoint, 
                 vis_data_resampled_nisp_zeropoint, header, overwrite=True)
    

