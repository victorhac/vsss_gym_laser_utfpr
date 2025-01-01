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
        default_threshold: float = .98
    ):
        behaviors = [
            DefenderBehaviorUtils.get_own_team_from_model_behavior(
                0,
                PositionEnum.RELATIVE_TO_BALL,
                updates_per_task)
        ]

        ball_behavior = DefenderBehaviorUtils.get_ball_behavior(
            updates_per_task,
            distance_range=(.55, 0)
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
            DefenderBehaviorUtils.get_own_team_from_model_behavior(
                0,
                PositionEnum.RELATIVE_TO_BALL,
                updates_per_task)
        ]

        ball_behavior = DefenderBehaviorUtils\
            .get_close_to_own_goal_ball_behavior(
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
            DefenderBehaviorUtils.get_own_team_from_model_behavior(
                0,
                PositionEnum.RELATIVE_TO_BALL,
                updates_per_task),
            DefenderBehaviorUtils.get_opponent_team_from_fixed_model_behavior(
                0,
                PositionEnum.RELATIVE_TO_BALL,
                updates_per_task,
                (0, .5))
        ]

        ball_behavior = DefenderBehaviorUtils.get_ball_behavior(
            updates_per_task,
            distance_range=(.55, 0)
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
            DefenderBehaviorUtils.get_own_team_goalkeeper_stopped_behavior(
                2,
                updates_per_task),
            DefenderBehaviorUtils.get_opponent_team_from_fixed_model_behavior(
                0,
                PositionEnum.RELATIVE_TO_BALL,
                updates_per_task,
                (0, .5)),
            DefenderBehaviorUtils.get_opponent_team_stopped_behavior(
                1,
                PositionEnum.OPPONENT_AREA_EXCEPT_GOAL_AREA,
                updates_per_task
            )
        ]

        ball_behavior = DefenderBehaviorUtils.get_ball_behavior(
            updates_per_task,
            distance_range=(.55, .1)
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
    def get_task_5(
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
            DefenderBehaviorUtils.get_own_team_stopped_behavior(
                1,
                PositionEnum.FIELD,
                updates_per_task),
            DefenderBehaviorUtils.get_own_team_goalkeeper_stopped_behavior(
                2,
                updates_per_task),
            DefenderBehaviorUtils.get_opponent_team_from_fixed_model_behavior(
                0,
                PositionEnum.RELATIVE_TO_BALL,
                updates_per_task,
                (0, .5)),
            DefenderBehaviorUtils.get_opponent_team_stopped_behavior(
                1,
                PositionEnum.FIELD,
                updates_per_task),
            DefenderBehaviorUtils.get_opponent_team_goalkeeper_ball_following_behavior(
                2,
                updates_per_task)
        ]

        ball_behavior = DefenderBehaviorUtils.get_ball_behavior(
            updates_per_task,
            distance_range=(.55, .1)
        )

        return CurriculumTask(
            "5",
            behaviors,
            ball_behavior,
            update_count=update_count,
            updates_per_task=updates_per_task,
            games_count=games_count,
            default_threshold=default_threshold)
    
    @staticmethod
    def get_task_6(
        update_count: int = 0,
        updates_per_task: int = 100,
        games_count: int = 100,
        default_threshold: float = .7
    ):
        behaviors = [
            DefenderBehaviorUtils.get_own_team_from_model_behavior(
                0,
                PositionEnum.RELATIVE_TO_BALL,
                updates_per_task)
        ]

        ball_behavior = DefenderBehaviorUtils.get_ball_behavior(
            updates_per_task,
            distance_range=(.6, 1)
        )

        return CurriculumTask(
            "6",
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
    def get_close_to_own_goal_ball_behavior(
        updates_per_task: int
    ):
        return BallCurriculumBehavior(
            position_enum=PositionEnum.OWN_GOAL_RELATIVE_TO_WALL,
            updates_per_task=updates_per_task,
            distance_range=(1.15, 0),
            distance_to_wall=.07)
    
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
        updates_per_task: int,
        velocity_alpha_range: 'tuple[float, float]'
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
            .set_velocity_alpha_range(velocity_alpha_range)\
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
    def get_own_team_stopped_behavior(
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
            .set_distance_range((.5, .2))\
            .set_velocity_alpha_range((0, 0))\
            .build()
    
    @staticmethod
    def get_opponent_team_ball_following_behavior(
        robot_id: int,
        position_enum: PositionEnum,
        updates_per_task: int,
        velocity_alpha_range: 'tuple[float, float]'
    ):
        builder = RobotCurriculumBehaviorBuilder(
            robot_id,
            True,
            updates_per_task
        )

        return builder\
            .set_ball_following_behavior()\
            .set_position_enum(position_enum)\
            .set_distance_range((.8, .4))\
            .set_velocity_alpha_range(velocity_alpha_range)\
            .build()
    
    @staticmethod
    def get_opponent_team_stopped_behavior(
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
            .set_distance_range((.8, .4))\
            .set_velocity_alpha_range((0, 0))\
            .build()
    
    @staticmethod
    def get_goalkeeper_stopped_behavior(
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
            .set_ball_following_behavior()\
            .set_velocity_alpha_range((0,0))\
            .set_position_enum(PositionEnum.OWN_GOAL_AREA)\
            .build()
    
    @staticmethod
    def get_own_team_goalkeeper_stopped_behavior(
        robot_id: int,
        updates_per_task: int
    ):
        return DefenderBehaviorUtils.get_goalkeeper_stopped_behavior(
            robot_id,
            False,
            updates_per_task
        )
    
    @staticmethod
    def get_opponent_team_goalkeeper_ball_following_behavior(
        robot_id: int,
        updates_per_task: int
    ):
        return DefenderBehaviorUtils.get_goalkeeper_stopped_behavior(
            robot_id,
            True,
            updates_per_task
        )