import React from "react";

import tw, { css } from "tailwind-styled-components";

interface MockCheckboxProps {
  isMock: boolean;
  setIsMock: React.Dispatch<React.SetStateAction<boolean>>;
}

const MockCheckboxInput = tw.input`
  border rounded
  focus:border-blue-400 focus:ring focus:ring-blue-200 focus:ring-opacity-50
  ${(props: any) =>
    props.checked &&
    css`
      border-blue-400 bg-blue-100
    `}
`;

const CheckboxWrapper = tw.label`
  flex items-center space-x-2 mt-2
  cursor-pointer
`;

const MockCheckbox: React.FC<MockCheckboxProps> = ({ isMock, setIsMock }) => {
  return (
    <CheckboxWrapper htmlFor="mock-checkbox">
      <MockCheckboxInput
        id="mock-checkbox"
        type="checkbox"
        checked={isMock}
        onChange={() => setIsMock(!isMock)}
        required
      />
      <span>Run mock test</span>
    </CheckboxWrapper>
  );
};

export default MockCheckbox;
