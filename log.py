def log_action(func):
    def wrapper(self, user, target, *args, **kwargs):
        print(f"{user.name} uses {self.name} on {target.name}!")

        result = func(self, user, target, *args, **kwargs)
        if result:
            print(result)

        return result

    return wrapper