from enum import Enum, auto

class BossState(Enum):
    STUNNED = auto(),
    STANDARD = auto(),
    CHARGING = auto(),
    WARNING = auto(),
    INVULNERABLE = auto(),

class Boss:
    def __init__(self, hp, rng):
        self.name = ""
        self.rng = rng

        self._hp = hp
        self._cur_hp = self._hp

        self.stagger = 100
        self._cur_stagger = 0

        self.state = BossState.STANDARD

        self.phases = []
        self._cur_phase = None

        self.next_action = None
        self.telegraph_targets = []

    def take_turn(self, game_state):
        # Reset telegraph targets
        self.telegraph_targets = []

        # If no next action, generate one, then use the next action.
        if self.next_action is None:
            self.next_action = self._cur_phase.get_next_action()
        self.next_action = self.next_action(game_state)


    def end_turn(self, game_state):
        pass

    def take_damage(self, damage):
        self._cur_hp -= damage

        if self._cur_hp < 0:
            self._cur_hp = 0

    def take_stagger(self, stagger):
        print(f"Boss took {stagger} stagger dmg!")
        self._cur_stagger += stagger

        if self._cur_stagger >= self.stagger:
            # override upcoming back and targets to a 2 turn stun and erase the target list
            self.next_action = lambda game_state: self.be_stunned(2)
            self.telegraph_targets = []

    def be_stunned(self, turn_count):
        turn_count -= 1
        
        if turn_count > 0:
            return lambda game_state: self.be_stunned(turn_count)
        else:
            return None

    def deal_damage(self, attack_name, min_dmg, max_dmg, targets):
        base_dmg = self.rng.randint(min_dmg, max_dmg)
        print(f"dealing {base_dmg} damage to {targets}")
        return {
            'type': 'damage',
            'attack_name': attack_name,
            'user': self,
            'damage': base_dmg,
            'targets': targets,
        }

    @property
    def hp(self):
        return self._cur_hp
    
    @property
    def max_hp(self):
        return self._hp
    
class Phase:
    def __init__(self, rng, rot_type, moves):
        self.rng = rng
        self.rot_type = rot_type   # Either 'random' or 'loop'
        self.moves = moves
        self.index = 0             # Used for 'loop' rot_type

    def get_next_action(self):
        if self.rot_type == "random":
            return self.rng.choice(self.moves)
        elif self.rot_type == "loop":
            # loop
            pass
        else:
            raise ValueError("Invalid rotation type passed to Phase")

class TrainingDummy(Boss):
    def __init__(self, rng):
        super().__init__(hp=100, rng=rng)
        self.name = "Training Dummy"

        self._cur_phase = Phase(rng, "random", [self.slap])

    def slap(self, game_state):
        self.deal_damage("Slap", 1, 1, game_state.party.members)
        return None