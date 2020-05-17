import React from "react";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import Container from "react-bootstrap/Container";
import TaxForm, {State as TaxFormState} from "./TaxForm";
import TaxHistogram from "./TaxHistogram";
import Banner from "../Utilities/Banner";

interface Props {}

interface State {
  targetTownIdx: number;
  targetTownTaxes: number;
  targetTownName: string;
  taxesComputed: boolean;
  figureData: string;
}

class TaxCalculator extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      targetTownIdx: -1,
      targetTownTaxes: 0,
      targetTownName: "",
      taxesComputed: false,
      figureData: "",
    };
    this.handleTaxFormSubmission = this.handleTaxFormSubmission.bind(this);
  }

  handleTaxFormSubmission(
    taxFormState: TaxFormState
  ) {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        targetTown: taxFormState.selectedTown[0],
        income: taxFormState.income,
        numChildren: taxFormState.numChildren,
        married: taxFormState.married,
        doubleSalary: taxFormState.doubleSalary,
      }),
    };

    fetch(process.env.REACT_APP_BACKEND_URL +"/tax_calculator/", requestOptions)
      .then((response) => response.json())
      .then((data) => {
        this.setState({
          targetTownIdx: data["target_town_idx"],
          targetTownTaxes: data["target_town_taxes"],
          targetTownName: data["target_town_name"],
          figureData: data["figure_data"],
          taxesComputed: true,
        });
      });
  }

  renderTaxes() {
    if (this.state.taxesComputed) {
      return (
        <h3 className="text-light">
          People with your profile in{" "}
          <strong>{this.state.targetTownName}</strong> pay on average{" "}
          <strong>
            CHF {new Intl.NumberFormat("ch").format(this.state.targetTownTaxes)}
            .-
          </strong>{" "}
          in taxes per year.
        </h3>
      );
    }
  }

  renderHistogram() {
    if (this.state.taxesComputed) {
      return (
        <div>
          <h4 className="text-light">Switzerland wide comparison:</h4>
          <TaxHistogram
            data={JSON.parse(this.state.figureData)}
            targetTownIdx={this.state.targetTownIdx}
          />
        </div>
      );
    }
  }

  render() {
    return (
      <Container fluid>
        <Banner />
        <Row className="mt-5 max-h-500">
          <Col className="text-light" xs={12} lg={4}>
            <TaxForm handleTaxFormSubmission={this.handleTaxFormSubmission} />
          </Col>
          <Col xs={12} lg={8}>
            {this.renderTaxes()}
            {this.renderHistogram()}
          </Col>
        </Row>
      </Container>
    );
  }
}

export default TaxCalculator;
