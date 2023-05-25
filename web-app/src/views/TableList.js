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

// Ukraine
import React, { useState, useEffect, component } from "react";
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
/* MY OWN IMPORT */
import { MapContainer, TileLayer, FeatureGroup, GeoJSON } from "react-leaflet"
import Map_sm from "components/IV/Map"
import { useRef } from "react"
import "../map.css";
import 'leaflet/dist/leaflet.css'
import { UkTwtPie } from "components/IV/UkTwtPie"
import { UkMasPie } from "components/IV/UkMasPie";
import states from "../data/states.json";
import { Distribution } from "components/IV/Distribution"
import axios from '../my-axios';

function TableList() {

  // Distribution Confg
  const [Loc, setLoc] = useState("")
  const [Dist, setDist] = useState("")
  const [distData, setdistData] = useState()
  const [suburbs, setSuburbs] = useState()
  // MAP confg
  const [center, setCenter] = useState({ lat: -25.0, lng: 135.0 });
  const ZOOM_LEVEL = 4;
  const mapRef = useRef();
  // API var
  const [data, setData] = useState([{}])
  const [loading, setLoading] = useState(true)
  //const [error, setError] = useState([{}])
  // Note topic
  const topic = "ukraine"

  // for Distribution
  const postLoc = (location) => {
    // construct dist data base on new loc?
    setLoc(location)
    // to set dist data
    get_dist_data(location)
  }
  const postDist = (distribution) => {
    // construct dist data base on new dist?
    setDist(distribution)
    get_dist_data(undefined, distribution)
    setDist(distribution)
  }

  // distribution functions
  function get_dist_data(loc, dist) {
    let loc_to_use = Loc
    let dist_to_use = Dist
    if (loc !== undefined) {
      loc_to_use = loc
    }
    if (dist !== undefined) {
      dist_to_use = dist
    }

    if (loc_to_use == "australia") {
      let d_data = get_dist(dist_to_use, data.aus)
      setdistData(d_data)
      setSuburbs(data.aus.sub)
    }
    if (loc_to_use == "new south wales") {
      let d_data = get_dist(dist_to_use, data.nsw)
      setdistData(d_data)
      setSuburbs(data.nsw.sub)
    }
    if (loc_to_use == "victoria") {
      let d_data = get_dist(dist_to_use, data.vic)
      setdistData(d_data)
      setSuburbs(data.vic.sub)
    }
    if (loc_to_use == "queensland") {
      let d_data = get_dist(dist_to_use, data.qsl)
      setdistData(d_data)
      setSuburbs(data.qsl.sub)
    }
    if (loc_to_use == "south australia") {
      let d_data = get_dist(dist_to_use, data.sa)
      setdistData(d_data)
      setSuburbs(data.sa.sub)
    }
    if (loc_to_use == "western australia") {
      let d_data = get_dist(dist_to_use, data.wa)
      setdistData(d_data)
      setSuburbs(data.wa.sub)
    }
    if (loc_to_use == "tasmania") {
      let d_data = get_dist(dist_to_use, data.tas)
      setdistData(d_data)
      setSuburbs(data.tas.sub)
    }
    if (loc_to_use == "northern territory") {
      let d_data = get_dist(dist_to_use, data.nt)
      setdistData(d_data)
      setSuburbs(data.nt.sub)
    }
    if (loc_to_use == "australian capital territory") {
      let d_data = get_dist(dist_to_use, data.act)
      setdistData(d_data)
      setSuburbs(data.act.sub)
    }
  }

  function get_dist(dist, d) {

    if (dist == "med") {
      let this_d = d.med_inc
      return this_d
    }
    if (dist == "emp") {
      let this_d = d.emp_rate
      return this_d

    }
    if (dist == "lf") {
      let this_d = d.part_rate
      return this_d
    }
    if (dist == "uni") {
      let this_d = d.uni_rate
      return this_d
    }
    if (dist == "tafe") {
      let this_d = d.tafe_rate
      return this_d
    }
    if (dist == "y12") {
      let this_d = d.y12_rate
      return this_d

    }
  }

  // get API data
  useEffect(() => {
    async function get_data() {
      await axios.get("/uk_map_data").then(
        response => {
          setData(response.data)
          setLoc("australia")
          setDist("med")
          setdistData(response.data.aus.med_inc)
          setSuburbs(response.data.aus.sub)
        }
      )
      return onEachState
    }
    get_data()
  }, [])

  // Display page depends on loading state
  if (loading) {

    if (data.map_data) {
      setLoading(false)
    }

    return (
      <>
        <Container fluid>
          <h3>Loading...</h3>
        </Container>
      </>
    )

  } else {

    // Get map ready
    const map_data = data.map_data
    const onEachState = (state, layer) => {
      const state_name = state.properties.STATE_NAME;
      //layer.bindPopup(state_name);
      map_data.forEach((item) => {
        if (state_name == item.state) {
          {/* Construct tooltip for this MAP*/ }
          layer.bindPopup(state_name + " - Count of Tweets: " + item.cnt + " (Age Avg: " + item.mid_age + ", Weekly Income Avg: $" + item.mid_week_inc + ", Sentiment Avg: " + item.sent + ")")
        }
      });
    }

    // return entire page
    return (
      <>
        <Container fluid>

          {/* MAP & POST COUNT */}
          <Row>

            {/* MAP: 8 states */}
            <Col md="9">
              <Card>
                <Card.Header>
                  <Card.Title as="h4">"Ukraine" Tweet Count per State</Card.Title>
                </Card.Header>
                <Card.Body>
                  <MapContainer center={center} zoom={ZOOM_LEVEL} ref={mapRef}>
                    <TileLayer url={Map_sm.maptiler.url} attribution={Map_sm.maptiler.attribution} />
                    <GeoJSON data={states.features} onEachFeature={onEachState} />
                  </MapContainer>
                </Card.Body>
              </Card>
            </Col>

            {/* TWT VS MAS TOPIC PERCENT */}
            <Col md="3">

              <Card>
                <Card.Header>
                  <Card.Title as="h5">"Ukraine" Twitter Tweet Count vs Entire Tweet Count </Card.Title>
                  {/* </Card.Header></Card><p className="card-category"></p> */}
                </Card.Header>
                <Card.Body>
                  <UkTwtPie />
                </Card.Body>
              </Card>

              <Card>
                <Card.Header>
                  <Card.Title as="h5">"Ukraine" Mastodon Toot Count vs Overall Toot Count</Card.Title>
                </Card.Header>
                <Card.Body>
                  <UkMasPie />
                </Card.Body>
              </Card>

            </Col>

          </Row>

          {/* loc BUTTONS, PROPERTY BUTTONS, DISTRIBUTION */}
          <Row >

            <Col md="12">
              <Card>
                <Card.Header>
                  <Card.Title as="h4">Choose Distribution Location and Type</Card.Title>
                </Card.Header>
                <Card.Body>
                  <div className="button-container mr-auto ml-auto">
                    <Button onClick={() => postLoc("australia")} className="btn-primary" > {/*type="submit" variant=""*/}
                      AUS
                    </Button>
                    <Button Style="padding:3px; border:0px;" />

                    <Button onClick={() => postLoc("new south wales")} className=" pull-right btn-primary" variant="">
                      NSW
                    </Button>
                    <Button Style="padding:3px; border:0px;" />

                    <Button onClick={() => postLoc("victoria")} className=" pull-right btn-primary" variant="">
                      VIC.
                    </Button>
                    <Button Style="padding:3px; border:0px;" />

                    <Button onClick={() => postLoc("queensland")} className="pull-right btn-primary" variant="">
                      QLD
                    </Button>
                    <Button Style="padding:3px; border:0px;" />

                    <Button onClick={() => postLoc("south australia")} className=" pull-right btn-primary" variant="">
                      SA
                    </Button>
                    <Button Style="padding:3px; border:0px;" />

                    <Button onClick={() => postLoc("western australia")} className=" pull-right btn-primary" variant="">
                      WA
                    </Button>
                    <Button Style="padding:3px; border:0px;" />

                    <Button onClick={() => postLoc("tasmania")} className=" pull-right btn-primary" variant="">
                      TAS.
                    </Button>
                    <Button Style="padding:3px; border:0px;" />

                    <Button onClick={() => postLoc("northern territory")} className=" pull-right btn-primary" variant="">
                      NT
                    </Button>
                    <Button Style="padding:3px; border:0px;" />

                    <Button onClick={() => postLoc("australian capital territory")} className=" pull-right btn-primary" variant="">
                      ACT
                    </Button>
                  </div>
                </Card.Body>

                <Card.Body>
                  <div className="button-container mr-auto ml-auto">
                    <Button onClick={() => postDist("med")} className=" pull-right btn-warning" variant="">
                      Median Income
                    </Button>
                    <Button Style="padding:3px; border:0px;" />

                    <Button onClick={() => postDist("emp")} className=" pull-right btn-warning" variant="">
                      Employment Rate
                    </Button>
                    <Button Style="padding:3px; border:0px;" />

                    <Button onClick={() => postDist("lf")} className=" pull-right btn-warning" variant="">
                      Labor Force
                    </Button>
                    <Button Style="padding:3px; border:0px;" />

                    <Button onClick={() => postDist("uni")} className=" pull-right btn-warning" variant="">
                      Uni Rate
                    </Button>
                    <Button Style="padding:3px; border:0px;" />

                    <Button onClick={() => postDist("tafe")} className=" pull-right btn-warning" variant="">
                      Tafe Rate
                    </Button>
                    <Button Style="padding:3px; border:0px;" />

                    <Button onClick={() => postDist("y12")} className=" pull-right btn-warning" variant="">
                      Y12 Rate
                    </Button>
                    <Button Style="padding:3px; border:0px;" />
                  </div>
                </Card.Body>

                <hr />

                <Card.Body>
                  <Distribution topic={topic} loc={Loc} dist={Dist} data={distData} sub={suburbs} />
                </Card.Body>
              </Card>
            </Col>

          </Row>

        </Container>
      </>
    )

  }

}

export default TableList;
