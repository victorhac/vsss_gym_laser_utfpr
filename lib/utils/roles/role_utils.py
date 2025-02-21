from lib.domain.enums.role_enum import RoleEnum
from lib.environment.base_environment import BaseEnvironment
from lib.utils.roles.attacker.attacker_v2_utils import AttackerV2Utils
from lib.utils.roles.attacker_utils import AttackerUtils
from lib.utils.roles.defender_utils import DefenderUtils
from lib.utils.roles.goalkeeper_utils import GoalkeeperUtils

class RoleUtils:    
    @staticmethod
    def get_speeds(
        environment: BaseEnvironment,
        role_enum: RoleEnum,
        robot_id: int,
        is_yellow: bool,
        is_left_team: bool,
        model,
        deterministic: bool = True
    ):
        if role_enum == RoleEnum.ATTACKER:
            return AttackerUtils.get_speeds(
                environment,
                robot_id,
                is_yellow,
                is_left_team,
                model,
                deterministic
            )
        elif role_enum == RoleEnum.ATTACKERV2:
            return AttackerV2Utils.get_speeds(
                environment,
                robot_id,
                is_yellow,
                is_left_team,
                model,
                deterministic
            )
        elif role_enum == RoleEnum.DEFENDER:
            return DefenderUtils.get_speeds(
                environment,
                robot_id,
                is_yellow,
                is_left_team,
                model,
                deterministic
            )
        elif role_enum == RoleEnum.GOALKEEPER:
            return GoalkeeperUtils.get_speeds(
                environment,
                robot_id,
                is_yellow,
                is_left_team,
                model,
                deterministic
            )
        
        return 0, 0
