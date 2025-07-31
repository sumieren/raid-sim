def _emit_event(event_type, data):
    """
    Private function that handles the event and returns the appropriate message.

    event_type == skill_use
    Expects skill object, hero object and target (hero or boss object)

    event_type == damage_dealt
    Expect skill object, damage numbers and target (hero or boss object)
    """

    match (event_type):
        case "skill_use":
            print(f"{data["user"]} uses {data["skill"]} on {data["targets"]}!")
        case "damage_dealt":
            crit_str = "CRITICAL! " if data["is_crit"] else ""
            print(f"{crit_str}{data["skill"]} deals {data["damage"]} damage to {data["targets"]}!")
        case _:
            raise Exception("Unexpected event_type sent to logger, check for typos")

def log_skill(func):
    def wrapper(skill, user, targets, *args, **kwargs):
        result = func(skill, user, targets, *args, **kwargs)

        _emit_event('skill_use', {
            'user': user.name,
            'targets': targets.name,
            'skill': skill.name
        })

        return result
    return wrapper

def log_damage(skill, damage, targets, is_crit=False):
    for target in targets:
        _emit_event('damage_dealt', {
            'skill': skill.name,
            'damage': damage,
            'is_crit': is_crit,
            'targets': target.name,
        })
