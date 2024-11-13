"""Service module for agent."""

import importlib.util
import sys
from pathlib import Path
from types import ModuleType


class ModuleLoader:
    """A utility class for dynamically loading Python modules from import strings."""

    @staticmethod
    def load_from_string(import_string: str) -> ModuleType:
        """Load a module from an import string (dot notation).

        Args:
            import_string: Import path in dot notation (e.g., "myapp.main")

        Returns:
            The loaded module or attribute

        Example:
            loader.load_from_string("myapp.main.app")
        """
        module_path, _, attribute = import_string.partition(":")

        module_name = module_path.replace(".", "/")
        file_path = Path(module_name + ".py")

        spec = importlib.util.spec_from_file_location(module_name, str(file_path))
        if spec is None or spec.loader is None:
            msg = f"Failed to create module spec for {file_path}"
            raise ImportError(msg)

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        return getattr(module, attribute)
