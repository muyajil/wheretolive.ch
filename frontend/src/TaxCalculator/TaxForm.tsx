import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import React from "react";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import TownTypeahead from "../Utilities/TownTypeahead";

interface Props {
  handleTaxFormSubmission: (
    townId: Object | string,
    income: number,
    numChildren: number,
    married: boolean,
    doubleSalary: boolean
  ) => void;
}

interface State {
  selectedTown: Array<Object | string>;
  income: number;
  numChildren: number;
  married: boolean;
  doubleSalary: boolean;
  validated: boolean;
}

class TaxForm extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);

    this.state = {
      selectedTown: [],
      income: 0,
      numChildren: 0,
      married: false,
      doubleSalary: false,
      validated: false
    };

    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }
  handleSubmit(event: any) {
    if (event.target.checkValidity() === false) {
      event.preventDefault();
      event.stopPropagation();
    }

    this.setState({validated: true});

    this.props.handleTaxFormSubmission(
      this.state.selectedTown[0],
      this.state.income,
      this.state.numChildren,
      this.state.married,
      this.state.doubleSalary
    );
    event.preventDefault();
  }

  handleChange<T extends keyof State>(
    event: React.ChangeEvent<HTMLInputElement>
  ) {
    const target = event.target;
    const value =
      target.id === "doubleSalary" || target.id === "married"
        ? target.checked
        : target.value;
    const name = target.id;

    const newState = {
      [name]: value,
    };

    this.setState(newState as { [P in T]: State[P] });
  }

  render() {
    return (
      <Form validated={this.state.validated} onSubmit={this.handleSubmit}>
        <Form.Group controlId="town">
          <Form.Label>Town</Form.Label>
          <TownTypeahead // check if value equivalent is offered by typeahead
            onChange={(selected: Array<Object | string>) => {
              this.setState({ selectedTown: selected });
            }}
          />
        </Form.Group>
        <Form.Group controlId="income">
          <Form.Label>Income</Form.Label>
          <Form.Control
            value={this.state.income}
            onChange={this.handleChange}
            type="number"
            placeholder="Enter income"
          />
        </Form.Group>

        <Form.Group controlId="numChildren">
          <Form.Label>Number of children</Form.Label>
          <Form.Control
            value={this.state.numChildren}
            onChange={this.handleChange}
            type="number"
            placeholder="Enter number of children"
          />
        </Form.Group>
        <Row>
          <Col>
            <Form.Group controlId="married">
              <Form.Check
                checked={this.state.married}
                onChange={this.handleChange}
                type="checkbox"
                label="Married"
              />
            </Form.Group>
          </Col>
          <Col>
            <Form.Group controlId="doubleSalary">
              <Form.Check
                checked={this.state.doubleSalary}
                onChange={this.handleChange}
                type="checkbox"
                label="Double Earner"
              />
            </Form.Group>
          </Col>
        </Row>

        <Button variant="primary" type="submit">
          Calculate Taxes!
        </Button>
      </Form>
    );
  }
}

export default TaxForm;
