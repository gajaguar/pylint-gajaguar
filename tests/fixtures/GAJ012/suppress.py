def fires():
    try:
        do_something()
    except ValueError:
        pass


def fires_multiple():
    try:
        do_something()
    except ValueError:
        pass
    except (KeyError, OSError) as error:
        pass


def bare_is_silent():
    try:
        do_something()
    except:
        pass


def with_else():
    try:
        do_something()
    except ValueError:
        pass
    else:
        do_other()


def with_finally():
    try:
        do_something()
    except ValueError:
        pass
    finally:
        cleanup()


def handler_does_work():
    try:
        do_something()
    except ValueError:
        log()


def handler_two_statements():
    try:
        do_something()
    except ValueError:
        pass
        pass


def only_finally():
    try:
        do_something()
    finally:
        cleanup()


def mixed_handlers():
    try:
        do_something()
    except ValueError:
        pass
    except KeyError:
        log()


def nested():
    try:
        try:
            do_something()
        except ValueError:
            pass
    except KeyError:
        log()


def star_is_silent():
    try:
        do_something()
    except* ValueError:
        pass
