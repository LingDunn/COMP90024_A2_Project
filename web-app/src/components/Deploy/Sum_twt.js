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

import React from 'react'
import { useState, useEffect } from 'react'
import axios from '../../my-axios';

export const Sum_twt = () => {

    const [data, setData] = useState([{}])

    useEffect(() => {
        axios.get("/sum_twt").then(
            response => {
                setData(response.data)
            }
        )
    }, [])

    return (data.sum_twt)

}