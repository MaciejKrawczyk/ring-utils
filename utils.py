# utils for stelmach rings

import math
from pipes import *


def cut_raw(material_density: str, raw_size: float,
            raw_width: float, raw_height: float):

    margin = 0.2

    pipes_to_cut = {
        'S18': 76,
        'S1': 82,
        'S2': 84,
        'S3': 83,
        'S4': 82
    }
    # the ratio between cut ring from pipe and final ring

    upsetting = {
        4.5: 7.5,
        5: 8.3,
        5.5: 9.1,
        6: 9.9,
        6.5: 10.8,
        7: 11.6
    }
    # { size_after_upsetting: size_before_upsetting }

    good_pipes = {}
    material_density = material_density.upper()
    pipes = MATERIAL_DENSITY_PIPES[material_density]
    available_pipes = list(set(pipes_to_cut.keys()).intersection(pipes))
    available_pipes.sort()
    if 'S1' in available_pipes and 'S18' in available_pipes:
        available_pipes[0], available_pipes[1] = available_pipes[1], available_pipes[0]
    # swapping two pipes in list because of wrong sorting by python function
    # print(available_pipes)
    height_of_pipe = 3
    raw_cut_width = margin + raw_width
    raw_size_in_mm = raw_size / math.pi
    for pipe in available_pipes:
        diam_inside = PIPES[pipe][0]
        # calculating the volume of the ring and cut pipe
        v_ring = (((raw_size_in_mm + 2 * raw_height) / 2) *
                  ((raw_size_in_mm + 2 * raw_height) / 2) * raw_width * math.pi) - \
                 (raw_size_in_mm / 2) * (raw_size_in_mm / 2) * raw_width * math.pi
        v_raw_cut = (((diam_inside + 2 * height_of_pipe) / 2) *
                     ((diam_inside + 2 * height_of_pipe) / 2) * raw_cut_width * math.pi) - \
                    (diam_inside / 2) * (diam_inside / 2) * raw_cut_width * math.pi
        # calculating the ratio between ring and cut pipe
        percent = (v_ring / v_raw_cut) * 100
        percent_for_good_pipe = pipes_to_cut[pipe]
        if percent <= percent_for_good_pipe:
            print(f'stosunek gotowej do odciętej: {math.ceil(percent)}%')
            good_pipes[pipe] = ('raw_cut', raw_cut_width)

    if len(good_pipes) == 0:
        if 'S18' in available_pipes:
            for width in upsetting.keys():
                if width >= raw_width:
                    good_pipes['S18'] = ('upsetting', upsetting[width])
                    break
    # print(good_pipes)
    return good_pipes

def get_pipe(raw_size: float, raw_width: float,
             raw_height: float, material_density: str,
             multicolor=False) -> dict:
    """
    function based on volume of two rings determines the size of pipe
    returns a dictionary -> { pipe: (,,type_of_cut'', width) },
    where ,,type_of_cut'' ->
    -------------------------
    :raw_cut - cut from pipes, must be manually processed
    :upsetting - only "S18"! needs to go to the upsetting press
    :normal_cut - can be cut from pipes without manual processing
    -------------------------
    """
    size = raw_size
    width = raw_width
    height = raw_height
    material_density = material_density.upper()

    small_diameter = size / math.pi
    large_diameter = small_diameter + 2 * height

    pipes = MATERIAL_DENSITY_PIPES[material_density]

    if multicolor:
        cut_raw(material_density, size, width, height)
    else:
        for pipe in pipes:
            dimension = PIPES[pipe]
            if small_diameter > dimension[0] and large_diameter < dimension[-1]:
                # print({pipe: ('normal_cut', raw_width)})
                return {pipe: ('normal_cut', raw_width)}
        return cut_raw(material_density, size, width, height)


print(get_pipe(57, 3.3, 1.9, 'r585'))
