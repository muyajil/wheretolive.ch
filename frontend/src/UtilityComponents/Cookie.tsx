// https://stackoverflow.com/questions/39826992/how-can-i-set-a-cookie-in-react
import React from "react";
import Container from "react-bootstrap/Container";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";

class Cookie extends React.Component {
  render() {
    return (
      <Container fluid>
        <Row className="mt-5">
          <Col>
            <h1>Cookie</h1>
          </Col>
        </Row>
      </Container>
    );
  }
}

export default Cookie;
