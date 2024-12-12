from lib.builders.robot_curriculum_behavior_builder import RobotCurriculumBehaviorBuilder
from lib.domain.ball_curriculum_behavior import BallCurriculumBehavior
from lib.domain.curriculum_task import CurriculumTask
from lib.domain.enums.position_enum import PositionEnum
from configuration.configuration import Configuration

class DefenderBehaviorUtils:
    @staticmethod
    def get_task_1(
        update_count: int = 0,
        updates_per_task: int = 100,
        games_count: int = 100,
        default_threshold: float = .95
    ):
        behaviors = [
            DefenderBehaviorUtils.get_own_team_from_model_behavior(
                0,
                PositionEnum.RELATIVE_TO_BALL,
                updates_per_task)
        ]

        ball_behavior = DefenderBehaviorUtils.get_ball_behavior(
            PositionEnum.RELATIVE_TO_OWN_GOAL,
            updates_per_task,
            distance_range=(.7, .2)
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
        default_threshold: float = .7
    ):
        behaviors = [
            DefenderBehaviorUtils.get_own_team_from_model_behavior(
                0,
                PositionEnum.RELATIVE_TO_BALL,
                updates_per_task),
            DefenderBehaviorUtils.get_opponent_team_ball_following_behavior(
                0,
                PositionEnum.RELATIVE_TO_BALL,
                updates_per_task)
        ]

        ball_behavior = DefenderBehaviorUtils.get_ball_behavior(
            PositionEnum.RELATIVE_TO_OWN_GOAL,
            updates_per_task,
            distance_range=(1, .2)
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
            DefenderBehaviorUtils.get_own_team_from_model_behavior(
                0,
                PositionEnum.RELATIVE_TO_BALL,
                updates_per_task),
            DefenderBehaviorUtils.get_own_team_goalkeeper_ball_following_behavior(
                2,
                updates_per_task),
            DefenderBehaviorUtils.get_opponent_team_from_fixed_model_behavior(
                0,
                PositionEnum.RELATIVE_TO_BALL,
                updates_per_task),
            DefenderBehaviorUtils.get_opponent_team_ball_following_behavior(
                1,
                PositionEnum.RELATIVE_TO_BALL,
                updates_per_task
            )
        ]

        ball_behavior = DefenderBehaviorUtils.get_ball_behavior(
            PositionEnum.RELATIVE_TO_OWN_GOAL,
            updates_per_task,
            distance_range=(1, .2)
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
            DefenderBehaviorUtils.get_own_team_from_model_behavior(
                0,
                PositionEnum.RELATIVE_TO_BALL,
                updates_per_task),
            DefenderBehaviorUtils.get_own_team_ball_following_behavior(
                1,
                PositionEnum.RELATIVE_TO_BALL,
                updates_per_task),
            DefenderBehaviorUtils.get_own_team_goalkeeper_ball_following_behavior(
                2,
                updates_per_task),
            DefenderBehaviorUtils.get_opponent_team_from_fixed_model_behavior(
                0,
                PositionEnum.RELATIVE_TO_BALL,
                updates_per_task),
            DefenderBehaviorUtils.get_opponent_team_ball_following_behavior(
                1,
                PositionEnum.RELATIVE_TO_BALL,
                updates_per_task),
            DefenderBehaviorUtils.get_opponent_team_goalkeeper_ball_following_behavior(
                2,
                updates_per_task)
        ]

        ball_behavior = DefenderBehaviorUtils.get_ball_behavior(
            PositionEnum.OWN_GOAL_AREA,
            updates_per_task,
            distance_range=(1, .2)
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
        position_enum: PositionEnum,
        updates_per_task: int,
        distance_range: 'tuple[float, float] | None' = None
    ):
        return BallCurriculumBehavior(
            position_enum=position_enum,
            updates_per_task=updates_per_task,
            distance_range=distance_range)
    
    @staticmethod
    def get_own_team_from_model_behavior(
        robot_id: int,
        position_enum: PositionEnum,
        updates_per_task: int
    ):
        builder = RobotCurriculumBehaviorBuilder(
            robot_id,
            False,
            updates_per_task
        )

        return builder\
            .set_from_model_behavior()\
            .set_position_enum(position_enum)\
            .set_distance_range((.2, .5))\
            .build()
    
    @staticmethod
    def get_opponent_team_from_fixed_model_behavior(
        robot_id: int,
        position_enum: PositionEnum,
        updates_per_task: int
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
            .set_distance_range((.2, .5))\
            .set_velocity_alpha_range((0, .5))\
            .build()
    
    @staticmethod
    def get_own_team_ball_following_behavior(
        robot_id: int,
        position_enum: PositionEnum,
        updates_per_task: int
    ):
        builder = RobotCurriculumBehaviorBuilder(
            robot_id,
            False,
            updates_per_task
        )

        return builder\
            .set_ball_following_behavior()\
            .set_position_enum(position_enum)\
            .set_distance_range((.2, .5))\
            .set_velocity_alpha_range((0, .5))\
            .build()
    
    @staticmethod
    def get_opponent_team_ball_following_behavior(
        robot_id: int,
        position_enum: PositionEnum,
        updates_per_task: int
    ):
        builder = RobotCurriculumBehaviorBuilder(
            robot_id,
            True,
            updates_per_task
        )

        return builder\
            .set_ball_following_behavior()\
            .set_position_enum(position_enum)\
            .set_distance_range((.2, .5))\
            .set_velocity_alpha_range((0, .5))\
            .build()
    
    @staticmethod
    def get_goalkeeper_ball_following_behavior(
        robot_id: int,
        is_yellow: bool,
        updates_per_task: int
    ):
        builder = RobotCurriculumBehaviorBuilder(
            robot_id,
            is_yellow,
            updates_per_task
        )

        return builder\
            .set_goalkeeper_ball_following_behavior()\
            .set_position_enum(PositionEnum.OWN_GOAL_AREA)\
            .build()
    
    @staticmethod
    def get_own_team_goalkeeper_ball_following_behavior(
        robot_id: int,
        updates_per_task: int
    ):
        return DefenderBehaviorUtils.get_goalkeeper_ball_following_behavior(
            robot_id,
            False,
            updates_per_task
        )
    
    @staticmethod
    def get_opponent_team_goalkeeper_ball_following_behavior(
        robot_id: int,
        updates_per_task: int
    ):
        return DefenderBehaviorUtils.get_goalkeeper_ball_following_behavior(
            robot_id,
            True,
            updates_per_task
        )