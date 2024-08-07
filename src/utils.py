def get_angles_for_rotation(rotations, angle):
    """
    Calcualte the angles for each rotation
    returns a list with the angles
    [-10.0, 0.0, 10.0]
    """
    angles = []
    avgRotations = (rotations + 1) / 2
    for rotation in range(rotations):
        angulo_elevacion = 0 + (rotation + 1 - avgRotations) * angle
        angles.append(angulo_elevacion)
    return angles


def get_angles_for_azimut_init(init, end, cant_steps):
    """
    Calcualte the angles for azimut movement
    returns a list with the angles azimuth starting in init, ending in end and with cant_steps quantity of angles
    - Example:
    get_angles_for_azimut_init(0, 90, 10) -> [0.0, 9.0, 18.0, 27.0, 36.0, 45.0, 54.0, 63.0, 72.0, 81.0]
    """
    if (not isinstance(init, (int, float))) or (not isinstance(end, (int, float))):
        return [0.0]

    if cant_steps == 0:
        return [init]

    if init == end:
        return [init] * cant_steps  # return cant_steps of init

    angles = []

    for step in range(cant_steps):
        angle = (end - init) / cant_steps
        angulo_elevacion = init + step * angle
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
