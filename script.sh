#!/bin/bash

INPUT_PATH='...'
OUTPUT_PATH='...'
SIZE=512
NUMBER_OF_IMAGES=10
NUMBER_OF_ROTATIONS=4
ANGLE_PER_ROTATION=30
DISTANCE=60
INIT_MOVEMENT=0
END_MOVEMENT=0
CANT_STEP_MOVEMENTS=0

# ADD pvpython to your PATH or else define absolute path to pvpython
pvpython cli.py \
-i "$INPUT_PATH" \
-o "$OUTPUT_PATH" \
-s "$SIZE" \
-n "$NUMBER_OF_IMAGES" \
-r "$NUMBER_OF_ROTATIONS" \
-a "$ANGLE_PER_ROTATION" \
-d "$DISTANCE" \
--initMovement "$INIT_MOVEMENT" \
--endMovement "$END_MOVEMENT" \
--cantStepMovement "$CANT_STEP_MOVEMENTS" \
-v