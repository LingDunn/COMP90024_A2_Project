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

/*
import allows the import of functionality from other modules.
*/
import React, { Component } from "react";

/* react-router is the core package containing standard components and functionalities to implement routing in React applications. 
On the other hand, react-router-dom is a specialized package that you can use only in web-browser-based application development */
import { useLocation, NavLink } from "react-router-dom";

/* React-Bootstrap is a complete re-implementation of the Bootstrap components using React. It has no dependency on either bootstrap.js or jQuery. 
If you have React setup and React-Bootstrap installed, you have everything you need. */
import { Nav } from "react-bootstrap";


/* define Sidebar function, allow to export at the end of page */
function Sidebar({ color, image, routes }) {
  const location = useLocation(); // ??
  const activeRoute = (routeName) => {
    return location.pathname.indexOf(routeName) > -1 ? "active" : "";
  }; // ??
  //console.log(routes)
  return (
    <div className="sidebar" data-image={image} data-color={color}>
      
      {/* Set Sidebar background image */}
      <div
        className="sidebar-background"
        style={{
          backgroundImage: "url(" + image + ")"
        }}
      />


      {/* SIDEBAR CONTENT START */}
      <div className="sidebar-wrapper">

        {/* sidebar head section logo + COMP90024 */}
        <div className="logo d-flex align-items-center justify-content-start">
          <a
            href="/"
            className="simple-text logo-mini mx-1"
          >
            <div className="logo-img">
              <img src={require("assets/img/reactlogo.png")} alt="..." />
            </div>
          </a>
          <a className="simple-text" href="/">
            COMP90024 CCC
          </a>
        </div>

        {/* Sidebar buttons: loop through list of buttons */}
        {/* Base Nav component from react-bootstrap, see doc for more */}
        <Nav>
          {/* 
          Elements are from the list routes
          prop: ???
          key: ???
          */}
          
          {routes.map((prop, key) => {
            if (!prop.redirect)
              {/* Return a li tag with the button name & navLink */}
              return (
                <li
                  className={
                    prop.upgrade
                      ? "active active-pro"
                      : activeRoute(prop.layout + prop.path)
                  }
                  /* For each li ele, there's a unique key to be set
                  to uniquely identify this ele from its sibilings */
                  key={key}
                >
                  <NavLink
                    to={prop.layout + prop.path}
                    className="nav-link"
                    activeClassName="active"
                  >
                    <i className={prop.icon} />
                    <p>{prop.name}</p>
                  </NavLink>
                </li>
              );
            return null;
          })}
        </Nav>
      </div>
    </div>
  );
}

{/*
export keyword labels variables and functions that 
should be accessible from outside the current module. 
*/}
export default Sidebar;
