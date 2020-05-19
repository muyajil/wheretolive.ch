import Form from "react-bootstrap/Form";
import React from "react";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import Button from "react-bootstrap/Button";

interface Props {
  handleChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  setStateInParent: (state: object) => void;
  birthYears: Array<number | undefined>;
  franchises: Array<number | undefined>;
  numPeople: number;
}

interface State {}

class HealthInfo extends React.Component<Props, State> {
  renderFranchiseInput(personId: number) {
    const controlId = "franchise-" + personId;
    const adultChoices = [300, 500, 1000, 1500, 2000, 2500];
    const childrenChoices = [0, 100, 200, 400, 600];
    const currentYear = new Date().getFullYear();
    const birthYear = this.props.birthYears[personId];
    let choices = [];

    if (
      birthYear !== undefined &&
      !isNaN(birthYear) &&
      birthYear !== null &&
      birthYear >= 1900
    ) {
      if (currentYear - birthYear >= 18) {
        choices = adultChoices;
      } else {
        choices = childrenChoices;
      }
      if (this.props.franchises[personId] === undefined) {
        const currentEntries = this.props.franchises;
        currentEntries[personId] = Math.min(...choices);
        this.props.setStateInParent({ franchises: currentEntries });
      }
      return (
        <Form.Group controlId={controlId}>
          <Form.Label>Franchise Person {personId + 1}</Form.Label>
          <Form.Control
            as="select"
            value={this.props.franchises[personId]}
            onChange={this.props.handleChange}
            placeholder="Choose Franchise"
            required={true}
          >
            {choices.map((option) => (
              <option>{option}</option>
            ))}
          </Form.Control>
        </Form.Group>
      );
    } else {
      return null;
    }
  }

  renderPersonInfoInput(personId: number) {
    const controlId = "birthYear-" + personId;
    const currentYear = new Date().getFullYear();

    return (
      <Row>
        <Col>
          <Form.Group controlId={controlId}>
            <Form.Label>Birth Year Person {personId + 1}</Form.Label>
            <Form.Control
              value={this.props.birthYears[personId]}
              onChange={this.props.handleChange}
              type="number"
              required={true}
              min={1940}
              max={currentYear}
            />
          </Form.Group>
        </Col>
        <Col>{this.renderFranchiseInput(personId)}</Col>
      </Row>
    );
  }

  renderHealthInsuranceForm() {
    const personFields = [];
    for (let personId = 0; personId < this.props.numPeople; personId++) {
      personFields.push(this.renderPersonInfoInput(personId));
    }
    return personFields;
  }
  render() {
    return (
      <Col
        xs={12}
        lg={6}
        xl={3}
        className="mt-5 mt-xl-0 pl-lg-5 pr-lg-5 border-right-lg"
      >
        <h5>
          <strong>Health Insurance Information:</strong>
        </h5>
        {this.renderHealthInsuranceForm()}
        <Row className="mb-5">
          <Col className="text-center">
            <Button
              variant="secondary"
              onClick={() =>
                this.props.setStateInParent({
                  numPeople: this.props.numPeople + 1,
                })
              }
            >
              Add Person
            </Button>
          </Col>
          <Col className="text-center">
            <Button
              variant="secondary"
              onClick={() => {
                const numPeople = Math.max(this.props.numPeople - 1, 1);
                this.props.setStateInParent({
                  numPeople: numPeople,
                  birthYears: this.props.birthYears.slice(0, numPeople),
                  franchises: this.props.franchises.slice(0, numPeople),
                });
              }}
            >
              Remove Person
            </Button>
          </Col>
        </Row>
      </Col>
    );
  }
}

export default HealthInfo;
