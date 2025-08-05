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
            return f"{data["user"]} uses {data["skill"]} on {data["target"]}!"
        case "damage_dealt":
            if data["is_miss"]:
                return f"{data["skill"]} missed!"
            crit_str = "CRITICAL! " if data["is_crit"] else ""
            return f"{crit_str}{data["skill"]} deals {data["damage"]} damage to {data["target"]}!"
        
        case "boss_damage":
            if data["is_dodge"]:
                return f"{data["target"]} dodged {data["attack"]}!"
            block_str = "BLOCK! " if data["is_block"] else ""
            return f"{block_str}{data["attack"]} deals {data["damage"]} damage to {data["target"]}."
        case _:
            raise Exception("Unexpected event_type sent to logger, check for typos")

def log_skill(func):
    def wrapper(skill, user, targets, *args, **kwargs):
        result = func(skill, user, targets, *args, **kwargs)

        return result, [_emit_event('skill_use', {
            'user': user.name,
            'target': targets.name,
            'skill': skill.name
        })]
    return wrapper

def log_damage(skill, damage, targets, is_crit=False, is_miss=False):
    log = []
    for target in targets:
        log.append(_emit_event('damage_dealt', {
            'skill': skill.name,
            'damage': damage,
            'is_crit': is_crit,
            'is_miss': is_miss,
            'target': target.name,
        }))
    return log

def log_boss_damage(attack_name, damage, targets, is_dodge=False, is_block=False):
    log = []
    for target in targets:
        log.append(_emit_event('boss_damage', {
            'attack': attack_name,
            'damage': damage,
            'is_dodge': is_dodge,
            'is_block': is_block,
            'target': target.name,
        }))
    return log

# TO DO make it work with emit_event
def log_bonus_action(giver, receiver):
    return [f"[SYNERGY] Lucky! {giver.name} triggered a bonus action for {receiver.name}!"]
