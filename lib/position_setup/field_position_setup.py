from configuration.configuration import Configuration
from lib.position_setup.position_setup import PositionSetup
from lib.utils.field_utils import FieldUtils

class FieldPositionSetup(PositionSetup):
    def get_position_function(self, args = None):
        return lambda: FieldUtils.get_random_position_inside_field(
            Configuration.field_length,
            Configuration.field_width)
