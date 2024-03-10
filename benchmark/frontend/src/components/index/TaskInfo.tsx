import React, { useState } from "react";
import tw from "tailwind-styled-components";
import { TaskData } from "../../lib/types";
import RunData from "./RunData";
import SelectedTask from "./SelectedTask";
import MockCheckbox from "./MockCheckbox";
import RunButton from "./RunButton";

interface TaskInfoProps<T extends TaskData> {
  selectedTask: T | null;
  isTaskInfoExpanded: boolean;
  setIsTaskInfoExpanded: React.Dispatch<React.SetStateAction<boolean>>;
  setSelectedTask: React.Dispatch<React.SetStateAction<T | null>>;
  isAllRunsVisible: boolean;
  setIsAllRunsVisible: React.Dispatch<React.SetStateAction<boolean>>;
  isPreviousRunVisible: boolean;
  setIsPreviousRunVisible: React.Dispatch<React.SetStateAction<boolean>>;
}

const TaskInfo: React.FC<TaskInfoProps<TaskData>> = ({
  selectedTask,
  isTaskInfoExpanded,
  setIsTaskInfoExpanded,
  setSelectedTask,
  isAllRunsVisible,
  setIsAllRunsVisible,
  isPreviousRunVisible,
  setIsPreviousRunVisible,
}) => {
  const [isMock, setIsMock] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [allResponseData, setAllResponseData] = useState<any[]>([]);
  const [responseData, setResponseData] = useState<any>();
  const [cutoff, setCutoff] = useState<number | null>(null);

  const handleCustomCutoffChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const value = event.target.value ? parseInt(event.target.value, 10) : null;
    if (!isNaN(value)) {
      setCutoff(value);
    }
  };

  const runBenchmark = async () => {
    setIsLoading(true);
    try {
      let url = `http://localhost:8000/run?mock=${isMock}`;
      cutoff !== null && !isMock && (url += `&cutoff=${cutoff}`);
      const response = await fetch(url);
      const data = await response.json();

      if (data["returncode"] > 0) {
        throw new Error(data["stderr"]);
      } else {
        const jsonObject = JSON.parse(data["stdout"]);
        setAllResponseData((prevData) => [...prevData, jsonObject]);
        setResponseData(jsonObject);
      }
    } catch (error) {
      console.error("There was an error fetching the data", error);
    }
    setIsLoading(false);
  };

  return (
    <TaskDetails isExpanded={isTaskInfoExpanded}>
      {isTaskInfoExpanded ? (
        <ToggleButton
          onClick={() => {
            setIsTaskInfoExpanded(!isTaskInfoExpanded);
            setSelectedTask(null);
          }}
          aria-label="Toggle task info"
        >
          →
        </ToggleButton>
      ) : (
        <BenchmarkWrapper>
          <RunButton
            cutoff={selectedTask?.cutoff}
            isLoading={isLoading}
            testRun={runBenchmark}
            isMock={isMock}
            data-testid="run-button"
          />
          <MockCheckbox
            isMock={isMock}
            setIsMock={setIsMock}
            title="Mock mode"
            description="Run the benchmark in mock mode"
            isCustomCutoff={cutoff !== null}
            onCustomCutoffChange={handleCustomCutoffChange}
          />
          <Detail>
            <b>or click a node on the left</b>
          </Detail>
        </BenchmarkWrapper>
      )}

      {selectedTask && (
        <SelectedTask
          selectedTask={selectedTask}
          isMock={isMock}
          setIsMock={setIsMock}
          cutoff={cutoff}
          setResponseData={setResponseData}
          allResponseData={allResponseData}
          setAllResponseData={setAllResponseData}
        />
      )}
      {!isMock && (
        <CheckboxWrapper>
          <p>Custom cutoff</p>
          <CutoffInput
            type="number"
            placeholder="Leave blank for default"
            value={cutoff ?? ""}
            onChange={handleCustomCutoffChange}
            min={0}
            max={10000}
            defaultValue={0}
          />
        </CheckboxWrapper>

