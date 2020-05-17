import React from "react";
import icon from "./icon.png";
import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";
import { LinkContainer } from "react-router-bootstrap";

class Navigation extends React.Component {
  render() {
    return (
      <Navbar bg="dark" variant="dark" expand="lg">
        <Navbar.Brand href="/">
          <img
            alt=""
            src={icon}
            width="30"
            height="30"
            className="d-inline-block align-top"
          />{" "}
          wheretolive
        </Navbar.Brand>
        <Nav className="mr-auto">
            <LinkContainer exact to="/">
              <Nav.Link>Home</Nav.Link>
            </LinkContainer>
            <LinkContainer to="/search">
              <Nav.Link>Search</Nav.Link>
            </LinkContainer>
            <LinkContainer to="/taxes">
              <Nav.Link>Tax Calculator</Nav.Link>
            </LinkContainer>
        </Nav>
      </Navbar>
    );
  }
}

export default Navigation;
