import React, { useState } from "react";
import tw, { TwStyle, CSSInterpolation } from "tailwind-styled-components";

import RadarChart from "./dashboard/RadarChart";
import CategorySuccess from "./dashboard/CategorySuccess";
import CurrentEnv from "./dashboard/CurrentEnv";

interface DashboardProps {
  data: any;
}

const Dashboard: React.FC<DashboardProps> = ({ data }) => {
  return (
    <DashboardContainer>
      <CardWrapper>
        <RadarChart />
      </CardWrapper>
      <CardWrapper>
        <CategorySuccess />
      </CardWrapper>
      <CardWrapper>
        <CurrentEnv />
      </CardWrapper>
    </DashboardContainer>
  );
};

export default Dashboard;

interface CardWrapperProps {
  css?: CSSInterpolation;
}

const DashboardContainer = tw.div`
  w-full
  h-screen
  flex
  flex-wrap
  justify-center
  items-center
` as TwStyle<CardWrapperProps>;

interface CardWrapperStyleProps {
  width?: string;
  height?: string;
}

const CardWrapperStyle: TwStyle<CardWrapperStyleProps> = {
  width: "w-96",
  height: "h-64",
  rounded: "rounded-xl",
  shadow: "shadow-lg",
  border: "border",
  padding: "p-4",
};

const CardWrapper = tw.div<CardWrapperStyleProps>(CardWrapperStyle)``;
