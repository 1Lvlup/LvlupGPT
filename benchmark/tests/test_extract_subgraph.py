import pytest

from agbenchmark.utils.dependencies.graphs import extract_subgraph_based_on_category

# Beginning of curriculum_graph fixture definition
@pytest.fixture
def curriculum_graph():
    # This fixture returns a dictionary representing a curriculum graph
    # with nodes and edges between them, categorized by subjects.
    return {
        "edges": [
            {"from": "Calculus", "to": "Advanced Calculus"},
            {"from": "Algebra", "to": "Calculus"},
            {"from": "Biology", "to": "Advanced Biology"},
            {"from": "World History", "to": "Modern History"},
        ],
        "nodes": [
            {"data": {"category": ["math"]}, "id": "Calculus", "label": "Calculus"},
            {
                "data": {"category": ["math"]},
                "id": "Advanced Calculus",
                "label": "Advanced Calculus",
            },
            {"data": {"category": ["math"]}, "id": "Algebra", "label": "Algebra"},
            {"data": {"category": ["science"]}, "id": "Biology", "label": "Biology"},
            {
                "data": {"category": ["science"]},
                "id": "Advanced Biology",
                "label": "Advanced Biology",
            },
            {
                "data": {"category": ["history"]},
                "id": "World History",
                "label": "World History",
            },
            {
                "data": {"category": ["history"]},
                "id": "Modern History",
                "label": "Modern History",
            },
        ],
    }

# Beginning of graph_example definition
graph_example = {
    "nodes": [
        {"id": "A", "data": {"category": []}},
        {"id": "B", "data": {"category": []}},
        {"id": "C", "data": {"category": ["math"]}},
    ],
    "edges": [{"from": "B", "to": "C"}, {"from": "A", "to": "C"}],
}
# graph_example is a sample graph with nodes and edges, with one node categorized as 'math'


def test_dfs_category_math(curriculum_graph):
    # This test function checks if the 'math' category nodes and edges are extracted correctly
    result_graph = extract_subgraph_based_on_category(curriculum_graph, "math")

    # Expected nodes: Algebra, Calculus, Advanced Calculus
    # Expected edges: Algebra->Calculus, Calculus->Advanced Calculus
    expected_nodes = ["Algebra", "Calculus", "Advanced Calculus"]
    expected_edges = [
        {"from": "Algebra", "to": "Calculus"},
        {"from": "Calculus", "to": "Advanced Calculus"},
    ]

    # Checking if the extracted nodes and edges match the expected ones
    assert set(node["id"] for node in result_graph["nodes"]) == set(expected_nodes)
    assert set((edge["from"], edge["to"]) for edge in result_graph["edges"]) == set(
        (edge["from"], edge["to"]) for edge in expected_edges
    )


def test_extract_subgraph_math_category():
    # This test function checks if the 'math' category nodes and edges are extracted correctly for the sample graph
    subgraph = extract_subgraph_based_on_category(graph_example, "math")

    # Checking if the extracted nodes and edges match the original sample graph nodes and edges
    assert set(
        (node["id"], tuple(node["data"]["category"])) for node in subgraph["nodes"]
    ) == set(
        (node["id"], tuple(node["data"]["category"])) for node in graph_example["nodes"]
    )
    assert set((edge["from"], edge["to"]) for edge in subgraph["edges"]) == set(
        (edge["from"], edge["to"]) for edge in graph_example["edges"]
    )


def test_extract_subgraph_non_existent_category():
    # This test function checks if an empty graph is returned when an non-existent category is provided
    result_graph = extract_subgraph_based_on_category(graph_example, "toto")

    # Asserting that the result graph has no nodes and no edges
    assert len(result_graph["nodes"]) == 0
    assert len(result_graph["edges"]) == 0
