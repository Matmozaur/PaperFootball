from controller import config


def log(*args, logger=config.LOG):
    if logger:
        print(args)

