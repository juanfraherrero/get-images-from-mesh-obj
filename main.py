
from math import sin, cos, radians
import argparse
import os
from src.Paraview import Paraview
# Configura el analizador de argumentos
parser = argparse.ArgumentParser(description='Script of paraview for get images of .obj')
parser.add_argument('-i', '--input', help='Ruta al archivo .obj de entrada.', required=True)
parser.add_argument('-o', '--output', help='Ruta a la carpeta donde estaran las imágenes resultantes.', required=True)
parser.add_argument('-s', '--size', help='Tamaño de la imagen de salida en pixels, es cuadrada', required=False, default=4000)
parser.add_argument('-n', '--numberimages', type=int, help='Cantidad de imágenes por giro', required=False, default=60)
parser.add_argument('-r', '--numberRotations', type=int, help='Cantidad de giros', required=False, default=5)
parser.add_argument('-a', '--anglePerRotation', type=int, help='cuanto se eleva por cada rotación', required=False, default=10)

# Analiza los argumentos de la línea de comandos
args = parser.parse_args()

# Verifica si el sirectorio no existe y lo crea
if not os.path.exists(args.output):
    # Si no existe, crea el directorio
    os.makedirs(args.output)

if __name__ == '__main__':
    pv = Paraview(input=args.input, size=args.size, numberimages=args.numberimages, numberRotations=args.numberRotations, anglePerRotation=args.anglePerRotation, radius=60, output=args.output)
    pv.start()