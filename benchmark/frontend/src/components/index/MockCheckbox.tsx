import React from "react";

// Importing Tailwind CSS styled-components and tw utility function
import tw, { css } from "tailwind-styled-components";

// Interface for MockCheckbox component props
interface MockCheckboxProps {
  isMock: boolean; // Flag to indicate if the test is a mock test
  setIsMock: React.Dispatch<React.SetStateAction<boolean>>; // Function to update the isMock state
}

// Styled input component for the mock checkbox
const MockCheckboxInput = tw.input`
  border rounded // Applies border and rounded corners
  focus:border-blue-400 focus:ring focus:ring-blue-2
