from lib.builders.robot_curriculum_behavior_builder import RobotCurriculumBehaviorBuilder
from lib.domain.ball_curriculum_behavior import BallCurriculumBehavior
from lib.domain.curriculum_task import CurriculumTask
from configuration.configuration import Configuration
from lib.position_setup.behind_ball_position_setup import BehindBallPositionSetup
from lib.position_setup.goal_area_position_setup import GoalAreaPositionSetup
from lib.position_setup.position_setup import PositionSetup
from lib.position_setup.relative_to_vertical_line_position_setup import RelativeToVerticalLinePositionSetup

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
                BehindBallPositionSetup(False),
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
        position_setup = RelativeToVerticalLinePositionSetup(
            True,
            .6,
            (-.35, .35),
            True
        )

        return BallCurriculumBehavior(
            position_setup=position_setup,
            updates_per_task=updates_per_task,
            distance_range=distance_range)
    
    @staticmethod
    def get_own_team_from_model_behavior(
        robot_id: int,
        updates_per_task: int
    ):
        position_setup = GoalAreaPositionSetup(True)
        builder = RobotCurriculumBehaviorBuilder(
            robot_id,
            False,
            updates_per_task,
            position_setup
        )

        return builder\
            .set_from_model_behavior()\
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