import numpy as np
from lib.curriculum.position_setup.position_setup import PositionSetup

class BallCurriculumBehavior:
    def __init__(
        self,
        updates_per_task: int,
        position_setup: PositionSetup,
        distance_range: 'tuple[float, float] | None' = None
    ):
        self.updates_per_task = updates_per_task
        self.distance_range = distance_range
        self.position_setup = position_setup

        self.updates = 0
        
        if distance_range is None:
            self.distance = None
            self.distance_beta = None
        else:
            self.distance = distance_range[0]
            
            self.distance_beta = BallCurriculumBehavior._get_beta(
                distance_range,
                updates_per_task
            )
            
    def update(self, times: int = 1):
        if self.distance_range is not None:
            def clip(value: float, range: 'tuple[float, float]'):
                if range[0] > range[1]:
                    return np.clip(value, range[1], range[0])
                
                return np.clip(value, range[0], range[1])

            self.distance = clip(
                self.distance + self.distance_beta * times,
                self.distance_range)
            
            self.updates = clip(self.updates + times, (0, self.updates_per_task))

    def reset(self):
        if self.distance_range is not None:
            self.distance = self.distance_range[0]

        self.updates = 0
    
    def is_over(self):
        return self.updates == self.updates_per_task

    @staticmethod
    def _get_beta(
        range: 'tuple[float, float]',
        updates_per_task: int
    ):
        return (range[1] - range[0]) / updates_per_task