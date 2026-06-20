import inspect
from collections.abc import Callable
from typing import Any


class Container:
    def __init__(self) -> None:
        self._registry: dict[type, Callable[[], Any]] = {}

    def register(self, cls: type, factory: Callable[[], Any] | None = None) -> None:
        self._registry[cls] = factory or (lambda: cls())

    def __setitem__(self, cls: type, instance: Any) -> None:
        self._registry[cls] = lambda: instance

    def resolve(self, target: type | Callable) -> Any:
        if isinstance(target, type) and target in self._registry:
            return self._registry[target]()

        sig = inspect.signature(target)
        kwargs = {
            p.name: self._registry[p.annotation]()
            for p in sig.parameters.values()
            if p.annotation in self._registry
        }
        return target(**kwargs)


container = Container()
