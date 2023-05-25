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

export function CcTwtPie() {

    const [data, setData] = useState([{}])
    useEffect(() => {
        axios.get("/cc_twt_pie").then(
            response => {
                setData(response.data)
            }
        )
    }, [])

    const res = {}
    res["counts"] = data.counts
    if (!res["counts"]) {
        console.log("Waiting...")
    } else {
        console.log("Received")
    }

    // Construct VI data
    const labels = ["Current Topic Count", "Other Topics Count"]
    const d = res.counts
    const PieData = {
        labels: labels,
        datasets: [
            {
                label: '#Tweets',
                data: d,
                backgroundColor: [
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                ],
                borderWidth: 1,
            },
        ],
    }

    return <Pie data={PieData} />;

}