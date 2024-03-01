#
#
# class _ACDDModelv1p3(object):
#     """
#     Data class containing the list of highly recommend, recommended and suggest attributes
#     according to the  Attribute Convention for Data Discovery (ACDD) version 1.3:
#
#         https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3
#     """
#
#     def __init__(self):
#         """
#
#         """
#         pass
#
#     @property
#     def hrec(self):
#         attr_list = [DatasetAttribute("title"),
#                      DatasetAttribute("summary"),
#                      DatasetAttribute("keywords"),
#                      DatasetAttribute("Conventions", default_value="ACDD-1.3")]
#         return attr_list
#
#     @property
#     def rec(self):
#         attr_list = [DatasetAttribute("id"),
#                      DatasetAttribute("naming_authority"),
#                      DatasetAttribute("history"),
#                      DatasetAttribute("source"),
#                      DatasetAttribute("processing_level"),
#                      DatasetAttribute("comment"),
#                      DatasetAttribute("acknowledgement"),
#                      DatasetAttribute("license"),
#                      DatasetAttribute("standard_name_vocabulary"),
#                      DatasetAttribute("date_created", validator_type="datetime"),
#                      DatasetAttribute("creator_name"),
#                      DatasetAttribute("creator_email"),
#                      DatasetAttribute("creator_url"),
#                      DatasetAttribute("institution"),
#                      DatasetAttribute("project"),
#                      DatasetAttribute("publisher_name"),
#                      DatasetAttribute("publisher_email"),
#                      DatasetAttribute("publisher_url"),
#                      DatasetAttribute("geospatial_bounds"),
#                      DatasetAttribute("geospatial_bounds_crs"),
#                      DatasetAttribute("geospatial_bounds_vertical_crs"),
#                      DatasetAttribute("geospatial_lat_min"),
#                      DatasetAttribute("geospatial_lat_max"),
#                      DatasetAttribute("geospatial_lon_min"),
#                      DatasetAttribute("geospatial_lon_max"),
#                      DatasetAttribute("geospatial_vertical_min"),
#                      DatasetAttribute("geospatial_vertical_max"),
#                      DatasetAttribute("geospatial_vertical_positive"),
#                      DatasetAttribute("time_coverage_start", validator_type="datetime"),
#                      DatasetAttribute("time_coverage_end", validator_type="datetime"),
#                      DatasetAttribute("time_coverage_duration", validator_type="duration"),
#                      DatasetAttribute("time_coverage_resolution", validator_type="duration")]
#         return attr_list
#
#     @property
#     def sug(self):
#         attr_list = [DatasetAttribute("creator_type"),
#                      DatasetAttribute("creator_institution"),
#                      DatasetAttribute("publisher_type"),
#                      DatasetAttribute("publisher_institution"),
#                      DatasetAttribute("program"),
#                      DatasetAttribute("contributor_name"),
#                      DatasetAttribute("contributor_role"),
#                      DatasetAttribute("geospatial_lat_units"),
#                      DatasetAttribute("geospatial_lat_resolution"),
#                      DatasetAttribute("geospatial_lon_units"),
#                      DatasetAttribute("geospatial_lon_resolution"),
#                      DatasetAttribute("geospatial_vertical_units"),
#                      DatasetAttribute("geospatial_vertical_resolution"),
#                      DatasetAttribute("date_modified", validator_type="datetime"),
#                      DatasetAttribute("date_issued", validator_type="datetime"),
#                      DatasetAttribute("date_metadata_modified", validator_type="datetime"),
#                      DatasetAttribute("product_version"),
#                      DatasetAttribute("keywords_vocabulary"),
#                      DatasetAttribute("platform"),
#                      DatasetAttribute("platform_vocabulary"),
#                      DatasetAttribute("instrument"),
#                      DatasetAttribute("instrument_vocabulary"),
#                      DatasetAttribute("cdm_data_type"),
#                      DatasetAttribute("metadata_link"),
#                      DatasetAttribute("references")]
#         return attr_list
#
#
# class DatasetAttribute(object):
#     """
#     A data class for a global attribute, contains name, value, default value and validator_type
#     """
#
#     def __init__(self, name, value=None, default_value=None, validator_type=None):
#         """
#         Create an instance for a global attribute.
#         :param name:
#         :param value:
#         :param default_value:
#         :param validator_type:
#         """
#
#         # Args
#         self._name = name
#         self._value = value
#         self.default_value = value
#         self.validator_type = validator_type
#
#     @property
#     def name(self):
#         return str(self._name)
#
#     @property
#     def value(self):
#         if self._value is None and self.default_value is not None:
#             return self.default_value
#         else:
#             return self._value
#
#
