import React from "react";
import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import Navigation from "./Navigation";
import WelcomeContent from "./Welcome";
import TaxCalculator from "./TaxCalculator/TaxCalculator";
import { Route, Switch } from "react-router-dom";
import Container from "react-bootstrap/Container";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import Image from "react-bootstrap/Image";
import bgImage from "./bg_image.png";


class App extends React.Component {
  render() {
    return (
      <div>
        <Navigation />
        <Container fluid>
        <Row className="imageRow text-center">
          <Col>
            <Image src={bgImage} fluid />
          </Col>
        </Row>
        </Container>
        <Switch>
          <Route exact path="/" component={WelcomeContent} />
          <Route path="/taxes" component={TaxCalculator} />
        </Switch>
      </div>
    );
  }
}

export default App;