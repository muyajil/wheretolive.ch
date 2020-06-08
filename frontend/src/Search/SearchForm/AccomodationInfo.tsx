import Form from "react-bootstrap/Form";
import React from "react";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";


interface Props{
    handleChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
    minRooms?: number;
    maxRooms?: number;
    minArea?: number;
    maxArea?: number;
    offerType: string;
}

interface State{}


class AccomodationInfo extends React.Component<Props, State> {
  render() {
      return(
    <Col xs={12} lg={6} xl={3} className="mt-5 mt-xl-0 pl-lg-5 pr-lg-5">
      <h5>
        <strong>Accomodation Information:</strong>
      </h5>
      <Row>
        <Col>
          <Form.Group controlId="minRooms">
            <Form.Label>Minimum Rooms</Form.Label>
            <Form.Control
              value={this.props.minRooms}
              onChange={this.props.handleChange}
              type="number"
              step="0.5"
            />
          </Form.Group>
        </Col>
        <Col>
          <Form.Group controlId="maxRooms">
            <Form.Label>Maximum Rooms</Form.Label>
            <Form.Control
              value={this.props.maxRooms}
              onChange={this.props.handleChange}
              type="number"
              step="0.5"
            />
          </Form.Group>
        </Col>
      </Row>
      <Row>
        <Col>
          <Form.Group controlId="minArea">
            <Form.Label>
              Minimum m<sup>2</sup>
            </Form.Label>
            <Form.Control
              value={this.props.minArea}
              onChange={this.props.handleChange}
              type="number"
            />
          </Form.Group>
        </Col>
        <Col>
          <Form.Group controlId="maxArea">
            <Form.Label>
              Maximum m<sup>2</sup>
            </Form.Label>
            <Form.Control
              value={this.props.maxArea}
              onChange={this.props.handleChange}
              type="number"
            />
          </Form.Group>
        </Col>
      </Row>
      <Row>
        <Col>
          <Form.Group controlId="offerType">
            <Form.Label>Offer Type</Form.Label>
            <Form.Control
              as="select"
              value={this.props.offerType}
              onChange={this.props.handleChange}
              required={true}
            >
              <option>Rent</option>
              <option>Buy</option>
            </Form.Control>
          </Form.Group>
        </Col>
        <Col></Col>
      </Row>
    </Col>);
  }
}

export default AccomodationInfo;