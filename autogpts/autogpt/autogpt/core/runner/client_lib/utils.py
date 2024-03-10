import asyncio
import functools
import sys
from typing import Any, Callable, Coroutine, ParamSpec, TypeVar

if sys.version_info >= (3, 7):
    asyncio.run = asyncio.run  # type: ignore
else:
    asyncio.run = lambda coro: coro()  # type: ignore


P = ParamSpec("P")
T = TypeVar("T")


def handle_exceptions(
    application_main: Callable[P, T],
    with_debugger: bool,
) -> Callable[P, T]:
    """Wraps a function so that it drops a user into a debugger if it raises an error.

    This is intended to be used as a wrapper for the main function of a CLI application.
    It will catch all errors and drop a user into a debugger if the error is not a
    `KeyboardInterrupt`. If the error is a `KeyboardInterrupt`, it will raise the error.
    If the error is not a `KeyboardInterrupt`, it will log the error and drop a user
    into a debugger if `with_debugger` is `True`.
    If `with_debugger` is `False`, it will raise the error.

    Parameters
    ----------
    application_main
        The function to wrap.
    with_debugger
        Whether to drop a user into a debugger if an error is raised.

    Returns
    -------
    Callable
        The wrapped function.

    """

    @functools.wraps(application_main)
    async def wrapped(*args: P.args, **kwargs: P.kwargs) -> T:
        try:
            return await application_main(*args, **kwargs)
        except (BdbQuit, KeyboardInterrupt, click.Abort):
            raise
        except Exception as e:
            if with_debugger:
                print(f"Uncaught exception {e}")
                import pdb

                pdb.post_mortem()
            else:
                raise

    return wrapped


def coroutine(f: Callable[P, Coroutine[Any, Any, T]]) -> Callable[P, T]:
    """A decorator for coroutine functions that ensures proper error handling.

    This decorator wraps a coroutine function so that it catches any exceptions and
    either logs them or drops the user into a debugger, depending on the `with_
