from jobs.registry import register_job
from jobs.job import Job

from skills.skills import disciplined_slash

@register_job
class Knight(Job):
    def __init__(self, rng):
        super().__init__(hp=10, mp=10, rng=rng)
        self.name = "Knight"

        self.skills = [disciplined_slash()]

    def take_turn(self, game_state):
        return self.skills[0].cast(self, game_state.boss)