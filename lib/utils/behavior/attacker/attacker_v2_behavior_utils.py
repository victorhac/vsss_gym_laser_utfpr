from lib.builders.robot_curriculum_behavior_builder import RobotCurriculumBehaviorBuilder
from lib.domain.ball_curriculum_behavior import BallCurriculumBehavior
from lib.domain.curriculum_task import CurriculumTask
from lib.domain.enums.robot_curriculum_behavior_enum import RobotCurriculumBehaviorEnum
from lib.position_setup.area_except_goal_area_position_setup import AreaExceptGoalAreaPositionSetup
from lib.position_setup.area_position_setup import AreaPositionSetup
from lib.position_setup.goal_area_position_setup import GoalAreaPositionSetup
from lib.position_setup.position_setup import PositionSetup
from lib.position_setup.relative_to_ball_position_setup import RelativeToBallPositionSetup
from lib.position_setup.relative_to_goal_position_setup import RelativeToGoalPositionSetup

class AttackerV2BehaviorUtils:
    @staticmethod
    def get_task_1(
        update_count: int = 0,
        updates_per_task: int = 100,
        games_count: int = 100,
        default_threshold: float = .7
    ):
        behaviors = [
            AttackerV2BehaviorUtils.get_own_team_from_model_behavior(
                0,
                RelativeToBallPositionSetup(True),
                updates_per_task)
        ]

        ball_behavior = AttackerV2BehaviorUtils.get_ball_behavior(
            RelativeToGoalPositionSetup(False),
            updates_per_task,
            distance_range=(.2, 1.3)
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
            AttackerV2BehaviorUtils.get_own_team_from_model_behavior(
                0,
                RelativeToBallPositionSetup(True),
                updates_per_task),
            AttackerV2BehaviorUtils.get_stopped_behavior(
                0,
                True,
                AreaPositionSetup(False),
                updates_per_task)
        ]
    
        ball_behavior = AttackerV2BehaviorUtils.get_ball_behavior(
            AreaPositionSetup(True),
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
            AttackerV2BehaviorUtils.get_own_team_from_model_behavior(
                0,
                RelativeToBallPositionSetup(True),
                updates_per_task),
            AttackerV2BehaviorUtils.get_opponent_team_ball_following_behavior(
                0,
                updates_per_task)
        ]
    
        ball_behavior = AttackerV2BehaviorUtils.get_ball_behavior(
            AreaPositionSetup(True),
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
        games_count: int = 200,
        default_threshold: float = .6
    ):
        behaviors = [
            AttackerV2BehaviorUtils.get_own_team_from_model_behavior(
                0,
                RelativeToBallPositionSetup(True),
                updates_per_task),
            AttackerV2BehaviorUtils.get_stopped_behavior(
                1,
                False,
                AreaExceptGoalAreaPositionSetup(True),
                updates_per_task),
            AttackerV2BehaviorUtils.get_opponent_team_ball_following_behavior(
                0,
                updates_per_task),
            AttackerV2BehaviorUtils.get_stopped_behavior(
                1,
                True,
                AreaExceptGoalAreaPositionSetup(False),
                updates_per_task)
        ]
    
        ball_behavior = AttackerV2BehaviorUtils.get_ball_behavior(
            AreaPositionSetup(True),
            updates_per_task
        )

        return CurriculumTask(
            "4",
            behaviors,
            ball_behavior,
            update_count=update_count,
            updates_per_task=updates_per_task,
            games_count=games_count,
            default_threshold=default_threshold,
            threshold_intervals=[
                (82, .55),
                (89, .5)])

    @staticmethod
    def get_task_5(
        update_count: int = 0,
        updates_per_task: int = 100,
        default_threshold: float = .5,
        games_count: int = 200
    ):
        behaviors = [
            AttackerV2BehaviorUtils.get_own_team_from_model_behavior(
                0,
                RelativeToBallPositionSetup(True),
                updates_per_task),
            AttackerV2BehaviorUtils.get_stopped_behavior(
                1,
                False,
                AreaExceptGoalAreaPositionSetup(True),
                updates_per_task),
            AttackerV2BehaviorUtils.get_stopped_behavior(
                2,
                False,
                GoalAreaPositionSetup(True),
                updates_per_task),
            AttackerV2BehaviorUtils.get_opponent_team_ball_following_behavior(
                0,
                updates_per_task),
            AttackerV2BehaviorUtils.get_stopped_behavior(
                1,
                True,
                AreaExceptGoalAreaPositionSetup(False),
                updates_per_task),
            AttackerV2BehaviorUtils.get_stopped_behavior(
                2,
                True,
                GoalAreaPositionSetup(False),
                updates_per_task)
        ]
    
        ball_behavior = AttackerV2BehaviorUtils.get_ball_behavior(
            AreaPositionSetup(True),
            updates_per_task
        )

        return CurriculumTask(
            "5",
            behaviors,
            ball_behavior,
            update_count=update_count,
            updates_per_task=updates_per_task,
            default_threshold=default_threshold,
            games_count=games_count,
            threshold_intervals=[
                (74, .45),
                (83, .33)
            ])
    
    @staticmethod
    def get_task_6(
        update_count: int = 0,
        updates_per_task: int = 100,
        default_threshold: float = .4,
        games_count: int = 200
    ):
        behaviors = [
            AttackerV2BehaviorUtils.get_own_team_from_model_behavior(
                0,
                RelativeToBallPositionSetup(True),
                updates_per_task),
            AttackerV2BehaviorUtils.get_stopped_behavior(
                1,
                False,
                AreaExceptGoalAreaPositionSetup(True),
                updates_per_task),
            AttackerV2BehaviorUtils.get_stopped_behavior(
                2,
                False,
                AreaExceptGoalAreaPositionSetup(True),
                updates_per_task),
            AttackerV2BehaviorUtils.get_opponent_team_from_previous_model_behavior(
                0,
                RelativeToBallPositionSetup(False),
                updates_per_task),
            AttackerV2BehaviorUtils.get_stopped_behavior(
                1,
                True,
                AreaExceptGoalAreaPositionSetup(False),
                updates_per_task),
            AttackerV2BehaviorUtils.get_stopped_behavior(
                2,
                True,
                GoalAreaPositionSetup(False),
                updates_per_task),
        ]
    
        ball_behavior = AttackerV2BehaviorUtils.get_ball_behavior(
            AreaPositionSetup(True),
            updates_per_task
        )

        return CurriculumTask(
            "6",
            behaviors,
            ball_behavior,
            update_count=update_count,
            updates_per_task=updates_per_task,
            default_threshold=default_threshold,
            games_count=games_count,
            threshold_intervals=[(14, .3)])

    @staticmethod
    def get_stopped_behavior(
        robot_id: int,
        is_yellow: bool,
        position_setup: PositionSetup,
        updates_per_task: int
    ):
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
    def get_opponent_team_from_previous_model_behavior(
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
            .set_from_previous_model_behavior()\
            .set_distance_range((.3, .6))\
            .set_velocity_alpha_range((0, .5))\
            .build()
    
    @staticmethod
    def get_ball_following_behavior(
        robot_id: int,
        is_yellow: bool,
        position_setup: PositionSetup,
        distance_range: 'tuple[float, float] | None',
        velocity_alpha_range: 'tuple[float, float] | None',
        updates_per_task: int
    ):
        builder = RobotCurriculumBehaviorBuilder(
            robot_id,
            is_yellow,
            updates_per_task,
            position_setup
        )

        builder.set_ball_following_behavior()

        if distance_range is not None:
            builder.set_distance_range(distance_range)
            
        if velocity_alpha_range is not None:
            builder.set_velocity_alpha_range(velocity_alpha_range)
            
        return builder.build()
    
    @staticmethod
    def get_opponent_team_ball_following_behavior(
        robot_id: int,
        updates_per_task: int
    ):
        builder = RobotCurriculumBehaviorBuilder(
            robot_id,
            True,
            updates_per_task,
            RelativeToBallPositionSetup(False)
        )

        return builder\
            .set_ball_following_behavior()\
            .set_distance_range((.3, .6))\
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
            RobotCurriculumBehaviorEnum.GOALKEEPER_BALL_FOLLOWING,
            updates_per_task,
            GoalAreaPositionSetup(not is_yellow)
        )

        return builder\
            .set_velocity_alpha_range((.2, .2))\
            .build()
    
    @staticmethod
    def get_ball_behavior(
        position_setup: PositionSetup,
        updates_per_task: int,
        distance_range: 'tuple[float, float] | None' = None
    ):
        return BallCurriculumBehavior(
            position_setup=position_setup,
            updates_per_task=updates_per_task,
            distance_range=distance_range)