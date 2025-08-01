from skill import Skill

def fn_disciplined_slash(skill, user, target):
    damage = user.rng.randint(2,4)
    return {
        "type": "damage",
        "damage": damage,
        "user": user,
        "targets": [target],
        "skill": skill
    }
def disciplined_slash(): return Skill(
        name="Disciplined Slash",
        description="A powerful slash at a single enemy.",
        cooldown=0,
        effect_function=fn_disciplined_slash
    )

def fn_fireball(skill, user, target):
    damage = user.rng.randint(5,10)
    return {
        "type": "damage",
        "damage": damage,
        "user": user,
        "targets": [target],
        "skill": skill
    }
def fireball(): return Skill(
    name="Fireball",
    description="Fling a ball of fire at a single enemy.",
    cooldown=1,
    effect_function=fn_fireball
)

