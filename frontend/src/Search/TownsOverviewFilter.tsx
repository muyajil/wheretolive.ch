import Form from "react-bootstrap/Form";
import React from "react";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import {renderMinutes} from "../Utilities/UtilityFunctions";

interface BooleanFilter {
  [key: string]: boolean;
}

interface NumberFilter {
  [key: string]: number;
}

interface Props {
  handleChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  booleanFilters: BooleanFilter;
  numberFilters: NumberFilter;
  maxCommute: number;
}

interface State {}

class TownsOverviewFilter extends React.Component<Props, State> {
  render() {
    return (
      <div className="text-light">
        <Row>
          <p>
            <strong>Commute Filter:</strong>
          </p>
        </Row>
        <Form.Row>
          <Col>
            <Form.Group controlId="maxCommute">
              <Form.Label>Max Commute</Form.Label>
              <p>{renderMinutes(this.props.numberFilters["maxCommute"] ? this.props.numberFilters["maxCommute"] : this.props.maxCommute)}</p>
              <Form.Control
                value={this.props.numberFilters["maxCommute"]}
                onChange={this.props.handleChange}
                min={0}
                max={this.props.maxCommute}
                defaultValue={this.props.maxCommute}
                step={5}
                type="range"
              />
            </Form.Group>
          </Col>
        </Form.Row>
        <Row>
          <p>
            <strong>Cost Filters:</strong>
          </p>
        </Row>
        <Form.Row>
          <Col>
            <Form.Group controlId="minTotalYearly">
              <Form.Label>Min CHF per Year</Form.Label>
              <Form.Control
                value={this.props.numberFilters["minTotalYearly"]}
                onChange={this.props.handleChange}
                type="number"
              />
            </Form.Group>
          </Col>
          <Col>
            <Form.Group controlId="maxTotalYearly">
              <Form.Label>Max CHF per Year</Form.Label>
              <Form.Control
                value={this.props.numberFilters["maxTotalYearly"]}
                onChange={this.props.handleChange}
                type="number"
              />
            </Form.Group>
          </Col>
        </Form.Row>
        <Form.Row>
          <Col>
            <Form.Group controlId="minTotalMonthly">
              <Form.Label>Min CHF per Month</Form.Label>
              <Form.Control
                value={this.props.numberFilters["minTotalMonthly"]}
                onChange={this.props.handleChange}
                type="number"
              />
            </Form.Group>
          </Col>
          <Col>
            <Form.Group controlId="maxTotalMonthly">
              <Form.Label>Max CHF per Month</Form.Label>
              <Form.Control
                value={this.props.numberFilters["maxTotalMonthly"]}
                onChange={this.props.handleChange}
                type="number"
              />
            </Form.Group>
          </Col>
        </Form.Row>
        <Row>
          <p>
            <strong>Shopping Filters:</strong>
          </p>
        </Row>
        <Form.Row>
          <Form.Group className="mr-4" controlId="migros">
            <Form.Check
              inline
              checked={this.props.booleanFilters["migros"]}
              onChange={this.props.handleChange}
              type="checkbox"
            />
            <Form.Label>Migros</Form.Label>
          </Form.Group>
          <Form.Group className="mr-4" controlId="coop">
            <Form.Check
              inline
              checked={this.props.booleanFilters["coop"]}
              onChange={this.props.handleChange}
              type="checkbox"
            />
            <Form.Label>Coop</Form.Label>
          </Form.Group>
          <Form.Group className="mr-4" controlId="aldi">
            <Form.Check
              inline
              checked={this.props.booleanFilters["aldi"]}
              onChange={this.props.handleChange}
              type="checkbox"
            />
            <Form.Label>Aldi</Form.Label>
          </Form.Group>
          <Form.Group controlId="lidl">
            <Form.Check
              inline
              checked={this.props.booleanFilters["lidl"]}
              onChange={this.props.handleChange}
              type="checkbox"
            />
            <Form.Label>Lidl</Form.Label>
          </Form.Group>
        </Form.Row>
      </div>
    );
  }
}

export default TownsOverviewFilter;
