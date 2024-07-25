import subprocess
import os
import logging

## CONFIG LOGGER
log_to_file = logging.getLogger(__name__)
logging.basicConfig(
    filename="app.log",
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


## FUNCTION TO RUN CLI.PY WITH PVPYTHON
def generate_images(
    input,
    output,
    size,
    numberRotations,
    numberImages,
    anglePerRotation,
    distanceOrRadio,
    initMovement,
    endMovement,
    cantStepMovement,
) -> int:
    current_dir = os.path.dirname(os.path.abspath(__file__))

    command = (
        "pvpython "
        + os.path.join(current_dir, "cli.py")
        + ' --input "'
        + str(input)
        + '" --output "'
        + str(output)
        + '" --size '
        + str(size)
        + " --numberRotations "
        + str(numberRotations)
        + " --numberImages "
        + str(numberImages)
        + " --anglePerRotation "
        + str(anglePerRotation)
        + " --distanceOrRadio "
        + str(distanceOrRadio)
        + " --initMovement "
        + str(initMovement)
        + " --endMovement "
        + str(endMovement)
        + " --cantStepMovement "
        + str(cantStepMovement)
    )

    result = subprocess.run(
        command, cwd=current_dir, shell=True, capture_output=True, text=True
    )

    if result.returncode != 0:
        log_to_file.error(f"Error during subprocess in cli.py -- {result.stderr}")
    else:
        log_to_file.info("Success running cli.py")

    return result.returncode
