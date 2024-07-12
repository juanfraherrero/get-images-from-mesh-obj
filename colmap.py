#
# Copyright (C) 2023, Inria
# GRAPHDECO research group, https://team.inria.fr/graphdeco
# All rights reserved.
#
# This software is free for non-commercial, research and evaluation use
# under the terms of the LICENSE.md file.
#
# For inquiries contact  george.drettakis@inria.fr
#

import os
import logging
from argparse import ArgumentParser
import shutil

# This Python script is based on the shell converter script provided in the MipNerF 360 repository.
parser = ArgumentParser("Colmap converter")
parser.add_argument("--no_gpu", action='store_true', help="Disable GPU usage.")
parser.add_argument("--skip_matching", action='store_true')
parser.add_argument("--source_path", "-s", required=True, type=str, help="Path to the source directory.")
parser.add_argument("--images_folder_name", default="input", type=str, help="Name of the folder containing the images.")
parser.add_argument("--camera", default="PINHOLE", type=str, help="Camera model to use. For Gaussian-Splatting-Cuda of MRNERF, use PINHOLE.")
parser.add_argument("--colmap_executable", default="", type=str, help="Path to the colmap executable if not in PATH.")
parser.add_argument("--resize", action="store_true", help="Resize images with magick.")
parser.add_argument("--magick_executable", default="", type=str, help="Path to the magick executable if not in PATH.")
parser.add_argument("--peak_threshold", default=0.001, type=float, help="Peak threshold for feature extraction. With PINHOLE camera model, use 0.001. With RADIAL use 0.004")
parser.add_argument("--edge_threshold", default=10, type=float, help="Edge threshold for feature extraction. With PINHOLE camera model, use 10. With RADIAL use 7.")

# parse arguments
args = parser.parse_args()

colmap_command = '"{}"'.format(args.colmap_executable) if len(args.colmap_executable) > 0 else "colmap"
magick_command = '"{}"'.format(args.magick_executable) if len(args.magick_executable) > 0 else "magick"
use_gpu = 1 if not args.no_gpu else 0

if not args.skip_matching:
    os.makedirs(args.source_path + "/distorted/sparse", exist_ok=True)

    ## Feature extraction
    feat_extracton_cmd = colmap_command + " feature_extractor "\
        "--database_path " + args.source_path + "/distorted/database.db \
        --image_path " + args.source_path + "/" + str(args.images_folder_name) + " \
        --ImageReader.single_camera 1 \
        --ImageReader.camera_model " + args.camera + " \
        --SiftExtraction.use_gpu " + str(use_gpu) + " \
        --SiftExtraction.peak_threshold " + str(args.peak_threshold) + " \
        --SiftExtraction.edge_threshold " + str(args.edge_threshold)
    exit_code = os.system(feat_extracton_cmd)
    if exit_code != 0:
        logging.error(f"Feature extraction failed with code {exit_code}. Exiting.")
        exit(exit_code)

    ## Feature matching
    feat_matching_cmd = colmap_command + " exhaustive_matcher \
        --database_path " + args.source_path + "/distorted/database.db \
        --SiftMatching.use_gpu " + str(use_gpu) + " \
        --SiftMatching.guided_matching 1 " + " \
        --SiftMatching.max_num_matches 40000 "
    exit_code = os.system(feat_matching_cmd)
    if exit_code != 0:
        logging.error(f"Feature matching failed with code {exit_code}. Exiting.")
        exit(exit_code)

    ### Bundle adjustment
    mapper_cmd = (colmap_command + " mapper \
        --database_path " + args.source_path + "/distorted/database.db \
        --image_path "  + args.source_path + "/" + str(args.images_folder_name) + " \
        --output_path "  + args.source_path + "/distorted/sparse "
        )
    exit_code = os.system(mapper_cmd)
    if exit_code != 0:
        logging.error(f"Mapper failed with code {exit_code}. Exiting.")
        exit(exit_code)

### Image undistortion
## We need to undistort our images into ideal pinhole intrinsics.
img_undist_cmd = (colmap_command + " image_undistorter \
    --image_path "  + args.source_path + "/" + str(args.images_folder_name) + " \
    --input_path " + args.source_path + "/distorted/sparse/0 \
    --output_path " + args.source_path + "\
    --output_type COLMAP")
exit_code = os.system(img_undist_cmd)
if exit_code != 0:
    logging.error(f"Mapper failed with code {exit_code}. Exiting.")
    exit(exit_code)

files = os.listdir(args.source_path + "/sparse")
os.makedirs(args.source_path + "/sparse/0", exist_ok=True)
# Copy each file from the source directory to the destination directory
for file in files:
    if file == '0':
        continue
    source_file = os.path.join(args.source_path, "sparse", file)
    destination_file = os.path.join(args.source_path, "sparse", "0", file)
    shutil.move(source_file, destination_file)


print("Done.")
