import argparse
import os
from src.Paraview import Paraview

#### ARGUMENTOS ####
parser = argparse.ArgumentParser(description='Script of paraview to get images of .obj file')
parser.add_argument('-i', '--input', type=str, help='Path to .obj input file.', required=True)
parser.add_argument('-o', '--output', type=str, help='Path directory to store images of .obj file.', required=True)
parser.add_argument('-s', '--size', type=int, help='Images size, square output', required=False, default=4000)
parser.add_argument('-n', '--numberImages', type=int, help='Quantity of images per rotation. || Cantidad de imágenes por giro.', required=False, default=60)
parser.add_argument('-r', '--numberRotations', type=int, help='Quantity of ratations. || Cantidad de giros.', required=False, default=5)
parser.add_argument('-a', '--anglePerRotation', type=int, help='Angle difference between two rotations. In ° || Ángulo de diferencia entre dos rataciones (cuanto se eleva por cada rotación). En °.', required=False, default=10)
parser.add_argument('-d', '--distanceOrRadio', type=int, help='Distance between camera and object. || Distancia entre la cámara y el objeto.', required=False, default=60)
parser.add_argument('--initMovement', type=int, help='The angle where starts the movement for each rotation. || El ángulo donde arranca el movimiento para cada rotación', required=False, default=0)
parser.add_argument('--endMovement', type=int, help='The angle where ends the movement for each rotation. || El ángulo donde termina el movimiento para cada rotación', required=False, default=0)
parser.add_argument('--cantStepMovement', type=int, help='The quantity of movements between angles defined in movement. || La cantidad de movimiento entre los ángulso de movimiento', required=False, default=1)
parser.add_argument('-v', '--verbose', help='Show info of steps. || Mostrar información de los pasos', action='store_true', required=False, default=False)
args = parser.parse_args()

## CREATE OUTPUT DIRECTORY
if not os.path.exists(args.output):
    os.makedirs(args.output)

if __name__ == '__main__':
    pv = Paraview(
            input=args.input, 
            size=args.size, 
            numberImages=args.numberImages, 
            numberRotations=args.numberRotations, 
            anglePerRotation=args.anglePerRotation, 
            radius=args.distanceOrRadio, 
            output=args.output,
            init_azimut=args.initMovement,
            end_azimut=args.endMovement,
            cant_step_azimut=args.cantStepMovement,
            verbose=args.verbose,
            )
    pv.start()
