from controller import config


def log(*args, logger=config.LOG):
    if logger:
        print(args)

def log_important(*args, logger=config.LOG_IMPORTANT):
    if logger:
        print(args)

