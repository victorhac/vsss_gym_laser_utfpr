from lib.domain.position_setup_args import PositionSetupArgs

class PositionSetup:
    def get_position_function(self, args: PositionSetupArgs | None = None):
        raise NotImplementedError()
