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
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie } from 'react-chartjs-2';
ChartJS.register(ArcElement, Tooltip, Legend);
import { useState, useEffect } from 'react'
import axios from '../../my-axios';

export function DashboardLanTwt() {

  // Top 8 and others
  const [data, setData] = useState([{}])
  useEffect(() => {
    axios.get("/dashboard_lang_twt").then(
      response => {
        setData(response.data)
      }
    )
  }, [])

  const res = {}
  res["lang"] = data.lang
  res["value"] = data.value
  if (!res["data"]) {
    console.log("Waiting...")
  } else {
    console.log("Received")
  }

  // Construct IV data
  const LangData = {
    labels: res["lang"],
    datasets: [
      {
        label: '# Tweets',
        data: res["value"],
        backgroundColor: [
          'rgba(255, 99, 132, 0.2)',
          'rgba(54, 162, 235, 0.2)',
          'rgba(255, 206, 86, 0.2)',
          'rgba(75, 192, 192, 0.2)',
          'rgba(153, 102, 255, 0.2)',
          'rgba(255, 159, 64, 0.2)',
          'rgba(255, 255, 132, 0.2)',
          'rgba(255, 99, 255, 0.2)',
          'rgba(88, 77, 77, 0.2)',
          'rgba(188, 99, 132, 0.2)',
          'rgba(255, 99, 7, 0.2)',
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
          'rgba(255, 159, 64, 1)',
          'rgba(255, 255, 132, 1)',
          'rgba(255, 99, 255, 1)',
          'rgba(88, 77, 77, 1)',
          'rgba(188, 99, 132, 1)',
          'rgba(255, 99, 7, 1)',

        ],
        borderWidth: 1,
      },
    ]
  };

  return <Pie data={LangData} />;

}