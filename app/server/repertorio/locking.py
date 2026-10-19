"""Bloqueio exclusivo e imediato do acervo em macOS e Windows."""
import errno
import sys


def lock_file(file):
    if sys.platform == 'win32':
        import msvcrt
        file.seek(0)
        try:
            msvcrt.locking(file.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError as exc:
            if exc.errno not in {errno.EACCES, errno.EAGAIN, errno.EDEADLK}:
                raise
            raise BlockingIOError(exc.errno, 'O acervo já está em uso.') from exc
    else:
        import fcntl
        fcntl.flock(file, fcntl.LOCK_EX | fcntl.LOCK_NB)
