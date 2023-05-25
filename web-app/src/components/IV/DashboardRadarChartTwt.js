///////////////////////////////////////////
//   COMP90024 2023-S1 A2 Team 52        //
//   City: Melbourne                     //
//   Team members:                       //
//       Ganbayar Sukhbaatar - 1227274   //
//       ZHIQUAN LAI - 1118797           //
//       Mingyang Liu - 1113531          //
//       Jiahao Chen - 1118749           //
//       Lingling Yao - 1204405          //
///////////////////////////////////////////

import React from 'react';
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js';
import { Radar } from 'react-chartjs-2';
ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);
import { useState, useEffect } from 'react'
import axios from '../../my-axios';


export function RadarChartTwt() {

  const [data, setData] = useState([{}])
  useEffect(() => {
    axios.get("/dashboard_topic_twt").then(
      response => {
        setData(response.data)
      }
    )
  }, [])

  // Wait for backend API to load data
  const res = {}
  res["data"] = data.counts
  if (!res["data"]) {
    console.log("Waiting...")
  } else {
    console.log("Received")
  }

  // Construct IV data
  const RadarData = {
    labels: ['Morrison', 'Ukraine', 'Cryptocurrency', 'NTF', 'Adult Film'],
    datasets: [
      {
        label: '# of Tweets',
        data: res.data,
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgba(54, 162, 235, 0.5)',
        borderWidth: 1,
      },
    ],
  };

  // return visual
  return <Radar data={RadarData} />;

}
