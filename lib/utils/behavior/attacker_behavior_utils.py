from lib.builders.robot_curriculum_behavior_builder import RobotCurriculumBehaviorBuilder
from lib.domain.ball_curriculum_behavior import BallCurriculumBehavior
from lib.domain.curriculum_task import CurriculumTask
from lib.enums.position_enum import PositionEnum
from lib.enums.robot_curriculum_behavior_enum import RobotCurriculumBehaviorEnum

class AttackerBehaviorUtils:
    @staticmethod
    def get_task_1(
        update_count: int = 0,
        updates_per_task: int = 100,
        games_count: int = 100,
        default_threshold: float = .7
    ):
        behaviors = [
            AttackerBehaviorUtils.get_own_team_from_model_behavior(
                0,
                PositionEnum.RELATIVE_TO_BALL,
                updates_per_task)
        ]

        ball_behavior = AttackerBehaviorUtils.get_ball_behavior(
            PositionEnum.RELATIVE_TO_OPPONENT_GOAL,
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
            AttackerBehaviorUtils.get_own_team_from_model_behavior(
                0,
                PositionEnum.RELATIVE_TO_BALL,
                updates_per_task),
            AttackerBehaviorUtils.get_stopped_behavior(
                0,
                True,
                PositionEnum.OWN_AREA,
                updates_per_task)
        ]
    
        ball_behavior = AttackerBehaviorUtils.get_ball_behavior(
            PositionEnum.OWN_AREA,
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
            AttackerBehaviorUtils.get_own_team_from_model_behavior(
                0,
                PositionEnum.RELATIVE_TO_BALL,
                updates_per_task),
            AttackerBehaviorUtils.get_opponent_team_ball_following_behavior(
                0,
                updates_per_task)
        ]
    
        ball_behavior = AttackerBehaviorUtils.get_ball_behavior(
            PositionEnum.OWN_AREA,
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
            AttackerBehaviorUtils.get_own_team_from_model_behavior(
                0,
                PositionEnum.RELATIVE_TO_BALL,
                updates_per_task),
            AttackerBehaviorUtils.get_stopped_behavior(
                1,
                False,
                PositionEnum.OWN_AREA_EXCEPT_GOAL_AREA,
                updates_per_task),
            AttackerBehaviorUtils.get_opponent_team_ball_following_behavior(
                0,
                updates_per_task),
            AttackerBehaviorUtils.get_stopped_behavior(
                1,
                True,
                PositionEnum.OWN_AREA_EXCEPT_GOAL_AREA,
                updates_per_task)
        ]
    
        ball_behavior = AttackerBehaviorUtils.get_ball_behavior(
            PositionEnum.OWN_AREA,
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
            AttackerBehaviorUtils.get_own_team_from_model_behavior(
                0,
                PositionEnum.RELATIVE_TO_BALL,
                updates_per_task),
            AttackerBehaviorUtils.get_stopped_behavior(
                1,
                False,
                PositionEnum.OWN_AREA_EXCEPT_GOAL_AREA,
                updates_per_task),
            AttackerBehaviorUtils.get_stopped_behavior(
                2,
                False,
                PositionEnum.GOAL_AREA,
                updates_per_task),
            AttackerBehaviorUtils.get_opponent_team_ball_following_behavior(
                0,
                updates_per_task),
            AttackerBehaviorUtils.get_stopped_behavior(
                1,
                True,
                PositionEnum.OWN_AREA_EXCEPT_GOAL_AREA,
                updates_per_task),
            AttackerBehaviorUtils.get_stopped_behavior(
                2,
                True,
                PositionEnum.GOAL_AREA,
                updates_per_task)
        ]
    
        ball_behavior = AttackerBehaviorUtils.get_ball_behavior(
            PositionEnum.OWN_AREA,
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
            AttackerBehaviorUtils.get_own_team_from_model_behavior(
                0,
                PositionEnum.RELATIVE_TO_BALL,
                updates_per_task),
            AttackerBehaviorUtils.get_stopped_behavior(
                1,
                False,
                PositionEnum.OWN_AREA_EXCEPT_GOAL_AREA,
                updates_per_task),
            AttackerBehaviorUtils.get_stopped_behavior(
                2,
                False,
                PositionEnum.GOAL_AREA,
                updates_per_task),
            AttackerBehaviorUtils.get_opponent_team_from_model_behavior(
                0,
                PositionEnum.RELATIVE_TO_BALL,
                updates_per_task),
            AttackerBehaviorUtils.get_stopped_behavior(
                1,
                True,
                PositionEnum.OWN_AREA_EXCEPT_GOAL_AREA,
                updates_per_task),
            AttackerBehaviorUtils.get_stopped_behavior(
                2,
                True,
                PositionEnum.GOAL_AREA,
                updates_per_task),
        ]
    
        ball_behavior = AttackerBehaviorUtils.get_ball_behavior(
            PositionEnum.OWN_AREA,
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
    def get_task_7(
        update_count: int = 0,
        updates_per_task: int = 100,
        default_threshold: float = .2,
        games_count: int = 300
    ):
        behaviors = [
            AttackerBehaviorUtils.get_own_team_from_model_behavior(
                0,
                PositionEnum.RELATIVE_TO_BALL,
                updates_per_task),
            AttackerBehaviorUtils.get_stopped_behavior(
                1,
                False,
                PositionEnum.OWN_AREA_EXCEPT_GOAL_AREA,
                updates_per_task),
            AttackerBehaviorUtils.get_stopped_behavior(
                2,
                False,
                PositionEnum.GOAL_AREA,
                updates_per_task),
            AttackerBehaviorUtils.get_opponent_team_from_model_behavior(
                0,
                PositionEnum.RELATIVE_TO_BALL,
                updates_per_task),
            AttackerBehaviorUtils.get_opponent_team_ball_following_behavior(
                1,
                updates_per_task),
            AttackerBehaviorUtils.get_stopped_behavior(
                2,
                True,
                PositionEnum.GOAL_AREA,
                updates_per_task)
        ]
    
        ball_behavior = AttackerBehaviorUtils.get_ball_behavior(
            PositionEnum.OWN_AREA,
            updates_per_task
        )

        return CurriculumTask(
            "7",
            behaviors,
            ball_behavior,
            update_count=update_count,
            updates_per_task=updates_per_task,
            default_threshold=default_threshold,
            games_count=games_count)
    
    @staticmethod
    def get_task_8(
        update_count: int = 0,
        updates_per_task: int = 100,
        default_threshold: float = .1,
        games_count: int = 300
    ):
        behaviors = [
            AttackerBehaviorUtils.get_own_team_from_model_behavior(
                0,
                PositionEnum.RELATIVE_TO_BALL,
                updates_per_task),
            AttackerBehaviorUtils.get_ball_following_behavior(
                1,
                False,
                PositionEnum.OWN_AREA_EXCEPT_GOAL_AREA,
                True,
                None,
                True,
                [.2, .2],
                updates_per_task=updates_per_task),
            AttackerBehaviorUtils.get_goalkeeper_ball_following_behavior(
                2,
                False,
                updates_per_task),
            AttackerBehaviorUtils.get_opponent_team_from_model_behavior(
                0,
                PositionEnum.RELATIVE_TO_BALL,
                updates_per_task),
            AttackerBehaviorUtils.get_opponent_team_ball_following_behavior(
                1,
                updates_per_task),
            AttackerBehaviorUtils.get_goalkeeper_ball_following_behavior(
                2,
                True,
                updates_per_task)
        ]
    
        ball_behavior = AttackerBehaviorUtils.get_ball_behavior(
            PositionEnum.OWN_AREA,
            updates_per_task
        )

        return CurriculumTask(
            "8",
            behaviors,
            ball_behavior,
            update_count=update_count,
            updates_per_task=updates_per_task,
            default_threshold=default_threshold,
            games_count=games_count)
    
    @staticmethod
    def get_stopped_behavior(
        robot_id: int,
        is_yellow: bool,
        position_enum: PositionEnum,
        updates_per_task: int
    ):
        builder = RobotCurriculumBehaviorBuilder(
            robot_id,
            is_yellow,
            RobotCurriculumBehaviorEnum.BALL_FOLLOWING,
            updates_per_task
        )

        return builder\
            .set_position_enum(position_enum)\
            .set_velocity_alpha_range([0, 0], True)\
            .build()
    
    @staticmethod
    def get_own_team_from_model_behavior(
        robot_id: int,
        position_enum: PositionEnum,
        updates_per_task: int
    ):
        builder = RobotCurriculumBehaviorBuilder(
            robot_id,
            False,
            RobotCurriculumBehaviorEnum.FROM_MODEL,
            updates_per_task
        )

        return builder\
            .set_position_enum(position_enum)\
            .set_distance_range((.2, .5), True)\
            .build()
    
    @staticmethod
    def get_opponent_team_from_model_behavior(
        robot_id: int,
        position_enum: PositionEnum,
        updates_per_task: int
    ):
        builder = RobotCurriculumBehaviorBuilder(
            robot_id,
            True,
            RobotCurriculumBehaviorEnum.FROM_MODEL,
            updates_per_task
        )

        return builder\
            .set_position_enum(position_enum)\
            .set_distance_range((.3, .6), True)\
            .set_velocity_alpha_range((0, .5), True)\
            .build()
    
    @staticmethod
    def get_ball_following_behavior(
        robot_id: int,
        is_yellow: bool,
        position_enum: PositionEnum,
        distance_range: 'tuple[float, float] | None',
        velocity_alpha_range: 'tuple[float, float] | None',
        updates_per_task: int
    ):
        builder = RobotCurriculumBehaviorBuilder(
            robot_id,
            is_yellow,
            RobotCurriculumBehaviorEnum.BALL_FOLLOWING,
            updates_per_task
        )

        builder.set_position_enum(position_enum)

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
            RobotCurriculumBehaviorEnum.BALL_FOLLOWING,
            updates_per_task
        )

        return builder\
            .set_position_enum(PositionEnum.RELATIVE_TO_BALL)\
            .set_distance_range((.3, .6), True)\
            .set_velocity_alpha_range((0, .5), True)\
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
            updates_per_task
        )

        return builder\
            .set_position_enum(PositionEnum.GOAL_AREA)\
            .set_velocity_alpha_range([.2, .2], True)\
            .build()
    
    @staticmethod
    def get_ball_behavior(
        position_enum: PositionEnum,
        updates_per_task: int = 10,
        distance_range: 'tuple[float, float] | None' = None
    ):
        return BallCurriculumBehavior(
            position_enum=position_enum,
            updates_per_task=updates_per_task,
            distance_range=distance_range)