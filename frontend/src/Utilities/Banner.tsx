import React from "react";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import Image from "react-bootstrap/Image";
import logo_front from "../logo_front.png";

class Banner extends React.Component {
  render() {
    return (
      <Row className="bg-light .mt-n5 imageRow text-center">
        <Col>
          <Image src={logo_front} fluid />
        </Col>
      </Row>
    );
  }
}

export default Banner;
