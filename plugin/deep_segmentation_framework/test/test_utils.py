import os

from qgis.core import QgsVectorLayer, QgsProject
from qgis.core import QgsCoordinateReferenceSystem, QgsRectangle, QgsApplication
from qgis.core import QgsRasterLayer

from deep_segmentation_framework.common.channels_mapping import ChannelsMapping, ImageChannelStandaloneBand

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, 'data'))


def get_dummy_model_path():
    """
    Get path of a dummy onnx model. See details in README in model directory.
    Model used for unit tests processing purposes
    """
    return os.path.join(TEST_DATA_DIR, 'dummy_model', 'dummy_model.onnx')


def get_dummy_fotomap_small_path():
    """
    Get path of dummy fotomap tif file, which can be used
    for testing with conjunction with dummy_mode (see get_dummy_model_path)
    """
    return os.path.join(TEST_DATA_DIR, 'dummy_fotomap_small.tif')


def get_dummy_fotomap_area_path():
    """
    Get path of the file with processing area polygon, for dummy_fotomap (see get_dummy_fotomap_small_path)
    """
    return os.path.join(TEST_DATA_DIR, 'dummy_fotomap_area.gpkg')


def create_rlayer_from_file(file_path):
    """
    Create raster layer from tif file and add it to current QgsProject
    """
    rlayer = QgsRasterLayer(file_path, 'fotomap')
    if rlayer.width() == 0:
        raise Exception("0 width - rlayer not loaded properly. Probably invalid file path?")
    rlayer.setCrs(QgsCoordinateReferenceSystem("EPSG:32633"))
    QgsProject.instance().addMapLayer(rlayer)
    return rlayer


def create_vlayer_from_file(file_path):
    """
    Create vector layer from geometry file and add it to current QgsProject
    """
    vlayer = QgsVectorLayer(file_path)
    if not vlayer.isValid():
        raise Exception("Invalid vlayer! Probably invalid file path?")
    QgsProject.instance().addMapLayer(vlayer)
    return vlayer


def create_default_input_channels_mapping_for_rgba_bands():
    channels_mapping = ChannelsMapping()
    channels_mapping.set_number_of_model_inputs(3)
    channels_mapping.set_image_channels(
        [
            ImageChannelStandaloneBand(band_number=1, name='red'),
            ImageChannelStandaloneBand(band_number=2, name='green'),
            ImageChannelStandaloneBand(band_number=3, name='blue'),
            ImageChannelStandaloneBand(band_number=0, name='alpha'),
        ]
    )
    return channels_mapping


def init_qgis():
    qgs = QgsApplication([b''], False)
    qgs.setPrefixPath('/usr/bin/qgis', True)
    qgs.initQgis()
    return qgs
