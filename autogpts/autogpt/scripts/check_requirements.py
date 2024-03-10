import contextlib
import os
import sys
from importlib.metadata import version
from poetry.core.constraints.version import Version
from poetry.core.dependency import Dependency
from poetry.factory import Factory

def check_dependencies():
    try:
        import poetry.factory  # noqa
    except ModuleNotFoundError:
        os.system(f"{sys.executable} -m pip install 'poetry>=1.6.1,<2.0.0'")
        return

    poetry_project = Factory().create_poetry()
    dependency_group = poetry_project.package.dependency_group("main")

    missing_packages = []
    for dep in dependency_group.dependencies:
        if not dep.is_optional():
            try:
                installed_version = version(dep.name)
            except ModuleNotFoundError:
                missing_packages.append(str(dep))
                continue

            constraint = dep.constraint
            if constraint is not None and not constraint.allows(Version.parse(installed_version)):
                missing_packages.append(str(dep))

    if missing_packages:
        print("Missing packages:")
        print(", ".join(missing_packages))
        sys.exit(1)

if __name__ == "__main__":
    check_dependencies()
