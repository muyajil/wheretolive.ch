import React from "react";
import Container from "react-bootstrap/Container";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import TaxForm from "./TaxForm";
import TaxHistogram from "./TaxHistogram";

class TaxCalculator extends React.Component {
  handleTaxFormSubmission(
    selectedTown: Object | string,
    income: number,
    numChildren: number,
    married: boolean,
    doubleSalary: boolean
  ) {
    console.log(selectedTown)
    console.log(income)
    console.log(numChildren)
    console.log(married)
    console.log(doubleSalary)
  }

  render() {
    return (
      <Container className="text-light" fluid>
        <Row className="mt-5">
          <Col xs={12} md={4}>
            <TaxForm handleTaxFormSubmission={this.handleTaxFormSubmission} />
          </Col>
          <Col xs={12} md={8}>
            <TaxHistogram />
          </Col>
        </Row>
      </Container>
    );
  }
}

export default TaxCalculator;
