import Form from "react-bootstrap/Form";
import React from "react";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";

interface Props {
  handleChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  married: boolean;
  doubleSalary: boolean;
  numChildren?: number;
  income?: number;
}

interface State {}

class TaxInfo extends React.Component<Props, State> {
  renderDoubleSalaryCheckbox() {
    if (this.props.married) {
      return (
        <Form.Group controlId="doubleSalary">
          <Form.Check
            checked={this.props.doubleSalary}
            onChange={this.props.handleChange}
            type="switch"
            label="Double Earner"
          />
        </Form.Group>
      );
    } else {
      return null;
    }
  }
  render() {
    return (
      <Col xs={12} lg={6} xl={3} className="mt-5 mt-lg-0 pl-lg-5 pr-lg-5 border-right-xl">
        <h5>
          <strong>Tax Information:</strong>
        </h5>
        <Form.Group controlId="income">
          <Form.Label>Gross Income</Form.Label>
          <Form.Control
            value={this.props.income}
            onChange={this.props.handleChange}
            type="number"
            required={true}
            min={12500}
            max={10000000}
          />
        </Form.Group>

        <Form.Group controlId="numChildren">
          <Form.Label>Number of children</Form.Label>
          <Form.Control
            value={this.props.numChildren}
            onChange={this.props.handleChange}
            type="number"
            required={true}
          />
        </Form.Group>
        <Row>
          <Col>
            <Form.Group controlId="married">
              <Form.Check
                checked={this.props.married}
                onChange={this.props.handleChange}
                type="switch"
                label="Married"
              />
            </Form.Group>
          </Col>
          <Col>{this.renderDoubleSalaryCheckbox()}</Col>
        </Row>
      </Col>
    );
  }
}

export default TaxInfo;
