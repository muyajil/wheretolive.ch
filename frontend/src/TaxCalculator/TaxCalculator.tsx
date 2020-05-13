import React from "react";
import Container from "react-bootstrap/Container";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import TaxForm from "./TaxForm";
import TaxHistogram from "./TaxHistogram";

interface Props {}

interface State {
  targetTownIdx: number;
  targetTownTaxes: number;
  targetTownName: string;
  taxesComputed: boolean;
  figureData: string;
}

class TaxCalculator extends React.Component<Props, State> {
  constructor (props: Props){
    super(props)
    this.state = {
      targetTownIdx: -1,
      targetTownTaxes: 0,
      targetTownName: '',
      taxesComputed: false,
      figureData: ''
    }
    this.handleTaxFormSubmission = this.handleTaxFormSubmission.bind(this)
  }

  handleTaxFormSubmission(
    selectedTown: Object | string,
    income: number,
    numChildren: number,
    married: boolean,
    doubleSalary: boolean
  ) {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        targetTown: selectedTown,
        income: income,
        numChildren: numChildren,
        married: married,
        doubleSalary: doubleSalary,
      }),
    };

    fetch("http://localhost:5000/tax_calculator/", requestOptions)
      .then((response) => response.json())
      .then((data) => {
        this.setState({
          targetTownIdx: data["target_town_idx"],
          targetTownTaxes: data["target_town_taxes"],
          targetTownName: data["target_town_name"],
          figureData: data["figure_data"],
          taxesComputed: true
        });
        console.log(data["figure_data"])
      });
  }

  renderTaxes () {
    if (this.state.taxesComputed) {
      return (<h3 className="text-light">Taxes for {this.state.targetTownName}: {new Intl.NumberFormat('ch').format(this.state.targetTownTaxes)}.- </h3>);
    }
  }

  renderHistogram () {
    if (this.state.taxesComputed) {
      return <TaxHistogram data={JSON.parse(this.state.figureData)} targetTownIdx={this.state.targetTownIdx} />
    }
  }

  render() {
    return (
      <Container fluid>
        <Row className="mt-5 max-h-500">
          <Col className="text-light" xs={12} md={4}>
            <TaxForm handleTaxFormSubmission={this.handleTaxFormSubmission} />
          </Col>
          <Col xs={12} md={8}>
            {this.renderTaxes()}
            {this.renderHistogram()}
          </Col>
        </Row>
      </Container>
    );
  }
}

export default TaxCalculator;
