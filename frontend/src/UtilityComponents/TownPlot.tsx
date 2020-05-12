// 2 plot types -> One for Total Cost and one for Commute Time, both histos
import React from "react";
import Container from "react-bootstrap/Container";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";

class TownPlot extends React.Component {
  render() {
    return (
      <Container fluid>
        <Row className="mt-5">
          <Col>
            <h1>TownPlot</h1>
          </Col>
        </Row>
      </Container>
    );
  }
}

export default TownPlot;
