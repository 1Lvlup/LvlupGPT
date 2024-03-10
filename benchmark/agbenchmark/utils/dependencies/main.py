import collections
import json
import os
from typing import Any, DefaultDict, Generator, List, NamedTuple, Set

import colorama
import networkx
from _pytest.nodes import Item

from .constants import MARKER_KWARG_DEPENDENCIES, MARKER_NAME
from .graphs import graph_interactive_network
from .util import clean_nodeid, get_absolute_nodeid, get_markers, get_name


class Result(NamedTuple):
    when: str
    outcome: str


@dataclass
class TestResult:
    nodeid: str
    results: DefaultDict[str, List[Result]] = collections.defaultdict(list)

    @property
    def success(self) -> bool:
        return all(
            result.outcome in self.GOOD_OUTCOMES for step, results in self.results.items() for result in results
        )


@dataclass
class TestDependencies:
    nodeid: str
    dependencies: Set[str] = set()
    unresolved: Set[str] = set()


class DependencyManager:
    def __init__(self) -> None:
        self.options: dict[str, Any] = {}
        self._items: List[Item] | None = None
        self._name_to_nodeids: DefaultDict[str, List[str]] = collections.defaultdict(list)
        self._nodeid_to_item: DefaultDict[str, Item] = collections.defaultdict(Item)
        self._results: DefaultDict[str, TestResult] = collections.defaultdict(TestResult)
        self._dependencies: DefaultDict[str, TestDependencies] = collections.defaultdict(TestDependencies)

    @property
    def items(self) -> List[Item]:
        return self._items

    @items.setter
    def items(self, items: List[Item]) -> None:
        if self._items is not None:
            raise AttributeError("The items attribute has already been set")
        self._items = items

        for item in items:
            nodeid = clean_nodeid(item.nodeid)
            self._nodeid_to_item[nodeid] = item
            name = get_name(item)
            self._name_to_nodeids[name].append(nodeid)
            self._results[nodeid] = TestResult(clean_nodeid(item.nodeid))

        for item in items:
            nodeid = clean_nodeid(item.nodeid)
            self._dependencies[nodeid] = TestDependencies(nodeid)

            markers = get_markers(item, MARKER_NAME)
            dependencies = [
                dep
                for marker in markers
                for dep in marker.kwargs.get(MARKER_KWARG_DEPENDENCIES, [])
            ]
            for dependency in dependencies:
                # If the name is not known, try to make it absolute (ie file::[class::]method)
                if dependency not in self._name_to_nodeids:
                    absolute_dependency = get_absolute_nodeid(dependency, nodeid)
                    if absolute_dependency in self._name_to_nodeids:
                        dependency = absolute_dependency

                # Add all items matching the name
                if dependency in self._name_to_nodeids:
                    for nid in self._name_to_nodeids[dependency]:
                        self._dependencies[nodeid].dependencies.add(nid)
                else:
                    self._dependencies[nodeid].unresolved.add(dependency)

    def __iter__(self) -> Generator[Item, None, None]:
        return (self._nodeid_to_item[nodeid] for nodeid in self._nodeid_to_item)

    def __getitem__(self, nodeid: str) -> Item:
        return self._nodeid_to_item[nodeid]

    def __len__(self) -> int:
        return len(self._nodeid_to_item)

    @property
    def name_to_nodeids(self) -> dict[str, List[str]]:
        return self._name_to_nodeids

    @property
    def results(self) -> dict[str, TestResult]:
        return self._results

    @property
    def dependencies(self) -> dict[str, TestDependencies]:
        return self._dependencies

    def print_name_map(self, verbose: bool = False) -> None:
        print("Available dependency names:")
        for name, nodeids in sorted(self.name_to_nodeids.items(), key=lambda x: x[0]):
            if len(nodeids) == 1:
                if name == nodeids[0]:
                    # This is just the base name, only print this when verbose
                    if verbose:
                        print(f"  {name}")
                else:
                    # Name refers to a single node id, so use the short format
                    print(f"  {name} -> {nodeids[0]}")
            else:
                # Name refers to multiple node ids, so use the long format
                print(f"  {name} ->")
                for
