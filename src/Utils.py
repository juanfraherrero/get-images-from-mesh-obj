import os
from PIL import Image 
from tqdm import tqdm

def get_angles_for_rotation (rotations, angle):
  """
    Calcualte the angles for each rotation
    returns a list with the angles
    [-10.0, 0.0, 10.0]
  """
  angles = []
  avgRotations = (rotations + 1)/2
  for rotation in range(rotations):
    angulo_elevacion = (0 + (rotation + 1 - avgRotations)* angle)
    angles.append(angulo_elevacion)
  return angles


def get_angles_for_azimut_init (init, end, cant_steps):
  """
    Calcualte the angles for azimut movement
    returns a list with the angles azimuth starting in init, ending in end and with cant_steps quantity of angles
    - Example:
    get_angles_for_azimut_init(0, 90, 10) -> [0.0, 9.0, 18.0, 27.0, 36.0, 45.0, 54.0, 63.0, 72.0, 81.0]
  """
  angles = []

  for step in range(cant_steps):
    angle = (end - init) / cant_steps
    angulo_elevacion = (init + step * angle)
    angles.append(angulo_elevacion)
  return angles

def get_angles_for_azimut_from_init_angle(init, cant_steps):
  """
    Calcualte the angles for azimut movement from init and with quantity of steps
    returns a list with the angles azimuth starting in init
    - Example:
    get_angles_for_azimut_from_init_angle(0, 4) -> [0.0, 90.0, 180.0, 270.0]
  """
  angles = []
  # cicle over each image
  for i in range(cant_steps):
    # Calcula la nueva posición de la cámara
    angulo_azimut = init + (360 / cant_steps) * i
    angles.append(angulo_azimut)
  return angles

def convert_images_to_black_and_white(folder_path):
  """
  Convert all images in the folder to black and white
  """

  fold = os.listdir(folder_path)
  progress_bar_folder = tqdm(total=len(os.listdir(folder_path)), desc='Processing folders', unit='folder', leave=False)
  for sub_folder in fold:
    image_folder = os.path.join(folder_path, sub_folder, "images")
    for image in os.listdir(image_folder):
      try:
        image_path = os.path.join(image_folder, image)
        img = Image.open(image_path).convert('L')
        img.save(image_path)
      except:
        print("Error with image: ", image_path)
        print("Deleting dataset: ", sub_folder)
        os.system(f"rm -rf {os.path.join(folder_path, sub_folder)}")
        break
    progress_bar_folder.update(1)
  progress_bar_folder.close()