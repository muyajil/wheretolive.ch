import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import React from "react";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import TownTypeahead from "../Utilities/TownTypeahead";

interface Props {
  handleSearchFormSubmission: (formState: State) => void;
}

export interface State {
  selectedTown: Array<Object | string>;
  income?: number;
  numChildren?: number;
  married: boolean;
  doubleSalary: boolean;
  validated: boolean;
  commuteTime: number;
  onlyTrainCommute: boolean;
  birthYears: Array<number | undefined>;
  franchises: Array<number | undefined>;
  numPeople: number;
  minRooms?: number;
  maxRooms?: number;
  minArea?: number;
  maxArea?: number;
  offerType: string;
}

class SearchForm extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);

    const state = localStorage.getItem("searchFormState");
    if (state) {
      this.state = JSON.parse(state);
    } else {
      this.state = this.getEmptyState()
    }

    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleHealthInsuranceChange = this.handleHealthInsuranceChange.bind(
      this
    );
  }

  getEmptyState() {
    return {
      selectedTown: [],
      income: undefined,
      numChildren: undefined,
      married: false,
      doubleSalary: false,
      validated: false,
      commuteTime: 0,
      onlyTrainCommute: false,
      birthYears: [undefined],
      franchises: [undefined],
      numPeople: 1,
      minRooms: undefined,
      maxRooms: undefined,
      minArea: undefined,
      maxArea: undefined,
      offerType: "",
    };
  }

  componentDidUpdate() {
    localStorage.setItem("searchFormState", JSON.stringify(this.state));
  }

  handleSubmit(event: any) {
    if (event.target.checkValidity() === false) {
      event.preventDefault();
      event.stopPropagation();
    } else {
      this.setState({ validated: true });
      console.log(JSON.stringify(this.state));
      this.props.handleSearchFormSubmission(this.state);
    }
    event.preventDefault();
  }

  handleHealthInsuranceChange(event: React.ChangeEvent<HTMLInputElement>) {
    const target = event.target;
    const personId = parseInt(target.id.split("-")[1], 10);
    const field = target.id.split("-")[0];
    if (field === "franchise") {
      const currentEntries = this.state.franchises;
      currentEntries[personId] = parseInt(target.value, 10);
      this.setState({ franchises: currentEntries });
    } else {
      const currentEntries = this.state.birthYears;
      currentEntries[personId] = parseInt(target.value, 10);
      this.setState({ birthYears: currentEntries });
    }
  }

  handleChange<T extends keyof State>(
    event: React.ChangeEvent<HTMLInputElement>
  ) {
    const target = event.target;
    const value =
      target.id === "doubleSalary" ||
      target.id === "married" ||
      target.id === "onlyTrainCommute"
        ? target.checked
        : target.value;
    const name = target.id;

    const newState = {
      [name]: value,
    };

    this.setState(newState as { [P in T]: State[P] });
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

  renderFranchiseInput(personId: number) {
    const controlId = "franchise-" + personId;
    const adultChoices = [300, 500, 1000, 1500, 2000, 2500];
    const childrenChoices = [0, 100, 200, 400, 600];
    const currentYear = new Date().getFullYear();
    const birthYear = this.state.birthYears[personId];
    let choices = [];

    if (birthYear !== undefined) {
      if (currentYear - birthYear >= 18) {
        choices = adultChoices;
      } else {
        choices = childrenChoices;
      }
      if (this.state.franchises[personId] === undefined) {
        const currentEntries = this.state.franchises;
        currentEntries[personId] = Math.min(...choices);
        this.setState({ franchises: currentEntries });
      }
      return (
        <Form.Group controlId={controlId}>
          <Form.Label>Franchise Person {personId + 1}</Form.Label>
          <Form.Control
            as="select"
            value={this.state.franchises[personId]}
            onChange={this.handleHealthInsuranceChange}
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
              value={this.state.birthYears[personId]}
              onChange={this.handleHealthInsuranceChange}
              type="number"
              placeholder="Enter Birth Year"
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

  renderMinutes() {
    var hours = Math.floor(this.state.commuteTime / 60);
    var minutes = this.state.commuteTime % 60;
    return (
      <p>
        {("0" + hours).slice(-2)}:{("0" + minutes).slice(-2)} h
      </p>
    );
  }

  renderHealthInsuranceForm() {
    const personFields = [];
    for (let personId = 0; personId < this.state.numPeople; personId++) {
      personFields.push(this.renderPersonInfoInput(personId));
    }
    return personFields;
  }

  render() {
    return (
      <Form
        className="text-light"
        validated={this.state.validated}
        onSubmit={this.handleSubmit}
      >
        <Row className="mt-5">
          <Col xs={12} lg={3} className="pl-lg-5 pr-lg-5 border-right">
            <h5>
              <strong>Commute Information:</strong>
            </h5>
            <Form.Group controlId="town">
              <Form.Label>Workplace Town</Form.Label>
              <TownTypeahead // check if value equivalent is offered by typeahead
                onChange={(selected: Array<Object | string>) => {
                  this.setState({ selectedTown: selected });
                }}
                selectedTown={this.state.selectedTown}
              />
            </Form.Group>
            <Form.Group controlId="commuteTime">
              <Form.Label>Maximum Commute Time</Form.Label>
              {this.renderMinutes()}
              <Form.Control
                value={this.state.commuteTime}
                onChange={this.handleChange}
                min={0}
                max={600}
                step={5}
                type="range"
              />
            </Form.Group>
            <Form.Group controlId="onlyTrainCommute">
              <Form.Check
                checked={this.state.onlyTrainCommute}
                onChange={this.handleChange}
                type="switch"
                label="Only consider time spent in train"
              />
            </Form.Group>
          </Col>
          <Col xs={12} lg={3} className="mt-5 mt-lg-0 pl-lg-5 pr-lg-5 border-right">
            <h5>
              <strong>Tax Information:</strong>
            </h5>
            <Form.Group controlId="income">
              <Form.Label>Gross Income</Form.Label>
              <Form.Control
                value={this.state.income}
                onChange={this.handleChange}
                type="number"
                placeholder="Enter income"
                required={true}
                min={12500}
                max={10000000}
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
          </Col>
          <Col xs={12} lg={3} className="mt-5 mt-lg-0 pl-lg-5 pr-lg-5 border-right">
            <h5>
              <strong>Health Insurance Information:</strong>
            </h5>
            {this.renderHealthInsuranceForm()}
            <Row className="mb-5">
              <Col className="text-center">
                <Button
                  variant="secondary"
                  onClick={() =>
                    this.setState({ numPeople: this.state.numPeople + 1 })
                  }
                >
                  Add Person
                </Button>
              </Col>
              <Col className="text-center">
                <Button
                  variant="secondary"
                  onClick={() => {
                    const numPeople = Math.max(this.state.numPeople - 1, 1);
                    this.setState({
                      numPeople: numPeople,
                      birthYears: this.state.birthYears.slice(0, numPeople),
                      franchises: this.state.franchises.slice(0, numPeople),
                    });
                  }}
                >
                  Remove Person
                </Button>
              </Col>
            </Row>
          </Col>
          <Col xs={12} lg={3} className="mt-5 mt-lg-0 pl-lg-5 pr-lg-5">
            <h5>
              <strong>Accomodation Information:</strong>
            </h5>
            <Row>
              <Col>
                <Form.Group controlId="minRooms">
                  <Form.Label>Minimum Rooms</Form.Label>
                  <Form.Control
                    value={this.state.minRooms}
                    onChange={this.handleChange}
                    type="decimal"
                    placeholder="Minimum Rooms"
                  />
                </Form.Group>
              </Col>
              <Col>
                <Form.Group controlId="maxRooms">
                  <Form.Label>Maximum Rooms</Form.Label>
                  <Form.Control
                    value={this.state.maxRooms}
                    onChange={this.handleChange}
                    type="decimal"
                    placeholder="Maximum Rooms"
                  />
                </Form.Group>
              </Col>
            </Row>
            <Row>
              <Col>
                <Form.Group controlId="minArea">
                  <Form.Label>Minimum Area</Form.Label>
                  <Form.Control
                    value={this.state.minArea}
                    onChange={this.handleChange}
                    type="number"
                    placeholder="Minimum Area"
                  />
                </Form.Group>
              </Col>
              <Col>
                <Form.Group controlId="maxArea">
                  <Form.Label>Maximum Area</Form.Label>
                  <Form.Control
                    value={this.state.maxArea}
                    onChange={this.handleChange}
                    type="number"
                    placeholder="Maximum Area"
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
                    value={this.state.offerType}
                    onChange={this.handleChange}
                    required={true}
                  >
                    <option>Rent</option>
                    <option>Purchase</option>
                  </Form.Control>
                </Form.Group>
              </Col>
              <Col></Col>
            </Row>
          </Col>
        </Row>
        <Row className="mt-5">
          <Col xs={12} className="text-center">
            <Button className="ml-n2" variant="primary" type="submit">
              Begin Search!
            </Button>
            <Button className="ml-2" variant="primary" type="reset" onClick={() => this.setState(this.getEmptyState())}>
              Reset Form
            </Button>
          </Col>
        </Row>
      </Form>
    );
  }
}

export default SearchForm;
