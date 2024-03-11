# Import the get_roots function from the dependencies.graphs module in agbenchmark.utils package.
from agbenchmark.utils.dependencies.graphs import get_roots


def test_get_roots():
    # Define a sample directed graph as a dictionary with nodes and edges.
    # Each node is represented as a dictionary with an 'id' and 'data' field.
    # The 'data' field is currently empty, but it can be used to store additional information about the node.
    graph = {
        "nodes": [
            {"id": "A", "data": {"category": []}},
            {"id": "B", "data": {"category": []}},
            {"id": "C", "data": {"category": []}},
            {"id": "D", "data": {"category": []}},
        ],
        "edges": [
            {"from": "A", "to": "B"},  # Directed edge from node 'A' to node 'B'
            {"from": "B", "to": "C"},  # Directed edge from node 'B' to node 'C'
        ],
    }

    # Call the get_roots function with the sample graph as an argument.
    result = get_roots(graph)

    # Assert that the result is a set containing 'A' and 'D', which are the root nodes of the graph.
    assert set(result) == {
        "A",
        "D",
    }, f"Expected roots to be 'A' and 'D', but got {result}"


def test_no_roots():
    # Define a fully connected directed graph as a dictionary with nodes and edges.
    fully_connected_graph = {
        "nodes": [
            {"id": "A", "data": {"category": []}},
            {"id": "B", "data": {"category": []}},
            {"id": "C", "data": {"category": []}},
        ],
        "edges": [
            {"from": "A", "to": "B"},  # Directed edge from node 'A' to node 'B'
            {"from": "B", "to": "C"},  # Directed edge from node 'B' to node 'C'
            {"from": "C", "to": "A"},  # Directed edge from node 'C' to node 'A'
        ],
    }

    # Call the get_roots function with the fully connected graph as an argument.
    result = get_roots(fully_connected_graph)

    # Assert that the result is an empty set, indicating that there are no root nodes in the graph.
    assert not result, "Expected no
