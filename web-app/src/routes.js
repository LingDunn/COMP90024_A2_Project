/*!

=========================================================
* Light Bootstrap Dashboard React - v2.0.1
=========================================================

* Product Page: https://www.creative-tim.com/product/light-bootstrap-dashboard-react
* Copyright 2022 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/light-bootstrap-dashboard-react/blob/master/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/

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

import Dashboard from "views/Dashboard.js";
import UserProfile from "views/UserProfile.js";
import TableList from "views/TableList.js";
import Typography from "views/Typography.js";
import Icons from "views/Icons.js";
import Maps from "views/Maps.js";
import Notifications from "views/Notifications.js";
import Upgrade from "views/Upgrade.js";
/* MY OWN IMPORT */
import { BsFillHouseDoorFill } from "react-icons/bs";



const dashboardRoutes = [
  {
    path: "/dashboard",
    name: "Home",
    icon: "fa fa-home",
    component: Dashboard,
    layout: "/admin"
  },
  {
   
    path: "/sm",
    name: "1. Scott Morrison",
    icon: "fa fa-newspaper", 
    component: UserProfile, // this is the component to be changed for story 
    layout: "/admin"
  },
  {
    
    path: "/ukraine",
    name: "2. Ukraine",
    icon: "fa fa-newspaper", 
    component: TableList, // this is the component to be changed for story 
    layout: "/admin"
  },
  {
  
    path: "/cc",
    name: "3. Cryptocurrency",
    icon: "fa fa-globe", 
    component: Typography, // this is the component to be changed for story 
    layout: "/admin"
  },
  {
  
    path: "/nft",
    name: "4. NFT",
    icon: "fa fa-globe", //nc-icon nc-button-play
    component: Icons,
    layout: "/admin"
  },
  {
   
    path: "/af",
    name: "5. Adult Film",
    icon: "fa fa-play-circle", //nc-icon nc-button-play
    component: Maps,
    layout: "/admin"
  }

];

export default dashboardRoutes;
