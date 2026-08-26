from __future__ import annotations

from pathlib import Path
import os
from typing import Iterable, Optional


CALLER_DIR_ENV_KEYS = (
    "SKILL_CALLER_DIR",
    "AGENT_SKILL_CALLER_DIR",
)
PROJECT_ENV_KEYS = (
    "SKILL_PROJECT",
    "SKILL_PROJECT_NAME",
    "AGENT_SKILL_PROJECT",
)
PROJECTS_ROOT_ENV_KEYS = (
    "SKILL_PROJECTS_ROOT",
    "SKILL_PROJECT_ROOT",
    "PROJECTS_ROOT",
)

def _resolve_directory(path: Optional[str | Path], default: Path) -> Path:
    candidate = Path(path).expanduser() if path else default
    resolved = candidate.resolve()
    if resolved.is_file():
        return resolved.parent
    return resolved


def _iter_directory_chain(directory: Path) -> Iterable[Path]:
    yield directory
    yield from directory.parents


def _env_caller_dir() -> Optional[Path]:
    for key in CALLER_DIR_ENV_KEYS:
        value = os.environ.get(key)
        if value and value.strip():
            return Path(value.strip()).expanduser()
    return None


def _first_env_value(keys: Iterable[str]) -> Optional[str]:
    for key in keys:
        value = os.environ.get(key)
        if value and value.strip():
            return value.strip()
    return None


def _normalize_project_name(project: Optional[str]) -> Optional[str]:
    if project is None:
        project = _first_env_value(PROJECT_ENV_KEYS)
    if project is None:
        return None
    normalized = project.strip()
    if not normalized:
        return None
    if any(separator in normalized for separator in ("/", "\\", ":", os.sep)):
        raise ValueError(f"Project name must be a simple directory name: {project}")
    return normalized


def _iter_projects_roots(
    anchors: Iterable[Path],
    projects_root: Optional[str | Path],
) -> Iterable[Path]:
    explicit_root = projects_root or _first_env_value(PROJECTS_ROOT_ENV_KEYS)
    if explicit_root:
        yield Path(explicit_root).expanduser().resolve()

    for anchor in anchors:
        for directory in _iter_directory_chain(anchor):
            yield directory

    well_known_roots = [
        Path("D:/Project"),
        Path("/mnt/d/Project"),
        Path("/root/Project"),
    ]
    try:
        well_known_roots.append(Path.home() / "Project")
    except RuntimeError:
        pass

    for candidate in well_known_roots:
        yield candidate.expanduser()


def _iter_project_env_dirs(
    anchors: Iterable[Path],
    project: Optional[str],
    project_names: Optional[Iterable[str]],
    projects_root: Optional[str | Path],
) -> Iterable[Path]:
    explicit_project = _normalize_project_name(project)
    if explicit_project:
        names = (explicit_project,)
    elif project_names is not None:
        names = tuple(project_names)
    else:
        return

    visited_roots: set[Path] = set()
    for root in _iter_projects_roots(anchors, projects_root):
        try:
            resolved_root = root.resolve()
        except OSError:
            resolved_root = root
        if resolved_root in visited_roots:
            continue
        visited_roots.add(resolved_root)

        for name in names:
            candidate = resolved_root / name
            if candidate.exists():
                yield candidate


def discover_default_env_file(
    start_dir: Optional[str | Path] = None,
    caller_dir: Optional[str | Path] = None,
    home_dir: Optional[str | Path] = None,
    project: Optional[str] = None,
    project_names: Optional[Iterable[str]] = None,
    projects_root: Optional[str | Path] = None,
) -> Path:
    resolved_caller_dir = caller_dir or _env_caller_dir()
    selected_project = _normalize_project_name(project)
    workspace_dir = _resolve_directory(start_dir, Path.cwd())
    anchors = [workspace_dir]

    search_dirs: list[Path] = []
    if resolved_caller_dir is not None:
        caller_directory = _resolve_directory(resolved_caller_dir, Path.cwd())
        anchors.insert(0, caller_directory)
        search_dirs.extend(_iter_directory_chain(caller_directory))
    project_dirs = list(
        _iter_project_env_dirs(
            anchors=anchors,
            project=selected_project,
            project_names=project_names,
            projects_root=projects_root,
        )
    )
    search_dirs.extend(project_dirs)
    search_dirs.extend(_iter_directory_chain(workspace_dir))

    if home_dir is not None:
        search_dirs.extend(_iter_directory_chain(_resolve_directory(home_dir, workspace_dir)))
    else:
        try:
            search_dirs.extend(_iter_directory_chain(Path.home().resolve()))
        except RuntimeError:
            pass

    visited: set[Path] = set()
    project_dir_set = set(project_dirs)
    for directory in search_dirs:
        if directory in visited:
            continue
        visited.add(directory)
        candidate = directory / ".env"
        if candidate.exists():
            return candidate
        if selected_project and directory in project_dir_set:
            return candidate

    return workspace_dir / ".env"


def _append_existing_env_path(paths: list[Path], seen: set[Path], path: Path) -> None:
    try:
        resolved = path.expanduser().resolve()
    except OSError:
        resolved = path.expanduser()
    if resolved in seen or not resolved.exists():
        return
    seen.add(resolved)
    paths.append(resolved)


def iter_env_file_candidates(
    start_dir: Optional[str | Path] = None,
    caller_dir: Optional[str | Path] = None,
    home_dir: Optional[str | Path] = None,
    project: Optional[str] = None,
    project_names: Optional[Iterable[str]] = None,
    projects_root: Optional[str | Path] = None,
    env_file: Optional[str | Path] = None,
    extra_dirs: Optional[Iterable[str | Path]] = None,
) -> list[Path]:
    if env_file:
        return [Path(env_file).expanduser().resolve()]

    resolved_caller_dir = caller_dir or _env_caller_dir()
    selected_project = _normalize_project_name(project)
    workspace_dir = _resolve_directory(start_dir, Path.cwd())
    anchors = [workspace_dir]

    search_dirs: list[Path] = []
    if resolved_caller_dir is not None:
        caller_directory = _resolve_directory(resolved_caller_dir, Path.cwd())
        anchors.insert(0, caller_directory)
        search_dirs.extend(_iter_directory_chain(caller_directory))

    search_dirs.extend(
        _iter_project_env_dirs(
            anchors=anchors,
            project=selected_project,
            project_names=project_names,
            projects_root=projects_root,
        )
    )
    search_dirs.extend(_iter_directory_chain(workspace_dir))

    if extra_dirs is not None:
        for directory in extra_dirs:
            search_dirs.extend(_iter_directory_chain(_resolve_directory(directory, workspace_dir)))

    if home_dir is not None:
        resolved_home = _resolve_directory(home_dir, workspace_dir)
    else:
        try:
            resolved_home = Path.home().resolve()
        except RuntimeError:
            resolved_home = None

    paths: list[Path] = []
    seen: set[Path] = set()
    for directory in search_dirs:
        _append_existing_env_path(paths, seen, directory / ".env")

    if resolved_home is not None:
        for candidate in (
            # shark-agent keeps every credential outside the repo, here.
            resolved_home / ".config" / "shark-agent" / ".env",
            resolved_home / ".config" / "agent-skills" / ".env",
            resolved_home / ".codex" / "skills" / ".env",
            resolved_home / ".env",
        ):
            _append_existing_env_path(paths, seen, candidate)
        for directory in _iter_directory_chain(resolved_home):
            _append_existing_env_path(paths, seen, directory / ".env")

    return paths


def read_env_file_values(path: str | Path) -> dict[str, str]:
    env_path = Path(path).expanduser().resolve()
    try:
        from dotenv import dotenv_values
    except ImportError:
        dotenv_values = None

    if dotenv_values is not None:
        raw_values = dotenv_values(env_path)
        return {
            str(key): str(value)
            for key, value in raw_values.items()
            if value is not None
        }

    values: dict[str, str] = {}
    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        if not key:
            continue
        values[key] = value.strip().strip('"').strip("'")
    return values


def load_project_env(
    env_file: Optional[str],
    *,
    default_env_file: Optional[Path] = None,
    project: Optional[str] = None,
) -> Path:
    env_path = (
        Path(env_file).expanduser().resolve()
        if env_file
        else (default_env_file or discover_default_env_file(project=project))
    )

    try:
        from dotenv import load_dotenv
    except ImportError:
        load_dotenv = None

    if env_file and not env_path.exists():
        raise FileNotFoundError(f"Env file does not exist: {env_path}")

    if load_dotenv is not None and env_path.exists():
        load_dotenv(dotenv_path=env_path, override=False)

    return env_path
