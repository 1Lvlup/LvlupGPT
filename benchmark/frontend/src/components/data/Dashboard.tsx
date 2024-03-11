// Import necessary modules and dependencies
import React, { useState } from "react";
import tw, { TwStyle, CSSInterpolation } from "tailwind-styled-components";

// Import the child components that will be used in this Dashboard component
import RadarChart from "./dashboard/RadarChart";
import CategorySuccess from "./dashboard/CategorySuccess";
import CurrentEnv from "./dashboard/CurrentEnv";

// Define the props for the Dashboard component
interface DashboardProps {
  data: any; // The data to be passed to the Dashboard component
}

// Define the Dashboard functional component
const Dashboard: React.FC<DashboardProps> = ({ data }) => {
  // Return the JSX that represents the Dashboard component
  return (
    <DashboardContainer> {/* The container for the dashboard cards */}
      <CardWrapper> {/* The first card wrapper */}
        <RadarChart /> {/* The RadarChart component */}
      </CardWrapper>
      <CardWrapper> {/* The second card wrapper */}
        <CategorySuccess /> {/* The CategorySuccess component */}
      </CardWrapper>
      <CardWrapper> {/* The third card wrapper */}
        <CurrentEnv /> {/* The CurrentEnv component */}
      </CardWrapper>
    </DashboardContainer>
  );
};

// Export the Dashboard component
export default Dashboard;

// Define the props for the CardWrapper component
interface CardWrapperProps {
  css?: CSSInterpolation; // Additional Tailwind CSS styles
}

// Define the styled DashboardContainer component
const DashboardContainer = tw.div`
  w-full
  h-screen
  flex
  flex-wrap
  justify-center
  items-center
` as TwStyle<CardWrapperProps>;

// Define the props for the CardWrapperStyle component
interface CardWrapperStyleProps {
  width?: string; // Optional width for the card wrapper
  height?: string; // Optional height for the card wrapper
}

// Define the styled CardWrapper component
const CardWrapperStyle: TwStyle<CardWrapperStyleProps> = {
  width: "w-96", // Default width
