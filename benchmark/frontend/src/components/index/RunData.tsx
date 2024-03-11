import React, { useState } from "react";
import { LatestRun } from "../../lib/types";
import tw from "tailwind-styled-components";

type RecursiveDropdownProps = {
  // The data to be rendered in the recursive dropdown
  data: any;
  // An array of keys to skip rendering
  skipKeys: string[];
};

const isObject = (value: any): value is object =>
  value !== null && typeof value === "object";

const RecursiveDropdown: React.FC<RecursiveDropdownProps> = ({
  data, // eslint-disable-line react/prop-types
  skipKeys,
}) => {
  // Return null if data is null or not an object
  if (data === null || typeof data !== "object") {
    return null;
  }

  return (
    <>
      {Object.entries(data).map(([key, value]) => {
        // Skip rendering keys specified in skipKeys array
        if (skipKeys.includes(key)) {
          return null;
        }

        // Return null if array is empty
        if (Array.isArray(value) && value.length === 0) {
          return null;
        }

        // Render a dropdown for objects
        if (isObject(value)) {
          return (
            <Dropdown key={key}>
              <DropdownSummary aria-label={`Expand ${key}`}>
                {key}
                <DropdownArrow />
              </DropdownSummary>
              <DropdownContent>
                <RecursiveDropdown data={value} skipKeys={skipKeys} />
              </DropdownContent>
            </Dropdown>
          );
        }

        // Render a section for non-object values
        return (
          <Section key={key}>
            <Label>{key}:</Label>
            <Data>
              {typeof value === "string" ? value : JSON.stringify(value)}
            </Data>
          </Section>
        );
      })}
    </>
  );
};

type RunDataProps = {
  latestRun: LatestRun;
};

const RunData: React.FC<RunDataProps> = ({ latestRun }) => {
  // Convert benchmark_start_time to a Date object
  const date = new Date(latestRun.benchmark_start_time);

  return (
    <Card>
      <Section>
        <Label>Command:</Label>
        <Data>{latestRun.command}</Data>
      </Section>
      <Section>
        <Label>Start time:</Label>
        <Data>{date.toLocaleString()}</Data>
      </Section>
      <Section>
        <Label>Run time:</Label>
        <Data>{latestRun.metrics.run_time}</Data>
      </Section>
      <Section>
        <Label>Highest difficulty:</Label>
        <Data>
          {latestRun.metrics.highest_difficulty.split(":")[1]?.slice(-1)}
        </Data>
      </Section>

      {/* Render a dropdown for each test in latestRun.tests */}
      {Object.keys(latestRun.tests).map((testKey) => (
        <Dropdown key={testKey}>
          <DropdownSummary aria-label={`Expand ${testKey}`}>
            {testKey}
            <DropdownArrow />
          </DropdownSummary>
          <DropdownContent>
            {latestRun.tests[testKey] && (
              <RecursiveDropdown
                data={latestRun.tests[testKey]}
                skipKeys={["cost", "data_path"]}
              />
            )}
          </DropdownContent>
        </Dropdown>
      ))}
    </Card>
  );
};

// Define styled components for the card and its sections
const Card = tw.div`
  bg-white
  p-4
  rounded
  shadow-lg
  w-full
  mt-4
`;

const Section = tw.div`
  mt-2
`;

const Label = tw.span`
  font-medium
`;

const Data = tw.span`
  ml-1
`;

// Define styled components for the dropdown and its parts
const Dropdown = tw.details`
  mt-4
`;

const DropdownSummary = tw.summary`
  cursor-pointer
  text-blue-500
`;

const DropdownArrow = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
    stroke="currentColor"
    className="inline-block w-4 h-4 ml-2 transform -rotate-90"
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M19 9l-7 7-7-7"
    />
  </svg>
);

