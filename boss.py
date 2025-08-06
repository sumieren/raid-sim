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

        self._stun_threshold = 100
        self._cur_stagger = 0
        self._stun_reset_pending = False

        self.state = BossState.STANDARD

        self.phases = []
        self._cur_phase = None

        self.next_action = None
        self.telegraph_targets = []

    def take_turn(self, game_state):
        tuples = []

        # Reset telegraph targets
        self.telegraph_targets = []

        # If no next action, generate one, then use the next action.
        if self.next_action is None:
            self.next_action = self._cur_phase.get_next_action()
        self.next_action, action_data, msg = self.next_action(game_state)
        tuples.append((action_data, msg))

        return tuples


    def end_turn(self, game_state):
        # But if the boss is on the last stun turn reset the gauge
        if self.state == BossState.STUNNED and self.next_action is None:
            self.state = BossState.STANDARD
            self._cur_stagger = 0
            self._stun_reset_pending = False
            print(f"{self.name} recovers from stun.")

    def take_damage(self, damage):
        self._cur_hp -= damage

        if self._cur_hp < 0:
            self._cur_hp = 0

    def take_stagger(self, stagger):
        self._cur_stagger += stagger

        if self._cur_stagger >= self.stun_threshold:
            if self.state is not BossState.STUNNED:
                # override upcoming back and targets to a 2 turn stun and erase the target list
                self.state = BossState.STUNNED
                self.next_action = lambda game_state: self.be_stunned(2)
                self.telegraph_targets = []
                self._cur_stagger = self.stun_threshold
            else:
                # If boss already stunned, just clamp stagger to max for now.
                self._cur_stagger = self.stun_threshold
    def be_stunned(self, turn_count, first=True):
        if first:
            log = [f"{self.name} was stunned!"]
        else:
            log = [f"{self.name} is stunned and took additional damage from all attacks!"]
        
        if turn_count > 0:
            return lambda game_state: self.be_stunned(turn_count-1, first=False), None, log
        else:
            return None, None, log
        
    def trigger_interrupt(self):
        self.state = BossState.STANDARD
        self.next_action = lambda game_state: self.be_interrupted()
        self.telegraph_targets = []
    def be_interrupted(self):
        log = [f"{self.name}'s attack was interrupted!"]
        return None, None, log

    def deal_damage(self, attack_name, min_dmg, max_dmg, targets, dodgeable=True):
        base_dmg = self.rng.randint(min_dmg, max_dmg)
        return {
            'type': 'damage',
            'attack_name': attack_name,
            'user': self,
            'damage': base_dmg,
            'targets': targets,
            'dodgeable': dodgeable,
        }

    @property
    def hp(self):
        return self._cur_hp
    
    @property
    def max_hp(self):
        return self._hp
    
    @property
    def stagger(self):
        return self._cur_stagger
    
    @property
    def stun_threshold(self):
        return self._stun_threshold
    
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
        action = self.deal_damage("Slap", 1, 1, game_state.party.members)
        log = [f"{self.name} slaps everyone!"]
        return None, action, log