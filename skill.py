from log import log_skill;

class Skill:
    def __init__(self, name, description, cooldown, effect_function, job_lock=None):
        self.name = name
        self.description = description

        self.cooldown = cooldown
        self.current_cooldown = 0
        self.turns_off_cooldown = 0

        self.effect = effect_function

    @log_skill
    def cast(self, user, targets):
        self.current_cooldown = self.cooldown + 1

        if self.turns_off_cooldown > 0:
            self.turns_off_cooldown = 0

        return self.effect(self, user, targets)
    
    def pass_turn(self):
        # If skill has a cooldown, reduce cd by 1. 
        # If skill has a cooldown and wasn't used, increment turns_off_cooldown
        if self.cooldown != 0:
            if self.current_cooldown > 0:
                self.current_cooldown -= 1
            else:
                self.turns_off_cooldown += 1
    