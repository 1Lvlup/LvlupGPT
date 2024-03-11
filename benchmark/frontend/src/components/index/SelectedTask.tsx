import React, { useState, useCallback } from "react";
import tw from "tailwind-styled-components";
import { TaskData } from "../../lib/types";
import RunButton from "./RunButton";
import MockCheckbox from "./MockCheckbox";

type SelectedTaskProps = {
  selectedTask: TaskData | null;
  isMock: boolean;
  setIsMock: React.Dispatch<React.SetStateAction<boolean>>;
  cutoff: number | null;
  setResponseData: React.Dispatch<React.SetStateAction<any>>;
  allResponseData: any[];
  setAllResponseData: React.Dispatch<React.SetStateAction<any[]>>;
};

// SelectedTask component receives several props related to the currently selected task,
// including the task data, whether to use mock mode, the cutoff value, and functions to
// manage the response data.
const SelectedTask: React.FC<SelectedTaskProps> = ({
  selectedTask,
  isMock,
  setIsMock,
  cutoff,
  setResponseData,
  allResponseData,
  setAllResponseData,
}) => {
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // runTest function is a callback that handles running the selected task with the given
  // parameters, updating the response data and managing the loading state.
  const runTest = useCallback(async () => {
    if (!selectedTask) return; // If there's no selected task, simply return.

    const testParam = selectedTask.name;
    setIsLoading(true); // Set loading state to true before making the API call.
    try {
      let url = `http://localhost:8000/run_single_test?test=${testParam}&mock=${isMock}`;
      if (cutoff !== null && !isMock) {
        url += `&cutoff=${cutoff}`; // If a cutoff value is provided and not in mock mode, append it to the URL.
      }
      const response = await fetch(url); // Make the API call.
      const data = await response.json();

      if (data.returncode > 0) {
        throw new Error(data.stderr); // If the return code is greater than 0, throw an error.
      } else {
        const jsonObject = JSON.parse(data.stdout); // Otherwise, parse the JSON data from the response.
        setAllResponseData((prevData) => [...prevData, jsonObject]); // Add the parsed JSON object to the allResponseData array.
        setResponseData(jsonObject); // Update the response data.
      }
    } catch (error) {
      console.error("There was an error fetching the data", error); // Log any errors that occur during the process.
    }
    setIsLoading(false); // Set loading state to false after the API call is complete.
  }, [selectedTask, isMock, cutoff]); // The runTest function depends on the selectedTask, isMock, and cutoff.

  return (
    <>
      {/* Render the task name, prompt, and details. */}
      <TaskName>{selectedTask?.name}</TaskName>
      <TaskPrompt>{selectedTask?.task}</TaskPrompt>
      <Detail>
        <b>Cutoff:</b> {selectedTask?.cutoff}
      </Detail>
      <Detail>
        <b>Description:</b> {selectedTask?.info?.description}
      </Detail>
      <Detail>
        <b>Difficulty:</b> {selectedTask?.info?.difficulty}
      </Detail>
      <Detail>
        <b>Category:</b> {selectedTask?.category.join(", ")}
      </Detail>
      {/* Render the RunButton and MockCheckbox components. */}
      <RunButton
        cutoff={selectedTask?.cutoff}
        isLoading={isLoading}
        testRun={runTest}
        isMock={isMock}
        disabled={isLoading}
      />
      <MockCheckboxInput
        type="checkbox"
        checked={isMock}
        onChange={(event) => {
          event.preventDefault();
          setIsMock(event.target.checked);
        }}
      />
      <CheckboxWrapper htmlFor="mock-checkbox">
        Mock
      </CheckboxWrapper>
    </>
  );
};

// Styled components for the SelectedTask component.
const TaskName = tw.h1`
    font-bold
    text-2xl
    break-words
`;

const TaskPrompt = tw.p`
    text-gray-900
    break-words
`;
const Detail = tw.
