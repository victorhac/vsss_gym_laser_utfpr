from configuration.configuration import Configuration
from lib.builders.robot_curriculum_behavior_builder import RobotCurriculumBehaviorBuilder
from lib.domain.ball_curriculum_behavior import BallCurriculumBehavior
from lib.domain.curriculum_task import CurriculumTask
from lib.domain.enums.position_enum import PositionEnum
from lib.domain.enums.role_enum import RoleEnum

class TeamBehaviorUtils:  
    @staticmethod
    def get_task_3(
        update_count: int = 0,
        updates_per_task: int = 10,
        games_count: int = 10,
        default_threshold: float = .8
    ):    
        behaviors = [
            TeamBehaviorUtils.get_own_team_multiple_role_behavior(
                0,
                PositionEnum.OWN_AREA_EXCEPT_GOAL_AREA,
                updates_per_task),
            TeamBehaviorUtils.get_own_team_multiple_role_behavior(
                1,
                PositionEnum.OWN_AREA_EXCEPT_GOAL_AREA,
                updates_per_task),
            TeamBehaviorUtils.get_own_team_multiple_role_behavior(
                2,
                PositionEnum.OWN_AREA_EXCEPT_GOAL_AREA,
                updates_per_task)
        ]

        ball_behavior = TeamBehaviorUtils.get_ball_behavior(
            PositionEnum.RELATIVE_TO_OPPONENT_GOAL,
            updates_per_task,
            (.2, 1.35)
        )

        return CurriculumTask(
            "3",
            behaviors,
            ball_behavior,
            update_count=update_count,
            updates_per_task=updates_per_task,
            games_count=games_count,
            default_threshold=default_threshold)
    
    @staticmethod
    def get_task_10(
        update_count: int = 0,
        updates_per_task: int = 20,
        games_count: int = 20,
        default_threshold: float = .8
    ):    
        behaviors = [
            TeamBehaviorUtils.get_own_team_multiple_role_behavior(
                0,
                PositionEnum.OWN_AREA_EXCEPT_GOAL_AREA,
                updates_per_task),
            TeamBehaviorUtils.get_own_team_multiple_role_behavior(
                1,
                PositionEnum.OWN_AREA_EXCEPT_GOAL_AREA,
                updates_per_task),
            TeamBehaviorUtils.get_own_team_multiple_role_behavior(
                2,
                PositionEnum.OWN_AREA_EXCEPT_GOAL_AREA,
                updates_per_task),
            TeamBehaviorUtils.get_opponent_team_from_fixed_model_behavior(
                RoleEnum.ATTACKER,
                0,
                updates_per_task,
                (0, 1))
        ]

        ball_behavior = TeamBehaviorUtils.get_ball_behavior(
            PositionEnum.RELATIVE_TO_OPPONENT_GOAL,
            updates_per_task,
            (.2, 1.35)
        )

        return CurriculumTask(
            "10",
            behaviors,
            ball_behavior,
            update_count=update_count,
            updates_per_task=updates_per_task,
            games_count=games_count,
            default_threshold=default_threshold)

    @staticmethod
    def get_task_11(
        update_count: int = 0,
        updates_per_task: int = 20,
        games_count: int = 20,
        default_threshold: float = .6
    ):    
        behaviors = [
            TeamBehaviorUtils.get_own_team_multiple_role_behavior(
                0,
                PositionEnum.OWN_AREA_EXCEPT_GOAL_AREA,
                updates_per_task),
            TeamBehaviorUtils.get_own_team_multiple_role_behavior(
                1,
                PositionEnum.OWN_AREA_EXCEPT_GOAL_AREA,
                updates_per_task),
            TeamBehaviorUtils.get_own_team_multiple_role_behavior(
                2,
                PositionEnum.OWN_AREA_EXCEPT_GOAL_AREA,
                updates_per_task),
            TeamBehaviorUtils.get_opponent_team_from_fixed_model_behavior(
                RoleEnum.ATTACKER,
                0,
                updates_per_task,
                (0, 1)),
            TeamBehaviorUtils.get_opponent_team_from_fixed_model_behavior(
                RoleEnum.DEFENDER,
                1,
                updates_per_task,
                (0, 1))
        ]

        ball_behavior = TeamBehaviorUtils.get_ball_behavior(
            PositionEnum.RELATIVE_TO_OPPONENT_GOAL,
            updates_per_task,
            (.2, 1.35)
        )

        return CurriculumTask(
            "11",
            behaviors,
            ball_behavior,
            update_count=update_count,
            updates_per_task=updates_per_task,
            games_count=games_count,
            default_threshold=default_threshold)
    
    @staticmethod
    def get_task_12(
        update_count: int = 0,
        updates_per_task: int = 20,
        games_count: int = 20,
        default_threshold: float = .5
    ):    
        behaviors = [
            TeamBehaviorUtils.get_own_team_multiple_role_behavior(
                0,
                PositionEnum.OWN_AREA_EXCEPT_GOAL_AREA,
                updates_per_task),
            TeamBehaviorUtils.get_own_team_multiple_role_behavior(
                1,
                PositionEnum.OWN_AREA_EXCEPT_GOAL_AREA,
                updates_per_task),
            TeamBehaviorUtils.get_own_team_multiple_role_behavior(
                2,
                PositionEnum.OWN_AREA_EXCEPT_GOAL_AREA,
                updates_per_task),
            TeamBehaviorUtils.get_opponent_team_from_fixed_model_behavior(
                RoleEnum.ATTACKER,
                0,
                updates_per_task,
                (0, 1)),
            TeamBehaviorUtils.get_opponent_team_from_fixed_model_behavior(
                RoleEnum.DEFENDER,
                1,
                updates_per_task,
                (0, 1)),
            TeamBehaviorUtils.get_opponent_team_from_fixed_model_behavior(
                RoleEnum.GOALKEEPER,
                2,
                updates_per_task,
                (0, 1))
        ]

        ball_behavior = TeamBehaviorUtils.get_ball_behavior(
            PositionEnum.RELATIVE_TO_OPPONENT_GOAL,
            updates_per_task,
            (.2, 1.35)
        )

        return CurriculumTask(
            "9",
            behaviors,
            ball_behavior,
            update_count=update_count,
            updates_per_task=updates_per_task,
            games_count=games_count,
            default_threshold=default_threshold)

    @staticmethod
    def get_ball_behavior(
        position_enum: PositionEnum,
        updates_per_task: int,
        distance_range: 'tuple[float, float]'
    ):
        return BallCurriculumBehavior(
            position_enum=position_enum,
            updates_per_task=updates_per_task,
            distance_range=distance_range)
    
    @staticmethod
    def get_own_team_multiple_role_behavior(
        robot_id: int,
        position_enum: PositionEnum,
        updates_per_task: int,
        distance_range: 'tuple[float, float] | None' = None
    ):
        builder = RobotCurriculumBehaviorBuilder(
            robot_id,
            False,
            updates_per_task
        )

        return builder\
            .set_multiple_role_behavior()\
            .set_position_enum(position_enum)\
            .set_distance_range(distance_range)\
            .build()
    
    @staticmethod
    def get_opponent_team_from_fixed_model_behavior(
        role_enum: RoleEnum,
        robot_id: int,
        updates_per_task: int,
        velocity_alpha_range: 'tuple[float, float]'
    ):
        builder = RobotCurriculumBehaviorBuilder(
            robot_id,
            True,
            updates_per_task
        )

        if role_enum == RoleEnum.DEFENDER:
            model_path = Configuration.model_defender_path
        elif role_enum == RoleEnum.GOALKEEPER:
            model_path = Configuration.model_goalkeeper_path
        else:
            model_path = Configuration.model_attacker_path

        if role_enum == RoleEnum.GOALKEEPER:
            position_enum = PositionEnum.OWN_GOAL_AREA
        else:
            position_enum = PositionEnum.OWN_AREA_EXCEPT_GOAL_AREA

        return builder\
            .set_from_fixed_model_behavior(model_path, role_enum)\
            .set_position_enum(position_enum)\
            .set_velocity_alpha_range(velocity_alpha_range)\
            .build()
