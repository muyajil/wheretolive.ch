import React from "react";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import Container from "react-bootstrap/Container";
import TaxForm, { State as TaxFormState } from "./TaxForm";
import TaxHistogram from "./TaxHistogram";
import Banner from "../Utilities/Banner";
import publicIp from "public-ip";

interface Props {}

interface State {
  targetTownId: number;
  targetTownTaxes: number;
  targetTownName: string;
  taxesComputed: boolean;
  taxData: string;
}

class TaxCalculator extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      targetTownId: 0,
      targetTownTaxes: 0,
      targetTownName: "",
      taxesComputed: false,
      taxData: "",
    };
    this.handleTaxFormSubmission = this.handleTaxFormSubmission.bind(this);
    this.reset = this.reset.bind(this);
  }

  handleTaxFormSubmission(taxFormState: TaxFormState) {
    if (taxFormState.selectedTown.length < 1){
      const ipAddress = publicIp.v4();
      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          targetTown: taxFormState.selectedTown[0],
          income: taxFormState.income,
          numChildren: taxFormState.numChildren,
          married: taxFormState.married,
          doubleSalary: taxFormState.doubleSalary,
          public_ip: ipAddress,
        }),
      };
  
      fetch(
        process.env.REACT_APP_BACKEND_URL + "/tax_calculator/",
        requestOptions
      )
        .then((response) => response.json())
        .then((data) => {
          this.setState({
            targetTownId: JSON.parse(JSON.stringify(taxFormState.selectedTown[0]))["id"],
            targetTownTaxes: data["targetTownTaxAmount"],
            targetTownName: JSON.parse(JSON.stringify(taxFormState.selectedTown[0]))[
              "label"
            ],
            taxData: JSON.stringify(data["taxData"]),
            taxesComputed: true,
          });
        });
    }
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

  reset() {
    this.setState({ taxesComputed: false });
  }

  renderHistogram() {
    if (this.state.taxesComputed) {
      return (
        <div>
          <h4 className="text-light">Switzerland wide comparison:</h4>
          <TaxHistogram
            data={this.state.taxData}
            targetTownId={this.state.targetTownId}
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
          <Col
            xs={{ span: 12, order: 1 }}
            lg={{ span: 8, order: 12 }}
            className="mt-5 mt-lg-0"
          >
            {this.renderTaxes()}
            {this.renderHistogram()}
          </Col>
          <Col
            className="text-light col-lg-pull-8"
            xs={{ span: 12, order: 12 }}
            lg={{ span: 4, order: 1 }}
          >
            <TaxForm
              resetCalculator={this.reset}
              handleTaxFormSubmission={this.handleTaxFormSubmission}
            />
          </Col>
        </Row>
      </Container>
    );
  }
}

export default TaxCalculator;
