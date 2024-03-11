from agbenchmark.utils.dependencies.graphs import is_circular  # Import the is_circular function


def test_is_circular():
    # Define a directed graph with a cycle
    cyclic_graph = {
        "nodes": [
            {"id": "A", "data": {"category": []}},
            {"id": "B", "data": {"category": []}},
            {"id": "C", "data": {"category": []}},
            {"id": "D", "data": {"category": []}},
        ],
        "edges": [
            ("A", "B"),  # Edge from A to B
            ("B", "C"),  # Edge from B to C
            ("C", "D"),  # Edge from C to D
            ("D", "A"),  # Edge from D to A, creating a cycle
        ],
    }

    # Test the is_circular function with the cyclic graph
    result = is_circular(cyclic_graph)

    # Assert that the function returns a result, indicating a cycle
    assert result is not None, "Expected a cycle, but none was detected"

    # Assert that all edges in the detected cycle path are part of the graph's edges
    assert all((edge in cyclic_graph["edges"]) for edge in result), (
        "The detected cycle path is not part of the graph's edges"
    )


def test_is_not_circular():
    # Define a directed acyclic graph (DAG)
    acyclic_graph = {
        "nodes": [
            {"id": "A", "data": {"category": []}},
            {"id": "B", "data": {"category": []}},
            {"id": "C", "data": {"category": []}},
            {"id": "D", "data": {"category": []}},
        ],
        "edges": [
            ("A", "B"),  # Edge from A to B
            ("B", "C"),  # Edge from B to C
            ("C", "D"),  # Edge from C to D
        ],
    }


