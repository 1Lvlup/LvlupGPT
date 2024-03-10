import { useEffect, useState } from "react";
import Head from "next/head";
import tw from "tailwind-styled-components";

import Graph from "../components/index/Graph";
import TaskInfo from "../components/index/TaskInfo";
import { TaskData } from "../lib/types";

const Home = () => {
  const [data, setData] = useState<TaskData[] | null>(null);
  const [selectedTask, setSelectedTask] = useState<TaskData | null>(null);
  const [isTaskInfoExpanded, setIsTaskInfoExpanded] = useState(false);

  useEffect(() => {
    // Load the JSON data from the public folder
    const fetchData = async () => {
      try {
        const response = await fetch("/graph.json");
        const data = await response.json();
        setData(data);
      } catch (error) {
        console.error("Error fetching the graph data:", error);
      }
    };

    fetchData();
  }, []);

  if (!data) {
    return <div>Loading...</div>;
  }

  return (
    <>
      <Head>
        <title>agbenchmark</title>
        <meta name="description" content="The best way to evaluate your agents" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className="flex h-screen flex-col items-center justify-center">
        <Panels>
          <Graph
            graphData={data}
            setSelectedTask={setSelectedTask}
            setIsTaskInfoExpanded={setIsTaskInfoExpanded}
          />
          <TaskInfo
            selectedTask={selectedTask}
            isTaskInfoExpanded={isTaskInfoExpanded}
            setIsTaskInfoExpanded={setIsTaskInfoExpanded}
            setSelectedTask={setSelectedTask}
          />
        </Panels>
      </main>
    </>
  );
};

export default Home;

const Panels = tw.div`
  flex
  h-full
  w-full
`;
