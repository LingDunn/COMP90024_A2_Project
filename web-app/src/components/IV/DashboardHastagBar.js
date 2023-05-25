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

import React from "react";
import axios from '../../my-axios';
import {
    Badge,
    Button,
    Card,
    Navbar,
    Nav,
    Table,
    Container,
    Row,
    Col,
} from "react-bootstrap";
import { useState, useEffect } from 'react'

export function DashboardHastagBar() {

    const [data, setData] = useState([{}])
    useEffect(() => {
        axios.get("/dashboard_hashtag").then(
            response => {
                //console.log("dashboard_hashtag", response.data)
                setData(response.data)
            }
        )
    }, [])

    const res = data
    if (!res) {
        console.log("Waiting...")
    } else {
        console.log("Received")
    }

    return (
        <Table className="table-hover table-striped">
            <thead>
                <tr>
                    <th className="border-0">#Hashtag</th>
                    <th className="border-0">Count</th>
                </tr>
            </thead>
            <tbody>
                {
                    res.map(item => {
                        return (
                            <tr key={item.hashtag}>
                                <td>{item.hashtag}</td>
                                <td>{item.cnt}</td>
                            </tr>
                        )
                    })
                }
            </tbody>
        </Table>
    )

}
