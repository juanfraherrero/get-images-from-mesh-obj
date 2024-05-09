
# ParaView controller

#### import the simple module from the paraview
from paraview.simple import *
from math import sin, cos, radians
from src.utils import *
class Paraview:
  def __init__(self, input, size, numberimages, numberRotations, anglePerRotation, radius, output, verbose, init_azimut, end_azimut, cant_step_azimut):
    """
    Inicializa ParaView.
    """
    #### disable automatic camera reset on 'Show'
    paraview.simple._DisableFirstRenderCameraReset()

    # Elimina los objetos Paraview anteriores
    # Obtiene todas las fuentes en la escena actual
    sources = GetSources()
    # Elimina cada fuente individualmente
    for key, source in sources.items():
        Delete(source)
    
    # Carga tu modelo
    self.model = OpenDataFile(input)

    # Asegúrate de que el modelo es el objeto activo
    SetActiveSource(self.model)

    # get active view
    self.renderView = GetActiveViewOrCreate('RenderView')

    # Deshabilita el eje de orientación en la vista renderizada
    self.renderView.OrientationAxesVisibility = 0

    # Display your model in the view
    self.display = Show(self.model, self.renderView)

    # set color to object
    self.set_object_color([1.0, 1.0, 1.0]) # white
    
    # Asegúrate de que toda la escena esté visible
    ResetCamera(self.renderView)

    # set background color to black
    self.set_background_color([0.0, 0.0, 0.0])

    # activate ilumination
    # self.activate_ilumination(0.5, 0.5)

    # get layout
    self.layout1 = GetLayout()

    # layout/tab size in pixels
    self.set_layout_size(size)
    # set parameters
    self.size = size
    self.radius = radius
    self.numberimages = numberimages
    self.numberRotations = numberRotations
    self.anglePerRotation = anglePerRotation
    self.output = output
    self.verbose = verbose
    self.init_azimut = init_azimut
    self.end_azimut = end_azimut
    self.cant_step_azimut = cant_step_azimut

  def interact (self):
    paraview.simple.Render()
    paraview.simple.Interact()

  def set_background_color(self, color):
    """
    Establece el color de fondo de la vista.
    """
    self.renderView.Background = color   
  def set_object_color(self, color):
    """
    Establece el color del objeto
    """
    self.display.DiffuseColor = color
  def set_layout_size(self, size):
    """
    Establece el tamaño del layout
    """
    self.layout1.SetSize(size, size)
  def activate_ilumination(self, principal_light=0.5, fill_light=0.5):
    """
    Activa o desactiva la iluminación
    """
    # Configura las propiedades de la iluminación
    self.renderView.UseLight = 1  # Activa el uso de la luz
    self.renderView.KeyLightWarmth = principal_light  # Ajusta la calidez de la luz principal
    self.renderView.FillLightWarmth = fill_light  # Ajusta la calidez de la luz de relleno
  def calculate_new_position(self, angle_azimut, angle_elevation, radius):
    '''
    Función para calcular la nueva posición de la cámara basada en ángulos
    '''
    x = self.renderView.CameraFocalPoint[0] + radius * cos(radians(angle_elevation)) * cos(radians(angle_azimut))
    y = self.renderView.CameraFocalPoint[1] + radius * cos(radians(angle_elevation)) * sin(radians(angle_azimut))
    z = self.renderView.CameraFocalPoint[2] + radius * sin(radians(angle_elevation))
    return [x, y, z]
  def save_screenshot(self, filename, image_resolution):
    """
    Guarda una captura de pantalla de la vista actual.
    """
    if image_resolution is None:
      image_resolution = [self.size, self.size]
    SaveScreenshot( 
                    filename, 
                    viewOrLayout=self.renderView,
                    ImageResolution=image_resolution,
                    FontScaling='Scale fonts proportionally',
                    OverrideColorPalette='BlackBackground',
                    StereoMode='No change',
                    TransparentBackground=0,
                    SaveInBackground=0,
                    EmbedParaViewState=0, 
                    # PNG options
                    CompressionLevel='5',
                    MetaData=['Application', 'ParaView']
                    )
  def set_position(self, new_position):
    """
    Establece la posición de la cámara
    """
    self.renderView.CameraPosition = new_position
    self.renderView.CameraViewUp = [0, 0, 1]  # Ajusta si es necesario
  def start(self):
    """
    proccess to get images
    """
    # get the angles for each rotation --- [-10.0, 0.0, 10.0]
    rotation_angles = get_angles_for_rotation(self.numberRotations, self.anglePerRotation)
    print(rotation_angles)
    # get the angles of azimut movement
    angles_azimuth_inits = get_angles_for_azimut_init(self.init_azimut, self.end_azimut, self.cant_step_azimut)

    # cicle over each rotation with its angle
    for rotation, elevation_angle in enumerate(rotation_angles):
      if (self.verbose):
        print("Rotación number: ", rotation)
      
      #cicle over the azimut angle
      for idx_angle_azimut_init, azimuth_angle_init in enumerate(angles_azimuth_inits):
        if (self.verbose):
          print(" Ángulo azimut init: ", azimuth_angle_init)

        angles = get_angles_for_azimut_from_init_angle(azimuth_angle_init, self.numberimages)

        # cicle over each image
        for idx_angle_azimut, final_azimuth_angle in enumerate(angles):
          # Calcula la nueva posición de la cámara
          if (self.verbose):
            print("   Ángulo azimut: ", final_azimuth_angle)
            print("   Ángulo elevación: ", elevation_angle)
          nueva_posicion = self.calculate_new_position(final_azimuth_angle, elevation_angle, self.radius)
          
          # apply the new position to the camera
          self.renderView.CameraPosition = nueva_posicion
          self.renderView.CameraViewUp = [0, 0, 1]  # Ajusta si es necesario
          if (self.verbose):
            print(f"{self.output}/{(idx_angle_azimut+(self.numberimages*(rotation))):04}.png")
          #  save screenshot
          self.save_screenshot(f"{self.output}/{(i+(self.numberimages*rotation)):04}.png", self.renderView, [self.size, self.size])
          if (self.verbose):        
            print("impreso")
  
  
  def test(self):
    """
    proccess to get images
    """

    while True :
      # # Aplicar una transformación
      # transform = paraview.simple.Transform(Input=self.model)
      # transform.Transform = 'Transform'

      # # Configurar la rotación sobre el eje X en 10 grados
      # transform.Transform.Rotate = [90, 0, 0]  # [RotateX, RotateY, RotateZ]

      # # Asegurarse de centrar la rotación en el objeto
      # # transform.Center = self.model.center

      # # Actualizar el pipeline para aplicar la transformación
      # # transform.UpdatePipeline()
      # # Asegúrate de actualizar y mostrar el objeto transformado
      # self.display = paraview.simple.Show(transform, self.renderView)
      # paraview.simple.Render()  
       
      self.interact()