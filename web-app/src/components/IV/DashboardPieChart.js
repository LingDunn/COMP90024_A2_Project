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
import { useState, useEffect } from 'react'
import axios from '../../my-axios';
ChartJS.register(ArcElement, Tooltip, Legend);

export function PieChart() {

    const [data, setData] = useState([{}])
    useEffect(() => {
        axios.get("/dashboard_sudo_pie").then(
            response => {
                setData(response.data)
            }
        )
    }, [])

    const res = {}
    res["labels"] = data.states
    res["suburbs"] = data.suburbs
    res["data"] = []
    if (!res["labels"] && !res["suburbs"]) {
        console.log("Waiting...")
    } else {
        console.log("Received")
        res["labels"].forEach((label) => {
            res["data"].push(res["suburbs"][label].length)
        });
    }

    // Construct IV data
    const labels = res.labels
    const d = res.data
    const PieData = {
        labels: labels,
        datasets: [
            {
                label: '#Suburbs',
                data: d,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(200, 23, 198, 0.2)',
                    'rgba(11, 11, 11, 0.2)',
                    'rgba(211, 211, 211, 0.2)',
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(200, 23, 198, 1)',
                    'rgba(11, 11, 11, 1)',
                    'rgba(211, 211, 211, 1)',
                ],
                borderWidth: 1,
            },
        ],
    }

    return <Pie data={PieData} />;

}