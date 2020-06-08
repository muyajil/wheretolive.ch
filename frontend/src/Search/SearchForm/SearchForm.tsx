import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import React from "react";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import AccomodationInfo from "./AccomodationInfo";
import TaxInfo from "./TaxInfo";
import CommuteInfo from "./CommuteInfo";
import HealthInfo from "./HealthInfo";

interface Props {
  handleSearchFormSubmission: (formState: State) => void;
}

interface SearchForm {
  typeaheadRef: any;
}

export interface State {
  selectedTown: Array<Object | string>;
  typeaheadValid: boolean;
  typeaheadInvalid: boolean;
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
  key: number;
}

class SearchForm extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);

    const state = localStorage.getItem("searchFormState");
    if (state) {
      this.state = JSON.parse(state);
      // if (this.state.validated) {
      //   this.props.handleSearchFormSubmission(this.state);
      // }
    } else {
      this.state = this.getEmptyState();
    }
    this.typeaheadRef = React.createRef();

    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleReset = this.handleReset.bind(this);
    this.handleTypeaheadChange = this.handleTypeaheadChange.bind(this);
    this.setStateInParent = this.setStateInParent.bind(this);
    this.handleHealthInsuranceChange = this.handleHealthInsuranceChange.bind(
      this
    );
  }

  getEmptyState() {
    return {
      selectedTown: [],
      typeaheadInvalid: false,
      typeaheadValid: false,
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
      offerType: "Rent",
      key: Date.now(),
    };
  }

  setStateInParent(state: object) {
    this.setState(state);
  }

  componentDidUpdate() {
    localStorage.setItem("searchFormState", JSON.stringify(this.state));
  }

  handleSubmit(event: any) {
    if (event.target.checkValidity() === false || this.state.selectedTown.length !== 1) {
      event.preventDefault();
      this.setState({ typeaheadInvalid: true, typeaheadValid: false});
      event.stopPropagation();
    } else {
      this.setState({ validated: true, typeaheadInvalid: false, typeaheadValid: true });

      this.props.handleSearchFormSubmission(this.state);
    }
    window.focus();
    event.preventDefault();
  }

  handleReset(event: any) {
    event.target.reset();
    this.typeaheadRef.current.clear();
    this.setState(this.getEmptyState());
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

  handleTypeaheadChange = (selected: Array<Object | string>) =>
    this.setState({ selectedTown: selected });

  validateNumbers(newState: any) {
    let newMinRooms = newState["minRooms"] ? newState["minRooms"] : this.state.minRooms;
    let newMaxRooms = newState["maxRooms"] ? newState["maxRooms"] : this.state.maxRooms;
    let newMinArea = newState["minArea"] ? newState["minArea"] : this.state.minArea;
    let newMaxArea = newState["maxArea"] ? newState["maxArea"] : this.state.maxArea;
    let changed = false;
    if (newMinRooms && newMaxRooms) {
      if (newMinRooms > newMaxRooms) {
        [newMinRooms, newMaxRooms] = [newMaxRooms, newMinRooms];
        changed = true;
      }
    }
    if (newMinRooms && newMinRooms % 0.5 !== 0){
      newMinRooms = Math.round(newMinRooms*2)/2;
      changed = true;
    }

    if (newMaxRooms && newMaxRooms % 0.5 !== 0){
      newMaxRooms = Math.round(newMaxRooms*2)/2;
      changed = true;
    }

    if (newMinArea && newMaxArea) {
      if (newMinArea > newMaxArea) {
        [newMinArea, newMaxArea] = [newMaxArea, newMinArea];
        changed = true;
      }
    }

    if (changed){
      return {
        minRooms: newMinRooms,
        maxRooms: newMaxRooms,
        minArea: newMinArea,
        maxArea: newMaxArea,
        key: Date.now()
      }
    } else {
      return {}
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

    const mergedState = {...newState, ...this.validateNumbers(newState)}

    this.setState(mergedState as { [P in T]: State[P] });
  }

  render() {
    return (
      <div key={this.state.key}>
        <Form
          className="text-light"
          validated={this.state.validated}
          onSubmit={this.handleSubmit}
          onReset={this.handleReset}
        >
          <Row className="mt-5">
            <CommuteInfo
              handleChange={this.handleChange}
              handleTypeaheadChange={this.handleTypeaheadChange}
              typeaheadRef={this.typeaheadRef}
              commuteTime={this.state.commuteTime}
              onlyTrainCommute={this.state.onlyTrainCommute}
              selectedTown={this.state.selectedTown}
              typeaheadInvalid={this.state.typeaheadInvalid}
              typeaheadValid={this.state.typeaheadValid}
            />
            <TaxInfo
              handleChange={this.handleChange}
              married={this.state.married}
              doubleSalary={this.state.doubleSalary}
              income={this.state.income}
              numChildren={this.state.numChildren}
            />
            <HealthInfo
              handleChange={this.handleHealthInsuranceChange}
              setStateInParent={this.setStateInParent}
              franchises={this.state.franchises}
              birthYears={this.state.birthYears}
              numPeople={this.state.numPeople}
            />

            <AccomodationInfo
              handleChange={this.handleChange}
              minArea={this.state.minArea}
              minRooms={this.state.minRooms}
              maxArea={this.state.maxArea}
              maxRooms={this.state.maxRooms}
              offerType={this.state.offerType}
            />
          </Row>
          <Row className="mt-5">
            <Col xs={12} className="text-center">
              <Button className="ml-n2" variant="primary" type="submit">
                Begin Search!
              </Button>
              <Button
                className="ml-2"
                variant="primary"
                type="reset"
                onClick={() => this.setState(this.getEmptyState())}
              >
                Reset Form
              </Button>
            </Col>
          </Row>
        </Form>
      </div>
    );
  }
}

export default SearchForm;
