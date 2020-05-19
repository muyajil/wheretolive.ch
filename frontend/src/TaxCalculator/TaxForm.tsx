import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import React from "react";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import TownTypeahead from "../Utilities/TownTypeahead";
import debounce from "lodash.debounce";

interface Props {
  handleTaxFormSubmission: (formState: State) => void;
  resetCalculator: () => void;
}

interface TaxForm {
  typeaheadRef: any;
  formRef: any;
}

export interface State {
  selectedTown: Array<Object | string>;
  income?: number;
  numChildren?: number;
  married: boolean;
  doubleSalary: boolean;
  validated: boolean;
  key: number;
}

class TaxForm extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);

    const state = localStorage.getItem("taxFormState");
    if (state) {
      this.state = JSON.parse(state);
      if (this.state.validated) {
        this.props.handleTaxFormSubmission(this.state);
      }
    } else {
      this.state = this.getEmptyState();
    }

    this.typeaheadRef = React.createRef();
    this.formRef = React.createRef();

    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleReset = this.handleReset.bind(this);
  }

  getEmptyState() {
    return {
      selectedTown: [],
      income: undefined,
      numChildren: undefined,
      married: false,
      doubleSalary: false,
      validated: false,
      key: Date.now(),
    };
  }

  handleSubmit(event: any) {
    if (event.target.checkValidity() === false) {
      event.preventDefault();
      event.stopPropagation();
    } else {
      this.setState({ validated: true });

      this.props.handleTaxFormSubmission(this.state);
    }
    window.focus();
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
    if (this.state.validated) {
      this.debounceHandleSubmit();
    }
  }

  handleReset(event: any) {
    event.target.reset();
    this.typeaheadRef.current.clear();
    this.props.resetCalculator();
    this.setState(this.getEmptyState());
  }

  debounceHandleSubmit = debounce(() => this.formRef.current.dispatchEvent(new Event('submit')), 500);

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
      <div key={this.state.key}>
        <Form
          validated={this.state.validated}
          onSubmit={this.handleSubmit}
          onReset={this.handleReset}
          ref={this.formRef}
        >
          <Form.Group controlId="town">
            <Form.Label>Town</Form.Label>
            <TownTypeahead
              onChange={(selected: Array<Object | string>) => {
                this.setState({ selectedTown: selected });
                this.debounceHandleSubmit();
              }}
              selectedTown={this.state.selectedTown}
              typeaheadRef={this.typeaheadRef}
            />
          </Form.Group>
          <Form.Group controlId="income">
            <Form.Label>Gross Income</Form.Label>
            <Form.Control
              value={this.state.income}
              onChange={this.handleChange}
              type="number"
              min={12500}
              max={9999999}
              required={true}
            />
          </Form.Group>

          <Form.Group controlId="numChildren">
            <Form.Label>Number of children</Form.Label>
            <Form.Control
              value={this.state.numChildren}
              onChange={this.handleChange}
              type="number"
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
          <Button className="ml-2" variant="primary" type="reset">
            Reset Form
          </Button>
        </Form>
      </div>
    );
  }
}

export default TaxForm;
