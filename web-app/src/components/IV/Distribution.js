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

import { useState, useEffect } from 'react'
import React from 'react';
import {
    Badge,
    Button,
    Card,
    Form,
    Navbar,
    Nav,
    Container,
    Row,
    Col
  } from "react-bootstrap";
import { Bar, Chart } from "test-react-chartjs-2";
import * as zoom from "chartjs-plugin-zoom";

export function Distribution(props){

    const topic_name = {
      "scotty": "Scotty Morrison",
      "uk": "Ukraine",
      "ukraine": "Ukraine",
      "cc": "Cryptocurrency",
      "nft": "NFT",
      "porn": "Adult Film"
    }

    // Declare var
    let show = <h4>The Distribution is not available for this Location</h4>
    let d = props.data
    let numBins = 10;
    let minValue = 0;
    let maxValue = 0;
    let binWidth = 0;
    let frequencies = 0;
    let binLabels;
    let label_txt;
    let title_txt;
    let foot_txt = props.sub;
    
    // helpers
    function form_title(dist){
      if (props.loc == "australia"){
        title_txt = dist + " Across Australia"
      }
      if (props.loc == "new south wales"){
        title_txt = dist + " Across New South Wales"
      }
      if (props.loc == "victoria"){
        title_txt = dist + " Across Victoria"
      }
      if (props.loc == "queensland"){
        title_txt = dist + " Across Queensland"
      }
      if (props.loc == "south australia"){
        title_txt = dist + " Across South Australia"
      }
      if (props.loc == "western australia"){
        title_txt = dist + " Across Western Australia"
      }
      if (props.loc == "tasmania"){
        title_txt = dist + " Across Tasmania"
      }
      if (props.loc == "northern territory"){
        title_txt = dist + " Across Northern Territory"
      }
      if (props.loc == "australian capital territory"){
        title_txt = dist + " Across Australian Capital Territory"
      }
    }

    if (props.dist == "med"){
      label_txt = "Median incomes of individual aged 25-65 (2011 dollars)"
      form_title("Distribution of Median Incomes")
    }
    if (props.dist == "emp"){
      label_txt = "Total number of inidividuals employed as a proportion to the total population";
      form_title("Distribution of Employment Rates")
    }
    if (props.dist == "lf"){
      label_txt = "Participation rate (labour force as a proportion to the population)"
      form_title("Distribution of Participation Rates")
    }
    if (props.dist == "uni"){
      label_txt = "Proportion of popluation with a bachelor degree or higher"
      form_title("Distribution of Proportions of Population with a Bachelor Degree or Higher")
    }
    if (props.dist == "tafe"){
      label_txt = "Proportion of popluation with TAFE qualification. E.g. Cert 3/4, diploma"
      form_title("Distribution of Proportions of Population with TAFE Qualification")
    }
    if (props.dist == "y12"){
      label_txt = "Proportion of popluation with no post-school qualifications"
      form_title("Distribution of Proportions of Population with No Post-school Qualifications")
    }
    
    // Prepare data
    if (d !== undefined){
      numBins = 10;
      minValue = Math.min(...d.map((value) => parseFloat(value)));
      maxValue = Math.max(...d.map((value) => parseFloat(value)));
      binWidth = (maxValue - minValue) / numBins;
      frequencies = Array(numBins).fill(0);

      d.forEach((value) => {
        const binIndex = Math.floor((parseFloat(value) - minValue) / binWidth);
        frequencies[binIndex]++;
      });
  
      binLabels = Array.from({ length: numBins }, (_, index) => {
        const binStart = minValue + index * binWidth;
        const binEnd = binStart + binWidth;
        return binStart;
      });
      frequencies.pop()
    }

    const [value, setValue] = useState(0);
    useEffect(() => {
        Chart.register(zoom);
    }, []);

    // Construct Option Data
    const options = {
      pan: {
        enabled: true,
        mode: "xy"
      },
      zoom: {
        enabled: true,
        drag: false,
        mode: "xy"
      },
      scales: {
        x: {
          type: "linear",
          offset: false,
          gridLines: {
            offsetGridLines: false
          },
          title: {
            display: true,
            text: label_txt
          },
        }
      },
      plugins: {
        beforeInit: function (chart, args, options) {
          console.log("called");
        },
        afterDatasetDraw: () => {
          console.log("called");
        },
        legend: {
          text: "Frequency",
          display: false,
        }
      }
    };

    // Construct return 
    if (d==undefined){
      show = <h4>The Distribution is not available for this Location</h4>
    }else{
      show = <Bar 
        data={{
        labels:binLabels,
        datasets: [
          {
            borderColor: "blac",
            lineTension: 0,
            fill: false,
            borderJoinStyle: "round",
            data: frequencies,
            borderWidth: 0.2,
            barPercentage: 1,
            categoryPercentage: 1,
            hoverBackgroundColor: "darkgray",
            barThickness: "flex"
          }
        ]
        }}
        options={options}
        plugins={[
          {
            afterDatasetDraw: () => {
              console.log("called");
            }
          }
        ]}></Bar>
    }

    // Return IV
    return (
        <>
          <Card.Header>
            <Card.Title as="h4">{title_txt}</Card.Title>
            <p className="card-category">The data are retrived from suburbs where have 
                tweets related to the topic "{topic_name[props.topic]}".</p>
          </Card.Header>
          <Card.Title></Card.Title>
          <Card.Body>
            {show}
          </Card.Body>
          <hr />
          <Card.Footer>
            <p className="card-category">The suburbs/states taken into consideration are {foot_txt}</p>
          </Card.Footer>
        </>
    )
    
}