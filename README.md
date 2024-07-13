# Get images from .OBJ file

This repo contains script to retrieve, with paraview, a sequence of images from .obj object file. 

## How it works

The scripts recive several params, Rotates the object for *--numberRotations* and each rotation is spaceing by *--anglePerRotation*. The rotations is over the y axis. Each rotation starts to take *--numberImages* images equally distributed over the axis. And for the movement, normally to obtain more data when using 4 as *--numberImages*, setting 0° to 90° by 10° the movement, this enables us to get more view angles.

``` txt
--input -> Path to .obj input file.
--output -> Path directory to store images of .obj file.
--size -> Images size, square output.
--numberImages -> Quantity of images per rotation.
--numberRotations -> Quantity of ratations.
--anglePerRotation -> Angle difference between two rotations. In °.
--distanceOrRadio -> Distance between camera and object.
--initMovement -> The angle where starts the movement for each rotation.
--endMovement -> The angle where ends the movement for each rotation.
--cantStepMovement -> The quantity of movements between angles defined in movement.
--verbose -> Show info of steps.
```

## Paraview Installation

Must have installed Paraview, and use *pvpython* inside bin to run the script. 
This enable python to access paraview API.

Download Paraview from (link)[https://www.paraview.org/download/]

*Recommend to add bin folder to PATH* else must use absolute path to pvpython!

## Class Diagram

```mermaid
classDiagram
    class Paraview {
        - model: any
        - renderView: any
        - display: any
        - layout1: any
        - size: int
        - radius: int
        - numberImages: int
        - numberRotations: int
        - anglePerRotation: int
        - output: int
        - verbose: int
        - init_azimut: int
        - end_azimut: int
        - cant_step_azimut: int
        - center: List[float]
        
        + Paraview(input: str, size: int, numberImages: int, numberRotations: int, anglePerRotation: int, radius: int, output: int, verbose: int, init_azimut: int, end_azimut: int, cant_step_azimut: int)
        + set_background_color(color: List[float]): void
        + set_object_color(color: List[float]): void
        + activate_ilumination(principal_light: float=0.5, fill_light: float=0.5): void
        + set_camera_position(position: List[float]): void
        + calculate_new_position(angle_azimut: float,angle_elevation: float,radius: int, center: List[float]): List[float]
        + save_screenshot(filename: str, view: any, image_resolution: List[int]=[3000, 3000]): void
        + start(): void
    }

```

## Entry points

```mermaid
graph TD
    A[Repositorio] --> B[script.sh]
    A --> C[cli.py]
    A --> D[run_test.py]
```