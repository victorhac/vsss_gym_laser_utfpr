from lib.builders.robot_curriculum_behavior_builder import RobotCurriculumBehaviorBuilder
from lib.curriculum.ball_curriculum_behavior import BallCurriculumBehavior
from lib.curriculum.curriculum_task import CurriculumTask
from configuration.configuration import Configuration
from lib.curriculum.position_setup.area_except_goal_area_position_setup import AreaExceptGoalAreaPositionSetup
from lib.curriculum.position_setup.behind_ball_position_setup import BehindBallPositionSetup
from lib.curriculum.position_setup.field_position_setup import FieldPositionSetup
from lib.curriculum.position_setup.goal_area_position_setup import GoalAreaPositionSetup
from lib.curriculum.position_setup.position_setup import PositionSetup
from lib.curriculum.position_setup.relative_to_ball_position_setup import RelativeToBallPositionSetup
from lib.curriculum.position_setup.relative_to_vertical_line_position_setup import RelativeToVerticalLinePositionSetup
from lib.curriculum.position_setup.relative_to_wall_position_setup import RelativeToWallPositionSetup

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
                RelativeToBallPositionSetup(True),
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
                RelativeToBallPositionSetup(True),
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
                RelativeToBallPositionSetup(True),
                updates_per_task),
            DefenderBehaviorUtils.get_opponent_team_from_fixed_model_behavior(
                0,
                RelativeToBallPositionSetup(False),
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
                RelativeToBallPositionSetup(True),
                updates_per_task),
            DefenderBehaviorUtils.get_own_team_goalkeeper_stopped_behavior(
                2,
                updates_per_task),
            DefenderBehaviorUtils.get_opponent_team_from_fixed_model_behavior(
                0,
                RelativeToBallPositionSetup(False),
                updates_per_task,
                (0, .5)),
            DefenderBehaviorUtils.get_opponent_team_stopped_behavior(
                1,
                AreaExceptGoalAreaPositionSetup(True),
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
                RelativeToBallPositionSetup(True),
                updates_per_task),
            DefenderBehaviorUtils.get_own_team_stopped_behavior(
                1,
                FieldPositionSetup(),
                updates_per_task),
            DefenderBehaviorUtils.get_own_team_goalkeeper_stopped_behavior(
                2,
                updates_per_task),
            DefenderBehaviorUtils.get_opponent_team_from_fixed_model_behavior(
                0,
                RelativeToBallPositionSetup(False),
                updates_per_task,
                (0, .5)),
            DefenderBehaviorUtils.get_opponent_team_stopped_behavior(
                1,
                FieldPositionSetup(),
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
        default_threshold: float = .8
    ):
        behaviors = [
            DefenderBehaviorUtils.get_own_team_from_model_relative_to_field_center_line_behavior(
                0,
                updates_per_task),
            DefenderBehaviorUtils.get_opponent_team_from_fixed_model_relative_to_field_center_line_behavior(
                0,
                updates_per_task)
        ]

        ball_behavior = DefenderBehaviorUtils.get_ball_behavior(
            updates_per_task,
            distance_range=(.65, .9)
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
    def get_task_7(
        update_count: int = 0,
        updates_per_task: int = 100,
        games_count: int = 100,
        default_threshold: float = .8
    ):
        behaviors = [
            DefenderBehaviorUtils.get_own_team_from_model_relative_to_field_center_line_behavior(
                0,
                updates_per_task),
            DefenderBehaviorUtils.get_own_team_stopped_behavior(
                1,
                FieldPositionSetup(),
                updates_per_task),
            DefenderBehaviorUtils.get_own_team_goalkeeper_stopped_behavior(
                2,
                updates_per_task),
            DefenderBehaviorUtils.get_opponent_team_from_fixed_model_relative_to_field_center_line_behavior(
                0,
                updates_per_task),
            DefenderBehaviorUtils.get_opponent_team_stopped_behavior(
                1,
                FieldPositionSetup(),
                updates_per_task),
            DefenderBehaviorUtils.get_opponent_team_goalkeeper_ball_following_behavior(
                2,
                updates_per_task)
        ]

        ball_behavior = DefenderBehaviorUtils.get_ball_behavior(
            updates_per_task,
            distance_range=(.65, .9)
        )

        return CurriculumTask(
            "7",
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
        position_setup = RelativeToVerticalLinePositionSetup(
            True,
            -.6,
            (-.65, .65),
            False
        )

        return BallCurriculumBehavior(
            updates_per_task=updates_per_task,
            distance_range=distance_range,
            position_setup=position_setup)
    
    @staticmethod
    def get_close_to_own_goal_ball_behavior(
        updates_per_task: int
    ):
        position_setup = RelativeToWallPositionSetup(
            True,
            .07
        )

        return BallCurriculumBehavior(
            updates_per_task=updates_per_task,
            distance_range=(1.15, 0),
            position_setup=position_setup)
    
    @staticmethod
    def get_own_team_from_model_behavior(
        robot_id: int,
        position_setup: PositionSetup,
        updates_per_task: int
    ):
        builder = RobotCurriculumBehaviorBuilder(
            robot_id,
            False,
            updates_per_task,
            position_setup
        )

        return builder\
            .set_from_model_behavior()\
            .set_distance_range((.2, .5))\
            .build()
    
    @staticmethod
    def get_own_team_from_model_relative_to_field_center_line_behavior(
        robot_id: int,
        updates_per_task: int
    ):
        position_setup = RelativeToVerticalLinePositionSetup(
            True,
            0,
            (-.65, .65),
            True
        )

        builder = RobotCurriculumBehaviorBuilder(
            robot_id,
            False,
            updates_per_task,
            position_setup
        )

        return builder\
            .set_from_model_behavior()\
            .set_distance_range((.6, .05))\
            .build()
    
    @staticmethod
    def get_opponent_team_from_fixed_model_behavior(
        robot_id: int,
        position_setup: PositionSetup,
        updates_per_task: int,
        velocity_alpha_range: 'tuple[float, float]',
        distance_range: 'tuple[float, float]' = (.2, .5)
    ):
        builder = RobotCurriculumBehaviorBuilder(
            robot_id,
            True,
            updates_per_task,
            position_setup
        )

        model_path = Configuration.model_attacker_path

        return builder\
            .set_from_fixed_model_behavior(model_path)\
            .set_distance_range(distance_range)\
            .set_velocity_alpha_range(velocity_alpha_range)\
            .build()
    
    @staticmethod
    def get_opponent_team_from_fixed_model_relative_to_field_center_line_behavior(
        robot_id: int,
        updates_per_task: int
    ):
        position_setup = BehindBallPositionSetup(False)
        builder = RobotCurriculumBehaviorBuilder(
            robot_id,
            True,
            updates_per_task,
            position_setup
        )

        model_path = Configuration.model_attacker_path

        return builder\
            .set_from_fixed_model_behavior(model_path)\
            .set_distance_range((.3, .3))\
            .set_velocity_alpha_range((.4, .7))\
            .build()
    
    @staticmethod
    def get_own_team_ball_following_behavior(
        robot_id: int,
        position_setup: PositionSetup,
        updates_per_task: int
    ):
        builder = RobotCurriculumBehaviorBuilder(
            robot_id,
            False,
            updates_per_task,
            position_setup
        )

        return builder\
            .set_ball_following_behavior()\
            .set_distance_range((.2, .5))\
            .set_velocity_alpha_range((0, .5))\
            .build()
    
    @staticmethod
    def get_own_team_stopped_behavior(
        robot_id: int,
        position_setup: PositionSetup,
        updates_per_task: int
    ):
        builder = RobotCurriculumBehaviorBuilder(
            robot_id,
            False,
            updates_per_task,
            position_setup
        )

        return builder\
            .set_ball_following_behavior()\
            .set_distance_range((.5, .2))\
            .set_velocity_alpha_range((0, 0))\
            .build()
    
    @staticmethod
    def get_opponent_team_ball_following_behavior(
        robot_id: int,
        position_setup: PositionSetup,
        updates_per_task: int,
        velocity_alpha_range: 'tuple[float, float]'
    ):
        builder = RobotCurriculumBehaviorBuilder(
            robot_id,
            True,
            updates_per_task,
            position_setup
        )

        return builder\
            .set_ball_following_behavior()\
            .set_distance_range((.8, .4))\
            .set_velocity_alpha_range(velocity_alpha_range)\
            .build()
    
    @staticmethod
    def get_opponent_team_stopped_behavior(
        robot_id: int,
        position_setup: PositionSetup,
        updates_per_task: int
    ):
        builder = RobotCurriculumBehaviorBuilder(
            robot_id,
            True,
            updates_per_task,
            position_setup
        )

        return builder\
            .set_ball_following_behavior()\
            .set_distance_range((.8, .4))\
            .set_velocity_alpha_range((0, 0))\
            .build()
    
    @staticmethod
    def get_goalkeeper_stopped_behavior(
        robot_id: int,
        is_yellow: bool,
        updates_per_task: int
    ):
        position_setup = GoalAreaPositionSetup(not is_yellow)
        builder = RobotCurriculumBehaviorBuilder(
            robot_id,
            is_yellow,
            updates_per_task,
            position_setup
        )

        return builder\
            .set_ball_following_behavior()\
            .set_velocity_alpha_range((0, 0))\
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