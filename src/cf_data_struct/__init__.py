#
# import yaml
# from pathlib import Path
#
#
# class NCDataset(object):
#     """
#     The main class for this module to create a netCDF file with CF/ACDD conventions
#     """
#
#     def __init__(self, template_file, data_dict=None, ancillary_dict=None, metadata_dict=None):
#         """
#         Init the dataset object.
#         :param template_file: Link to the yaml template file
#         :param data_dict: A dictionary(-like) object including all fields with the field name as key
#         :param ancillary_dict: A dictionary(-like) object including all ancillary fields (dimensions)
#         :param metadata_dict: A dictionay(-like) object containing all metadata fields necessary to create
#             attributes
#         """
#
#         # Store properties
#         self.template_file = template_file
#         self.data_dict = data_dict
#         self.ancillary_dict = ancillary_dict
#         self.metadata_dict = metadata_dict
#         self.template = NetCDFTemplate(template_file)
#
#     def set_variable(self, field_name, data, attrs=None):
#         """
#         Add a
#         :param field_name:
#         :param data:
#         :param attrs:
#         :return:
#         """
#
#
# class NetCDFTemplate(object):
#     """
#     Container for the netCDF template
#     """
#
#     def __init__(self, filepath):
#         """
#
#         :param filepath:
#         """
#         # Properties
#         self.filepath = Path(filepath)
#         if not self.filepath.is_file():
#             raise IOError("Not a valid file: {}".format(self.filepath))
#
#         # Read the yaml file content
#         self.template = None
#         with open(str(filepath), 'r') as fileobj:
#             self.template = AttrDict(yaml.safe_load(fileobj))
