import React from "react";
import Container from "react-bootstrap/Container";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";

class TownTable extends React.Component {
  render() {
    return (
      <Container fluid>
        <Row className="mt-5">
          <Col>
            <h1>TownTable</h1>
          </Col>
        </Row>
      </Container>
    );
  }
}

export default TownTable;
