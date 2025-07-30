from skill import Skill

def fn_disciplined_slash(skill, user, target):
    skill.description = "A powerful slash at a single enemy."

    damage = user.rng.randint(2,4)
    target.take_damage(damage)
    return {
        "type": "damage",
        "amount": damage,
        "user": user,
        "targets": target,
        "skill": skill
    }
disciplined_slash = Skill(
    name="Disciplined Slash",
    cooldown=0,
    effect_function=fn_disciplined_slash
)
