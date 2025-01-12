class FIRASimUtils:
    @staticmethod
    def correct_position(
        x: float,
        y: float,
        is_left_team: bool):
        
        if is_left_team:
            return x, y 
        
        return -x, -y
    
    @staticmethod
    def correct_speed(
        x: float,
        y: float,
        is_left_team: bool):

        if is_left_team:
            return x, y 
        
        return -x, -y