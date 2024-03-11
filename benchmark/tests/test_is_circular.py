from agbenchmark.utils.dependencies.graphs import is_circular


def test_is_circular():
    cyclic_graph = {
        "nodes": [
            {"id": "A", "data": {"category": []}},
            {"id": "B", "data": {"category": []}},
            {"id": "C", "data": {"category": []}},
            {"id": "D", "data": {"category": []}},
        ],
        "edges": [
            ("A", "B"),
            ("B", "C"),
            ("C", "D"),
            ("D", "A"),
        ],
    }

    result = is_circular(cyclic_graph)
    assert result is not None, "Expected a cycle, but none was detected"
    assert all(
        (edge in cyclic_graph["edges"]) for edge in result
    ), "The detected cycle path is not part of the graph's edges"


def test_is_not_circular():
    acyclic_graph = {
        "nodes": [
            {"id": "A", "data": {"category": []}},
            {"id": "B", "data": {"category": []}},
            {"id": "C", "data": {"category": []}},
            {"id": "D", "data": {"category": []}},
        ],
        "edges": [
            ("A", "B"),
            ("B", "C"),
            ("C", "D"),
        ],
    }

    assert is_circular(acyclic_graph) is None, "Detected a cycle in an acyclic graph"
