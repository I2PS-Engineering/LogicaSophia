"""No-shell, scoped read-only filesystem tools; reject symlinks at every path component."""
from __future__ import annotations
import hashlib
import os
import stat
import time
from pathlib import Path
from .contracts import valid_path

MAX_FILE = 65536
MAX_SEARCH_FILES = 32
MAX_SEARCH_SECONDS = 3


class ObservationError(Exception):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


def read_scoped(workspace: Path, relative: str) -> bytes:
    valid_path(relative)
    if workspace.is_symlink() or not workspace.is_dir():
        raise ObservationError('invalid_workspace')
    descriptors = []
    try:
        fd = os.open(str(workspace), os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        descriptors.append(fd)
        for part in relative.split('/')[:-1]:
            fd = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            descriptors.append(fd)
        fd = os.open(relative.split('/')[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
        descriptors.append(fd)
        size = os.fstat(fd)
        if not stat.S_ISREG(size.st_mode) or size.st_size > MAX_FILE:
            raise ObservationError('non_regular_or_too_large')
        result = os.read(fd, MAX_FILE + 1)
        if len(result) > MAX_FILE:
            raise ObservationError('file_too_large')
        result.decode('utf-8', errors='strict')
        return result
    except (OSError, UnicodeError) as exc:
        raise ObservationError('file_unavailable_or_unsafe') from exc
    finally:
        for fd in reversed(descriptors):
            os.close(fd)


def read_observation(workspace: Path, path: str) -> dict:
    raw = read_scoped(workspace, path)
    return {'tool': 'read_file', 'path': path, 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw), 'exit_code': 0}


def ensure_scoped_directory(workspace: Path, folder: str) -> Path:
    valid_path(folder, allow_root=True)
    if workspace.is_symlink() or not workspace.is_dir():
        raise ObservationError('invalid_workspace')
    if folder == '.':
        return workspace
    fds = []
    try:
        fd = os.open(str(workspace), os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        fds.append(fd)
        for part in folder.split('/'):
            fd = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            fds.append(fd)
    except OSError as exc:
        raise ObservationError('invalid_search_directory') from exc
    finally:
        for fd in reversed(fds):
            os.close(fd)
    return workspace / folder


def search_observation(workspace: Path, folder: str, query: str) -> dict:
    valid_path(folder, allow_root=True)
    # Phase A directories are enumerated for discoverability, but all file reads
    # go through read_scoped to enforce dir-fd and O_NOFOLLOW checks.
    start = time.monotonic()
    root = ensure_scoped_directory(workspace, folder)
    matches, examined, truncated = [], 0, False
    for base, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if not d.startswith('.') and not (Path(base) / d).is_symlink())
        for name in sorted(files):
            if name.startswith('.'):
                continue
            if examined >= MAX_SEARCH_FILES or time.monotonic() - start > MAX_SEARCH_SECONDS:
                truncated = True
                break
            path = (Path(base) / name).relative_to(workspace).as_posix()
            examined += 1
            try:
                raw = read_scoped(workspace, path)
            except ObservationError:
                continue
            if query in raw.decode('utf-8'):
                matches.append({'path': path, 'sha256': hashlib.sha256(raw).hexdigest()})
        if truncated:
            break
    return {'tool': 'search_files', 'path': folder, 'matches': matches, 'files_examined': examined, 'truncated': truncated, 'exit_code': 0}
