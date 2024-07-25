# ParaView controller

#### import the simple module from the paraview
from typing import List
from paraview.simple import *
from math import sin, cos, radians
from src.utils import *


class Paraview:
    def __init__(
        self,
        input: str,
        size: int,
        numberImages: int,
        numberRotations: int,
        anglePerRotation: int,
        radius: int,
        output: str,
        verbose: int,
        init_azimut: int,
        end_azimut: int,
        cant_step_azimut: int,
    ) -> None:
        """
        Inicializa ParaView
        """

        # disable automatic camera reset on 'Show'
        paraview.simple._DisableFirstRenderCameraReset()

        # Delete all sources from view
        sources = GetSources()
        for key, source in sources.items():
            Delete(source)

        # load model
        self.model = OpenDataFile(input)

        # force active source
        SetActiveSource(self.model)

        # get active view
        self.renderView = GetActiveViewOrCreate("RenderView")

        # unable viewOrientation ui
        self.renderView.OrientationAxesVisibility = 0

        # Display model in view
        self.display = Show(self.model, self.renderView)

        # set color to object
        self.set_object_color([1.0, 1.0, 1.0])  # white

        ResetCamera(self.renderView)

        # set background color to black
        self.set_background_color([0.0, 0.0, 0.0])  # black

        # activate ilumination
        self.activate_ilumination(0.5, 0.5)

        # get layout
        self.layout1 = GetLayout()

        # set layout size in pixels
        self.layout1.SetSize(size, size)

        ## save params
        self.size = size
        self.radius = radius
        self.numberImages = numberImages
        self.numberRotations = numberRotations
        self.anglePerRotation = anglePerRotation
        self.output = output
        self.verbose = verbose
        self.init_azimut = init_azimut
        self.end_azimut = end_azimut
        self.cant_step_azimut = cant_step_azimut
        self.center = self.renderView.CameraFocalPoint

    def set_background_color(self, color: List[float]):
        """
        Set background color
        """
        if len(color) != 3:
            raise ValueError(
                "The 'color' list must contain exactly three float numbers."
            )
        self.renderView.Background = color

    def set_object_color(self, color: List[float]):
        """
        Set coor of object in scene
        """
        if len(color) != 3:
            raise ValueError(
                "The 'color' list must contain exactly three float numbers."
            )
        self.display.DiffuseColor = color

    def activate_ilumination(self, principal_light=0.5, fill_light=0.5):
        """
        Activate ilumination
        """
        self.renderView.UseLight = 1  # Activate use of light
        self.renderView.KeyLightWarmth = (
            principal_light  # adjust the color temperature of principal light
        )
        self.renderView.FillLightWarmth = (
            fill_light  # adjust the color temperature of fill light
        )

    def set_camera_position(self, position: List[float]):
        """
        Set position of the camera
        """
        if len(position) != 3:
            raise ValueError(
                "The 'position' list must contain exactly three float numbers."
            )
        self.renderView.CameraPosition = position

    def calculate_new_position(
        self,
        angle_azimut: float,
        angle_elevation: float,
        radius: int,
        center: List[float],
    ) -> List[float]:
        """
        Calculate new position based on angles
        """
        x = center[0] + radius * cos(radians(angle_elevation)) * cos(
            radians(angle_azimut)
        )
        y = center[1] + radius * cos(radians(angle_elevation)) * sin(
            radians(angle_azimut)
        )
        z = center[2] + radius * sin(radians(angle_elevation))
        return [x, y, z]

    def save_screenshot(self, filename, view, image_resolution=[3000, 3000]):
        """
        Save screenshots of view
        """
        SaveScreenshot(
            filename,
            viewOrLayout=view,
            ImageResolution=image_resolution,
            FontScaling="Scale fonts proportionally",
            OverrideColorPalette="BlackBackground",
            StereoMode="No change",
            TransparentBackground=0,
            SaveInBackground=1,
            EmbedParaViewState=0,
            # PNG options
            CompressionLevel="5",
            MetaData=["Application", "ParaView"],
        )

    def start(self):
        """
        Get images from .obj file
        """
        # get angles for each rotation --- [-10.0, 0.0, 10.0]
        rotation_angles = get_angles_for_rotation(
            self.numberRotations, self.anglePerRotation
        )
        if self.verbose:
            print("The 'vertical' angles for each rotation are:  ", rotation_angles)

        # get the angles of azimut movement
        angles_azimuth_inits = get_angles_for_azimut_init(
            self.init_azimut, self.end_azimut, self.cant_step_azimut
        )
        if self.verbose:
            print("The movements angles for each rotation are:  ", angles_azimuth_inits)

        # cicle over each rotation with its angle
        for rotation, elevation_angle in enumerate(rotation_angles):
            if self.verbose:
                print("Rotation: ", rotation)
                print("Angle of elevation: ", rotation)

            # cicle over the azimut angle for movements
            for _, azimuth_angle_init in enumerate(angles_azimuth_inits):

                angles = get_angles_for_azimut_from_init_angle(
                    azimuth_angle_init, self.numberImages
                )

                if self.verbose:
                    print(" Starting for angle movement: ", azimuth_angle_init)
                    print(" Taking pictures for angles: ", azimuth_angle_init)

                # cicle over each angle to take picture
                for idx_angle_azimut, final_azimuth_angle in enumerate(angles):
                    new_position = self.calculate_new_position(
                        final_azimuth_angle, elevation_angle, self.radius, self.center
                    )
                    self.set_camera_position(new_position)
                    self.renderView.CameraViewUp = [0, 0, 1]  # Adjust
                    #  save screenshot
                    self.save_screenshot(
                        f"{self.output}/rot{rotation:04}_mov_{azimuth_angle_init:03}_angle{idx_angle_azimut:03}.png",
                        self.renderView,
                        [self.size, self.size],
                    )
                    if self.verbose:
                        print(
                            "impreso",
                            f"{self.output}/rot{rotation:04}_mov_{azimuth_angle_init:03}_angle{idx_angle_azimut:03}.png",
                        )
