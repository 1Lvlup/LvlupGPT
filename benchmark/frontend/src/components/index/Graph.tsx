// Import necessary libraries and components
import React, { useEffect, useRef, useState } from "react";
import { Network, DataSet } from "vis-network/standalone";
import tw from "tailwind-styled-components";

// Import custom types
import { GraphNode, TaskData } from "../../lib/types";

// Define the shape of GraphEdge interface
interface GraphEdge {
  id: string;
  from: string;
  to: string;
  arrows: string;
}

// Define the shape of GraphProps interface
interface GraphProps {
  graphData: {
    nodes: GraphNode[];
    edges: GraphEdge[];
  };
  setSelectedTask: React.Dispatch<React.SetStateAction<TaskData | null>>;
  setIsTaskInfoExpanded: React.Dispatch<React.SetStateAction<boolean>>;
}

// Style the GraphContainer component
const GraphContainer = tw.div`
  w-full
  h-full
`;

// Implement the Graph component
const Graph: React.FC<GraphProps> = ({
  graphData, // Accept graphData as a prop
  setSelectedTask, // Accept setSelectedTask as a prop
  setIsTaskInfoExpanded, // Accept setIsTaskInfoExpanded as a prop
}) => {
  const graphRef = useRef<HTMLDivElement>(null); // Create a ref for the graph container

  // Clean up the network when the component unmounts
  useEffect(() => {
    return () => {
      if (networkInstance) {
        networkInstance.destroy();
      }
    };
  }, []);

  // Initialize the network when the component mounts and graphData changes
  useEffect(() => {
    if (!graphRef.current) {
      return;
    }

    // Create DataSet instances for nodes and edges
    const nodes = new DataSet<GraphNode>(graphData.nodes);
    const edges = new DataSet<GraphEdge>(graphData.edges);

    // Initialize the network with nodes, edges, and options
    const networkInstance = new Network(graphRef.current, { nodes, edges }, {
      nodes: {
        font: {
          size: 20,
          color: "black",
        },
        shapeProperties: {
          useBorderWithImage: true,
        },
      },
      edges: {
        length: 250,
      },
      layout: {
        hierarchical: {
          // Configure the hierarchical layout
        },
      },
      physics: {
        stabilization: {
          // Configure the stabilization physics
        },
        hierarchicalRepulsion: {
          // Configure the hierarchical repulsion physics
        },
        timestep: 0.5,
      },
    });

    // Add event listener for node clicks
    networkInstance.on("click", (params) => {
      if (params.nodes.length) {
        // Handle node click
      } else {
        // Handle no node click
      }
    });

    // Update networkInstance in the effect dependency array
    return () => {
      networkInstance.destroy();
    };
  }, [graphData, setSelectedTask, setIsTaskInfoExpanded]); // Add graphData and callbacks to the dependency array

  return <GraphContainer ref={graphRef} />; // Render the GraphContainer component
};

export default Graph; // Export the Graph component
