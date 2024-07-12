
import argparse
import os
from src.Paraview import Paraview
from src.Utils import get_angles_for_rotation, get_angles_for_azimut_init, get_angles_for_azimut_from_init_angle, convert_images_to_black_and_white
import json
import shutil
from tqdm import tqdm
import gc
from PIL import Image

# Configura el analizador de argumentos
parser = argparse.ArgumentParser(description='Script to prepare data for training of brakeBalls.')
parser.add_argument('-c', '--config', help='Ruta al archivo .json con las configuraciones ', required=True)
parser.add_argument('-t', '--test', action='store_true',  help='Booleano que fuerza a solo ejecutar el script sobre un solo objeto ')
parser.add_argument('-v', '--verbose', action='store_true', help='Imprimir info de cada impresión de la generación de imágenes')

# Analiza los argumentos de la línea de comandos
args = parser.parse_args()

def createFolder(idx, output):
    # Verifica si el directorio no existe y lo crea con la estructura adecuada
    folder_path = os.path.join(output, "dataset"+str(idx))
    folder_images = os.path.join(folder_path, "images")
    folder_object = os.path.join(folder_path, "object")

    if not os.path.exists(folder_path):
        # Si no existe, crea el directorio
        os.makedirs(folder_path)
        os.makedirs(folder_images)
        os.makedirs(folder_object)
    return folder_path, folder_images, folder_object

if __name__ == '__main__':
    #load configs
    with open(args.config) as json_file:
        config = json.load(json_file)
    number_rotations = config['number_rotations']
    cant_step_azimut = config['cant_step_azimut']
    
    # initialize the progress bar
    arr_objects = os.listdir(config['array_of_folder_with_objs'])
    progress_bar_object = tqdm(total=len(arr_objects), desc='Processing Objects', unit='object', leave=True)
        
    ## cicle over each .obj in the folder input
    for idx_object, obj_dir in enumerate(arr_objects):
        path_object = os.path.join(config['array_of_folder_with_objs'],obj_dir)
        
        # print("objeto: ", obj_dir)
        # print("folder_path: ", folder_path)
        # print("folder_images: ", folder_images)
        # print("folder_object: ", folder_object)
        
        # Create the Paraview Ob ject for each object
        pv = Paraview(input=path_object, 
                      size=config['size_for_img'], 
                      numberimages=config['number_images_per_rotation'], 
                      numberRotations=number_rotations, 
                      anglePerRotation=config['angle_per_rotation'], 
                      radius=config['distance_or_radio'], 
                      output="", # not important
                      verbose=args.verbose,
                      init_azimut=config['init_azimut'],
                      end_azimut=config['end_azimut'],
                      cant_step_azimut=cant_step_azimut,)
        # get the angles for each rotation --- [-10.0, 0.0, 10.0]
        rotation_angles = get_angles_for_rotation(number_rotations, config['angle_per_rotation'])
        # get the angles of azimut movement
        angles_azimuth_inits = get_angles_for_azimut_init(config['init_azimut'], config['end_azimut'], cant_step_azimut)
        progress_bar_rotation = tqdm(total=number_rotations, desc='Processing Rotations', unit='rotation', leave=False)
        # cicle over each rotation with its angle
        for idx_rotation, elevation_angle in enumerate(rotation_angles):
            if (args.verbose):
                print("Rotación number: ", idx_rotation)
            progress_bar_angle_init = tqdm(total=number_rotations, desc='Processing angles init', unit='angle init', leave=False)
            #cicle over the azimut angle
            for idx_angle_azimut_init, azimuth_angle_init in enumerate(angles_azimuth_inits):
                if (args.verbose):
                    print(" Ángulo azimut init: ", azimuth_angle_init)
                angles = get_angles_for_azimut_from_init_angle(azimuth_angle_init, config['number_images_per_rotation'])
                # cicle over each image
                for idx_angle_azimut, final_azimuth_angle in enumerate(angles):
                    # Calcula la nueva posición de la cámara
                    if (args.verbose):
                        print("   Ángulo azimut: ", final_azimuth_angle)
                        print("   Ángulo elevación: ", elevation_angle)   
                    idx_dataset_folder = idx_object * len(rotation_angles) * len(angles_azimuth_inits)+ idx_rotation * len(angles_azimuth_inits) + idx_angle_azimut_init 
                    folder_path, folder_images, folder_object = createFolder(idx_dataset_folder, config['output_folder'])
                    path_image = f"{folder_images}/{(idx_angle_azimut):01}.png"
                    nueva_posicion = pv.calculate_new_position(final_azimuth_angle, elevation_angle, config['distance_or_radio'])
                    pv.set_position(nueva_posicion)
                    # save image
                    pv.save_screenshot(path_image, None)
                    if (args.verbose):
                        print("impreso ", path_image)
                    # copy the object to the folder object
                    shutil.copy(path_object, folder_object+"/0.obj")
                    
                    progress_bar_angle_init.update(1)
                
                progress_bar_angle_init.close()
                # free angles
                del angles
            progress_bar_rotation.update(1)
        progress_bar_rotation.close()
        # update the progress bar
        progress_bar_object.update(1)

        # free pv
        del pv
        del angles_azimuth_inits
        del rotation_angles

        # if test is True, break the loop
        if args.test:
            break

    # end the progress bar
    progress_bar_object.close()
    
    # convert images to black and white, only one channel
    convert_images_to_black_and_white(config['output_folder'])