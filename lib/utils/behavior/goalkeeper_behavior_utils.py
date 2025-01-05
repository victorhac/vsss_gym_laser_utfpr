from lib.builders.robot_curriculum_behavior_builder import RobotCurriculumBehaviorBuilder
from lib.domain.ball_curriculum_behavior import BallCurriculumBehavior
from lib.domain.curriculum_task import CurriculumTask
from lib.domain.enums.position_enum import PositionEnum
from configuration.configuration import Configuration

class GoalkeeperBehaviorUtils:
    @staticmethod
    def get_task_1(
        update_count: int = 0,
        updates_per_task: int = 100,
        games_count: int = 100,
        default_threshold: float = .7
    ):
        behaviors = [
            GoalkeeperBehaviorUtils.get_own_team_from_model_behavior(
                0,
                updates_per_task),
            GoalkeeperBehaviorUtils.get_opponent_team_from_fixed_model_behavior(
                0,
                PositionEnum.BEHIND_BALL,
                updates_per_task,
                (.5, 1),
                (.2, .2)
            )
        ]

        ball_behavior = GoalkeeperBehaviorUtils.get_ball_behavior(
            updates_per_task,
            distance_range=(1, .3)
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
    def get_ball_behavior(
        updates_per_task: int,
        distance_range: 'tuple[float, float] | None' = None
    ):
        return BallCurriculumBehavior(
            position_enum=PositionEnum.RELATIVE_TO_OWN_VERTICAL_LINE,
            updates_per_task=updates_per_task,
            distance_range=distance_range,
            x_line=-.6,
            y_range=(-.35, .35),
            left_to_line=False)
    
    @staticmethod
    def get_own_team_from_model_behavior(
        robot_id: int,
        updates_per_task: int
    ):
        builder = RobotCurriculumBehaviorBuilder(
            robot_id,
            False,
            updates_per_task
        )

        return builder\
            .set_from_model_behavior()\
            .set_position_enum(PositionEnum.OWN_GOAL_AREA)\
            .build()
    
    @staticmethod
    def get_opponent_team_from_fixed_model_behavior(
        robot_id: int,
        position_enum: PositionEnum,
        updates_per_task: int,
        velocity_alpha_range: 'tuple[float, float]',
        distance_range: 'tuple[float, float]' = (.2, .5)
    ):
        builder = RobotCurriculumBehaviorBuilder(
            robot_id,
            True,
            updates_per_task
        )

        model_path = Configuration.get_model_attacker_path()

        return builder\
            .set_from_fixed_model_behavior(model_path)\
            .set_position_enum(position_enum)\
            .set_distance_range(distance_range)\
            .set_velocity_alpha_range(velocity_alpha_range)\
            .build()