import React from "react";
import { Radar } from "react-chartjs-2";
import tw from "tailwind-styled-components";

interface RadarChartProps {
  data: {
    labels: string[];
    datasets: {
      label: string;
      data: number[];
      backgroundColor: string;
      borderColor: string;
    }[];
  };
}

const RadarChart: React.FC<RadarChartProps> = ({ data }) => {
  return <RadarChartContainer><Radar data={data} /></RadarChartContainer>;
};

const RadarChartContainer = tw.div`
  w-full
  h-full
`;

export default RadarChart;
