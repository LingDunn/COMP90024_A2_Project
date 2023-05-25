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
import ChartistGraph from "react-chartist";
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
  Form,
  OverlayTrigger,
  Tooltip,
} from "react-bootstrap"; 
/* MY OWN IMPORT */
import { BsTwitter } from "react-icons/bs";
import { BsMastodon } from "react-icons/bs";
import { BsClipboard2Data } from "react-icons/bs";
import {useState, useEffect } from 'react'
import { Sum_mas } from "components/Deploy/Sum_mas";
import { Sum_twt } from "components/Deploy/Sum_twt";
import { Sum_sudo } from "components/Deploy/Sum_sudo";
import { RadarChartTwt } from "components/IV/DashboardRadarChartTwt";
import { RadarChartMas } from "components/IV/DashboardRadarChartMas";
import { PieChart } from "components/IV/DashboardPieChart";
import { DashboardLanTwt } from "components/IV/DashboardLanTwt";
import { DashboardLanMas } from "components/IV/DashboardLanMas";
import { DashboardHastagBar } from "components/IV/DashboardHastagBar";

function Dashboard() {

  /* return home page content */
  return (
    /* JSX needs a parent tag to return multi elements */
    <>
      <Container fluid>

        {/* Row 0: GENERAL INFO DESCRIPTION */}
        <Row>
          <Col lg="12" sm="12">
            <Card className="card-stats">
              <Card.Body>
                This is a web application providing information 
                visulation on data from Mastodon, Twitter, and SUDO.
                <br></br>
                There are Five Topics Selected: Scott Morrison, Ukraine,
                Cryptocurrency, NFT and Adult Film.
              </Card.Body>
              <Card.Footer></Card.Footer>
            </Card>
          </Col>
        </Row>

        {/* ROW 1: GENERATE DATA INFO: COUNTS */}
        <Row>

          {/* CARD 2: Twitter DATA COUNT*/}
          <Col lg="4" sm="6">
            <Card className="card-stats">
              <Card.Body>
                <Row>
                  <Col xs="5">
                    <div className="icon-big text-center icon-warning text-info">
                      {/*<i className="fa fa-twitter-o"></i>*/}
                      <BsTwitter />
                    </div>
                  </Col>
                  <Col xs="7">
                    <div className="numbers">
                      <p className="card-category">Number of Twitter Tweets</p>
                      {/* NEED TO BE READ FROM COUCHDB*/}
                      
                      {(typeof <Sum_twt /> == 'undefined' || <Sum_twt /> == null) ? (
                        <Card.Title as="h4" className="text-info"><strong>Loading...</strong></Card.Title>
                      ) : (
                        <Card.Title as="h4" className="text-info"><strong><Sum_twt /></strong></Card.Title>
                      )}
                      
                    </div>
                  </Col>
                </Row>
              </Card.Body>
              <Card.Footer>
                <hr></hr>
                <div className="stats">
                {/* NEED TO BE READ FROM COUCHDB*/}
                  <i className="far fa-calendar-alt mr-1"></i>
                  Time Range: 2021 - 2022
                </div>
              </Card.Footer>
            </Card>
          </Col>

          {/* CARD 1: Mastodon DATA COUNT*/}
          <Col lg="4" sm="6">
            <Card className="card-stats">
              <Card.Body>
                <Row>
                  <Col xs="5">
                    <div className="icon-big text-center icon-warning">
                      {/* <i className="nc-icon nc-chart text-warning"></i> */}
                      <BsMastodon style={{ color: 'purple' }} />
                    </div>
                  </Col>
                  <Col xs="7">
                    <div className="numbers">
                      <p className="card-category">Number of Mastodon Posts</p>
                      {/* NEED TO BE READ FROM COUCHDB */}
                      {(typeof <Sum_mas /> == 'undefined' || <Sum_mas /> == null) ? (
                        <Card.Title as="h4" style={{ color: 'purple' }}>Loading...</Card.Title>
                      ) : (
                        <Card.Title as="h4" style={{ color: 'purple' }}><Sum_mas /></Card.Title>
                      )}
                      
                    </div>
                  </Col>
                </Row>
              </Card.Body>
              
              {/* CARD FOOTER - TIME RANGE */}
              <Card.Footer>
                <hr></hr>
                <div className="stats">
                  <i className="nc-icon nc-tv-2"></i>
                  &nbsp;&nbsp;Number of Server Referenced: 3
                </div>

                {/* MAKE THIS A BUTTON, ALIGN TO RIGHT 
                <div className="stats">
                  <i className="fas fa-redo mr-1"></i>
                  Refresh Now 
                </div> */}
              </Card.Footer>
              
            </Card>
          </Col>

          {/* CARD 3: SUDO DATA COUNT*/}
          <Col lg="4" sm="6">
            <Card className="card-stats">
              <Card.Body>
                <Row>
                  <Col xs="5">
                    <div className="icon-big text-center icon-warning">
                      <BsClipboard2Data />
                      {/*<i className="nc-icon nc-vector text-danger"></i> */}
                    </div>
                  </Col>
                  <Col xs="7">
                    <div className="numbers">
                      <p className="card-category">Number of Documents developed by SUDO</p>
                      <Card.Title as="h4">
                        <Sum_sudo />
                      </Card.Title>
                    </div>
                  </Col>
                </Row>
              </Card.Body>
              <Card.Footer>
                <hr></hr>
                <div className="stats">
                  <i className="nc-icon nc-single-copy-04"></i>
                  &nbsp; Number of SUDO files referenced: 2
                </div>
              </Card.Footer>
            </Card>
          </Col>

        </Row>

        {/* ROW 2: SHOW 1 or 2 visual on data */}
        <Row>

          {/* Twitter RADAR CHART */}
          <Col md="4">
            <Card>
              <Card.Header>
                <Card.Title as="h4">Topic with No. Tweet</Card.Title>
                <p className="card-category">This Rader Chart shows our selected Topics 
                and the number of posts contribute to each topic.</p>
              </Card.Header>
              <Card.Body>
                <RadarChartTwt /> 
              </Card.Body>
              <Card.Footer>
               
              </Card.Footer>
            </Card>
          </Col>

          {/* Mastodon RADAR CHART */}
          <Col md="4">
            <Card>
              <Card.Header>
                <Card.Title as="h4">Topic with No. Mastodon Post</Card.Title>
                <p className="card-category">This Radar Chart shows our swlected Topics and the number of Mastodon posts contribute to each topic.</p>
              </Card.Header>
              <Card.Body>
                <RadarChartMas />
              </Card.Body>
              <Card.Footer>
                
              </Card.Footer>
            </Card>
          </Col>

          {/* SUDO IV? */}
          <Col md="4">
            <Card>
              <Card.Header>
                <Card.Title as="h4">State and Suburb from SUDO</Card.Title>
                <p className="card-category">This Pie Chart gives a general idea of the geo-information of our choice from SUDO.</p>
              </Card.Header>
              <Card.Body>
                <PieChart />
              </Card.Body>
              <Card.Footer>
            
              </Card.Footer>
            </Card>
          </Col>

        </Row>

        {/* ROW 3: SHOW Lang on data */}
        <Row>

          {/* Twitter Chart lang */}
          <Col md="4">
            <Card>
              <Card.Header>
                <Card.Title as="h4">Language Distribution in Twitter Data</Card.Title>
                <p className="card-category"> This Pie chart shows the language Distribution in the provided twitter data
                  and the count of tweets in each language.
                </p>
              </Card.Header>
              <Card.Body>
                <DashboardLanTwt />
              </Card.Body>
              <Card.Footer>
              </Card.Footer>
            </Card>
          </Col>

          {/* Mastodon CHART Lang */}
          <Col md="4">
            <Card>
              <Card.Header>
                <Card.Title as="h4">Language Distribution in Mastodon Data</Card.Title>
                <p className="card-category">This Pie chart shows the language Distribution in the harvested Mastondon data
                  and the count of Mastodon in each language.</p>
              </Card.Header>
              <Card.Body>
              <DashboardLanMas />
              </Card.Body>
              <Card.Footer>
                
              </Card.Footer>
            </Card>
          </Col>

          {/* HASHTAG TABLE */}
          <Col md="4">
            <Card>
              <Card.Header>
                <Card.Title as="h4">Top 8 Hashtags from Twitter Data</Card.Title>
                  <p className="card-category">
                    This table shows the 8 most popular hashtags extracted from Twitter data, 
                    ranked by the number of tweets for each hashtag.
                  </p>
              </Card.Header>
              <Card.Body>
                <DashboardHastagBar />
              </Card.Body>
              <Card.Footer>
                
              </Card.Footer>
            </Card>
          </Col>

        </Row>

      {/* END OF DASHBOARD CONTENT */}
      </Container>
    </>
  );
  
}

export default Dashboard;
