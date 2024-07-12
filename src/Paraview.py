
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
    def calculate_new_position(self, angle_azimut, angle_elevation, radius, center):
      '''
      Función para calcular la nueva posición de la cámara basada en ángulos
      '''
      x = center[0] + radius * cos(radians(angle_elevation)) * cos(radians(angle_azimut))
      y = center[1] + radius * cos(radians(angle_elevation)) * sin(radians(angle_azimut))
      z = center[2] + radius * sin(radians(angle_elevation))
      return [x, y, z]
    def save_screenshot(self, filename, view, image_resolution=[3000, 3000]):
        """
        Guarda una captura de pantalla de la vista actual.
        """
        SaveScreenshot( 
                        filename, 
                        viewOrLayout=view,
                        ImageResolution=image_resolution,
                        FontScaling='Scale fonts proportionally',
                        OverrideColorPalette='WhiteBackground',
                        StereoMode='No change',
                        TransparentBackground=0,
                        SaveInBackground=1,
                        EmbedParaViewState=0, 
                        # PNG options
                        CompressionLevel='5',
                        MetaData=['Application', 'ParaView']
                       )
    def start(self):
        """
        proccess to get images
        """
        for rotation in range(self.numberRotations):
          print("Rotación: ", rotation)
          for i in range(self.numberimages):
            angulo_elevacion = ((-1*self.numberRotations/2) + rotation) * self.anglePerRotation
            angulo_azimut = (360 / self.numberimages) * i
            print("Ángulo azimut: ", angulo_azimut)
            print("Ángulo elevación: ", angulo_elevacion)
            # Calcula la nueva posición de la cámara
            nueva_posicion = self.calculate_new_position(angulo_azimut, angulo_elevacion, self.radius, self.center)
            # print(nueva_posicion)
            # Aplica la nueva posición de la cámara
            self.renderView.CameraPosition = nueva_posicion
            self.renderView.CameraViewUp = [0, 0, 1]  # Ajusta si es necesario
            print(f"{self.output}{(i+(self.numberimages*(rotation))):04}.png")
            #  save screenshot
            self.save_screenshot(f"{self.output}{(i+(self.numberimages*rotation)):04}.png", self.renderView, [self.size, self.size])
            
            print("impreso")
        