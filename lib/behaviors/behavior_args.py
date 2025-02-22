from lib.domain.enums.role_enum import RoleEnum

class BehaviorArgs:
    def __init__(
        self,
        role_enum: 'RoleEnum | None' = None
    ):
        self.role_enum = role_enum