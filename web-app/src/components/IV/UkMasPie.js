import React from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie } from 'react-chartjs-2';
import { useState, useEffect } from 'react'
import axios from '../../my-axios';
ChartJS.register(ArcElement, Tooltip, Legend);

export function UkMasPie() {

    const [data, setData] = useState([{}])
    useEffect(() => {
        axios.get("/uk_mas_pie").then(
            response => {
                setData(response.data)
                console.log(response.data)
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
                label: '#Posts',
                data: d,
                backgroundColor: [
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                ],
                borderColor: [
                    'rgba(153, 102, 255, 0.5)',
                    'rgba(255, 206, 86, 1)',
                ],
                borderWidth: 1,
            },
        ],
    }

    return <Pie data={PieData} />;

}