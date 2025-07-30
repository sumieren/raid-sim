from log import log_action;

class Skill:
    def __init__(self, name, cooldown, effect_function, job_lock=None):
        self.name = name
        self.cooldown = cooldown
        self.current_cooldown = 0
        self.effect = effect_function

        self.description = ""

    @log_action
    def cast(self, user, target):
        return self.effect(self, user, target)
    