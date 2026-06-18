import inspect
from collections.abc import Callable
from typing import Any

from fastapi import Depends


class Container:
    def __init__(self) -> None:
        self._registry: dict[type, Callable[[], Any]] = {}

    def register(self, cls: type, factory: Callable[[], Any] | None = None) -> None:
        self._registry[cls] = factory or (lambda: cls())

    def resolve(self, cls: type) -> Any:
        factory = self._registry.get(cls)
        if factory is None:
            msg = f"No factory registered for {cls.__name__}"
            raise KeyError(msg)
        return factory()

    def register_module(self, module_fn: Callable) -> None:
        sig = inspect.signature(module_fn)
        for param in sig.parameters.values():
            default = param.default
            if isinstance(default, Depends):
                dep_cls = default.dependency
                if dep_cls and dep_cls not in self._registry:
                    self.register(dep_cls)


container = Container()
