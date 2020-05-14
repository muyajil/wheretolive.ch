import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import React from "react";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import TownTypeahead from "../Utilities/TownTypeahead";

interface Props {
  handleTaxFormSubmission: (
    formState: State
  ) => void;
}

export interface State {
  selectedTown: Array<Object | string>;
  income?: number;
  numChildren?: number;
  married: boolean;
  doubleSalary: boolean;
  validated: boolean;
}

class TaxForm extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);

    const state = localStorage.getItem("taxFormState");
    if (state) {
      const state_parsed = JSON.parse(state);
      this.state = state_parsed;
      this.props.handleTaxFormSubmission(this.state);
    } else {
      this.state = {
        selectedTown: [],
        income: undefined,
        numChildren: undefined,
        married: false,
        doubleSalary: false,
        validated: false,
      };
    }

    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleSubmit(event: any) {
    if (event.target.checkValidity() === false) {
      event.preventDefault();
      event.stopPropagation();
    } else {
      this.setState({ validated: true });

      this.props.handleTaxFormSubmission(this.state);
    }
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

  componentDidUpdate() {
    localStorage.setItem("taxFormState", JSON.stringify(this.state));
  }

  renderDoubleSalaryCheckbox() {
    if (this.state.married) {
      return (
        <Form.Group controlId="doubleSalary">
          <Form.Check
            checked={this.state.doubleSalary}
            onChange={this.handleChange}
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
      <Form validated={this.state.validated} onSubmit={this.handleSubmit}>
        <Form.Group controlId="town">
          <Form.Label>Town</Form.Label>
          <TownTypeahead // check if value equivalent is offered by typeahead
            onChange={(selected: Array<Object | string>) => {
              this.setState({ selectedTown: selected });
            }}
            selectedTown={this.state.selectedTown}
          />
        </Form.Group>
        <Form.Group controlId="income">
          <Form.Label>Gross Income</Form.Label>
          <Form.Control
            value={this.state.income}
            onChange={this.handleChange}
            type="number"
            placeholder="Enter income"
            min={12500}
            max={10000000}
            required={true}
          />
        </Form.Group>

        <Form.Group controlId="numChildren">
          <Form.Label>Number of children</Form.Label>
          <Form.Control
            value={this.state.numChildren}
            onChange={this.handleChange}
            type="number"
            placeholder="Enter number of children"
            required={true}
          />
        </Form.Group>
        <Row>
          <Col>
            <Form.Group controlId="married">
              <Form.Check
                checked={this.state.married}
                onChange={this.handleChange}
                type="switch"
                label="Married"
              />
            </Form.Group>
          </Col>
          <Col>{this.renderDoubleSalaryCheckbox()}</Col>
        </Row>

        <Button variant="primary" type="submit">
          Calculate Taxes!
        </Button>
      </Form>
    );
  }
}

export default TaxForm;
