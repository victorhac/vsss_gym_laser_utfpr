from configuration.configuration import Configuration
from lib.builders.robot_curriculum_behavior_builder import RobotCurriculumBehaviorBuilder
from lib.domain.ball_curriculum_behavior import BallCurriculumBehavior
from lib.domain.curriculum_task import CurriculumTask
from lib.domain.enums.role_enum import RoleEnum
from lib.position_setup.area_except_goal_area_position_setup import AreaExceptGoalAreaPositionSetup
from lib.position_setup.fixed_position_setup import FixedPositionSetup
from lib.position_setup.goal_area_position_setup import GoalAreaPositionSetup
from lib.position_setup.position_setup import PositionSetup
from lib.position_setup.relative_to_goal_position_setup import RelativeToGoalPositionSetup

class TeamV2BehaviorUtils:  
    @staticmethod
    def get_task_1(
        update_count: int = 0,
        updates_per_task: int = 100,
        games_count: int = 100,
        default_threshold: float = .98
    ):    
        behaviors = [
            TeamV2BehaviorUtils.get_own_team_multiple_role_behavior(
                0,
                FixedPositionSetup((-0.3, -0.3)),
                updates_per_task)
        ]

        ball_behavior = TeamV2BehaviorUtils.get_ball_behavior(
            FixedPositionSetup((0.3, 0.3)),
            updates_per_task,
            (.2, 1.35)
        )

        return CurriculumTask(
            "1",
            behaviors,
            ball_behavior,
            update_count=update_count,
            updates_per_task=updates_per_task,
            games_count=games_count,
            default_threshold=default_threshold)
    
    @staticmethod
    def get_task_2(
        update_count: int = 0,
        updates_per_task: int = 100,
        games_count: int = 100,
        default_threshold: float = .98
    ):    
        behaviors = [
            TeamV2BehaviorUtils.get_own_team_multiple_role_behavior(
                0,
                AreaExceptGoalAreaPositionSetup(True),
                updates_per_task),
            TeamV2BehaviorUtils.get_own_team_multiple_role_behavior(
                1,
                AreaExceptGoalAreaPositionSetup(True),
                updates_per_task),
            TeamV2BehaviorUtils.get_own_team_multiple_role_behavior(
                2,
                AreaExceptGoalAreaPositionSetup(True),
                updates_per_task),
            TeamV2BehaviorUtils.get_opponent_team_from_fixed_model_behavior(
                RoleEnum.ATTACKER,
                0,
                updates_per_task,
                (0, 1))
        ]

        ball_behavior = TeamV2BehaviorUtils.get_fixed_position_ball_behavior(
            updates_per_task
        )

        return CurriculumTask(
            "2",
            behaviors,
            ball_behavior,
            update_count=update_count,
            updates_per_task=updates_per_task,
            games_count=games_count,
            default_threshold=default_threshold)

    @staticmethod
    def get_task_3(
        update_count: int = 0,
        updates_per_task: int = 100,
        games_count: int = 100,
        default_threshold: float = .7
    ):    
        behaviors = [
            TeamV2BehaviorUtils.get_own_team_multiple_role_behavior(
                0,
                AreaExceptGoalAreaPositionSetup(True),
                updates_per_task),
            TeamV2BehaviorUtils.get_own_team_multiple_role_behavior(
                1,
                AreaExceptGoalAreaPositionSetup(True),
                updates_per_task),
            TeamV2BehaviorUtils.get_own_team_multiple_role_behavior(
                2,
                AreaExceptGoalAreaPositionSetup(True),
                updates_per_task),
            TeamV2BehaviorUtils.get_opponent_team_from_fixed_model_behavior(
                RoleEnum.ATTACKER,
                0,
                updates_per_task,
                (0, 1)),
            TeamV2BehaviorUtils.get_opponent_team_from_fixed_model_behavior(
                RoleEnum.GOALKEEPER,
                1,
                updates_per_task,
                (0, 1))
        ]

        ball_behavior = TeamV2BehaviorUtils.get_fixed_position_ball_behavior(
            updates_per_task
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
    def get_task_4(
        update_count: int = 0,
        updates_per_task: int = 100,
        games_count: int = 100,
        default_threshold: float = .7
    ):    
        behaviors = [
            TeamV2BehaviorUtils.get_own_team_multiple_role_behavior(
                0,
                AreaExceptGoalAreaPositionSetup(True),
                updates_per_task),
            TeamV2BehaviorUtils.get_own_team_multiple_role_behavior(
                1,
                AreaExceptGoalAreaPositionSetup(True),
                updates_per_task),
            TeamV2BehaviorUtils.get_own_team_multiple_role_behavior(
                2,
                AreaExceptGoalAreaPositionSetup(True),
                updates_per_task),
            TeamV2BehaviorUtils.get_opponent_team_from_fixed_model_behavior(
                RoleEnum.ATTACKER,
                0,
                updates_per_task,
                (0, 1)),
            TeamV2BehaviorUtils.get_opponent_team_from_fixed_model_behavior(
                RoleEnum.DEFENDER,
                1,
                updates_per_task,
                (0, 1)),
            TeamV2BehaviorUtils.get_opponent_team_from_fixed_model_behavior(
                RoleEnum.GOALKEEPER,
                2,
                updates_per_task,
                (0, 1))
        ]

        ball_behavior = TeamV2BehaviorUtils.get_fixed_position_ball_behavior(
            updates_per_task
        )

        return CurriculumTask(
            "4",
            behaviors,
            ball_behavior,
            update_count=update_count,
            updates_per_task=updates_per_task,
            games_count=games_count,
            default_threshold=default_threshold)

    @staticmethod
    def get_ball_behavior(
        position_setup: PositionSetup,
        updates_per_task: int,
        distance_range: 'tuple[float, float]'
    ):
        return BallCurriculumBehavior(
            position_setup=position_setup,
            updates_per_task=updates_per_task,
            distance_range=distance_range)
    
    @staticmethod
    def get_fixed_position_ball_behavior(
        updates_per_task: int
    ):
        return BallCurriculumBehavior(
            position_setup=FixedPositionSetup((0, 0)),
            updates_per_task=updates_per_task)
    
    @staticmethod
    def get_own_team_multiple_role_behavior(
        robot_id: int,
        position_setup: PositionSetup,
        updates_per_task: int,
        distance_range: 'tuple[float, float] | None' = None
    ):
        builder = RobotCurriculumBehaviorBuilder(
            robot_id,
            False,
            updates_per_task,
            position_setup
        )

        return builder\
            .set_ball_following_behavior()\
            .set_velocity_alpha_range((0, 0))\
            .set_distance_range(distance_range)\
            .build()
    
    @staticmethod
    def get_opponent_team_from_fixed_model_behavior(
        role_enum: RoleEnum,
        robot_id: int,
        updates_per_task: int,
        velocity_alpha_range: 'tuple[float, float]'
    ):
        if role_enum == RoleEnum.GOALKEEPER:
            position_setup = GoalAreaPositionSetup(False)
        else:
            position_setup = AreaExceptGoalAreaPositionSetup(False)

        builder = RobotCurriculumBehaviorBuilder(
            robot_id,
            True,
            updates_per_task,
            position_setup
        )

        if role_enum == RoleEnum.DEFENDER:
            model_path = Configuration.model_defender_path
        elif role_enum == RoleEnum.GOALKEEPER:
            model_path = Configuration.model_goalkeeper_path
        else:
            model_path = Configuration.model_attacker_path


        return builder\
            .set_from_fixed_model_behavior(model_path, role_enum)\
            .set_velocity_alpha_range(velocity_alpha_range)\
            .build()
