import cfdm


class NCDataset(object):
    """
    The main class for this module to create a netCDF file with CF/ACDD conventions
    """

    def __init__(self, template_file, data_dict, ancillary_dict, metadata_dict):
        """
        Init the dataset object.
        :param template_file: Link to the yaml template file
        :param data_dict: A dictionary(-like) object including all fields with the field name as key
        :param ancillary_dict: A dictionary(-like) object including all ancillary fields (dimensions)
        :param metadata_dict: A dictionay(-like) object containing all metadata fields necessary to create
            attributes
        """

        # Store properties
        self.template_file = template_file
        self.data_dict = data_dict
        self.metadata_dict = metadata_dict

        # Init the CF data model
        self.fields = cfdm.F