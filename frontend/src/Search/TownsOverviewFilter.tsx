import Form from "react-bootstrap/Form";
import React from "react";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import { renderMinutes } from "../Utilities/UtilityFunctions";

interface BooleanFilter {
  [key: string]: boolean;
}

interface NumberFilter {
  [key: string]: number;
}

interface Props {
  handleChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  // handleRangeChange: (state: any) => void;
  booleanFilters: BooleanFilter;
  numberFilters: NumberFilter;
  maxCommute: number;
  maxYearly: number;
  maxMonthly: number;
}

interface State {}

class TownsOverviewFilter extends React.Component<Props, State> {
  renderNumber(number: number) {
    return new Intl.NumberFormat("ch").format(number);
  }

  render() {
    return (
      <div className="flex-fill bg-light px-4 pt-4 rounded">
        <Row>
          <Col>
            <p>
              <strong>Filters:</strong>
            </p>
          </Col>
        </Row>
        <Form.Row>
          <Col>
            <Form.Group controlId="minCommute">
              <Form.Label>Min Commute</Form.Label>
              <p>
                {renderMinutes(
                  this.props.numberFilters["minCommute"]
                    ? this.props.numberFilters["minCommute"]
                    : 0
                )}
              </p>
              <Form.Control
                value={this.props.numberFilters["minCommute"]}
                onChange={this.props.handleChange}
                min={0}
                max={(Math.floor(this.props.maxCommute/5) + 1)*5}
                defaultValue={0}
                step={5}
                type="range"
              />
            </Form.Group>
          </Col>
          <Col>
            <Form.Group controlId="maxCommute">
              <Form.Label>Max Commute</Form.Label>
              <p>
                {renderMinutes(
                  this.props.numberFilters["maxCommute"]
                    ? this.props.numberFilters["maxCommute"]
                    : this.props.maxCommute
                )}
              </p>
              <Form.Control
                value={this.props.numberFilters["maxCommute"]}
                onChange={this.props.handleChange}
                min={0}
                max={(Math.floor(this.props.maxCommute/5) + 1)*5}
                defaultValue={this.props.maxCommute}
                step={5}
                type="range"
              />
            </Form.Group>
          </Col>
        </Form.Row>
        {/* <Row>
          <Col>
            <p>
              <strong>Cost Filters:</strong>
            </p>
          </Col>
        </Row> */}
        <Form.Row>
          <Col>
            <Form.Group controlId="minTotalYearly">
              <Form.Label>Min CHF per Year</Form.Label>
              <p>
                CHF{" "}
                {this.renderNumber(
                  this.props.numberFilters["minTotalYearly"]
                    ? this.props.numberFilters["minTotalYearly"]
                    : 0
                )}
              </p>
              <Form.Control
                value={this.props.numberFilters["minTotalYearly"]}
                onChange={this.props.handleChange}
                min={0}
                max={(Math.floor(this.props.maxYearly/500) + 1)*500}
                defaultValue={0}
                step={500}
                type="range"
              />
            </Form.Group>
          </Col>
          <Col>
            <Form.Group controlId="maxTotalYearly">
              <Form.Label>Max CHF per Year</Form.Label>
              <p>
                CHF{" "}
                {this.renderNumber(
                  this.props.numberFilters["maxTotalYearly"]
                    ? this.props.numberFilters["maxTotalYearly"]
                    : this.props.maxYearly
                )}
              </p>
              <Form.Control
                value={this.props.numberFilters["maxTotalYearly"]}
                onChange={this.props.handleChange}
                min={0}
                max={(Math.floor(this.props.maxYearly/500) + 1)*500}
                defaultValue={this.props.maxYearly}
                step={500}
                type="range"
              />
            </Form.Group>
          </Col>
        </Form.Row>
        <Form.Row>
          <Col>
            <Form.Group controlId="minTotalMonthly">
              <Form.Label>Min CHF per Month</Form.Label>
              <p>
                CHF{" "}
                {this.renderNumber(
                  this.props.numberFilters["minTotalMonthly"]
                    ? this.props.numberFilters["minTotalMonthly"]
                    : 0
                )}
              </p>
              <Form.Control
                value={this.props.numberFilters["minTotalMonthly"]}
                onChange={this.props.handleChange}
                min={0}
                max={(Math.floor(this.props.maxMonthly/500) + 1)*500}
                defaultValue={0}
                step={500}
                type="range"
              />
            </Form.Group>
          </Col>
          <Col>
            <Form.Group controlId="maxTotalMonthly">
              <Form.Label>Max CHF per Month</Form.Label>
              <p>
                CHF{" "}
                {this.renderNumber(
                  this.props.numberFilters["maxTotalMonthly"]
                    ? this.props.numberFilters["maxTotalMonthly"]
                    : this.props.maxMonthly
                )}
              </p>
              <Form.Control
                value={this.props.numberFilters["maxTotalMonthly"]}
                onChange={this.props.handleChange}
                min={0}
                max={(Math.floor(this.props.maxMonthly/500) + 1)*500}
                defaultValue={this.props.maxMonthly}
                step={500}
                type="range"
              />
            </Form.Group>
          </Col>
        </Form.Row>
        {/* <Row>
          <Col>
            <p>
              <strong>Shopping Filters:</strong>
            </p>
          </Col>
        </Row> */}
        <Form.Row className="mt-4 ml-2">
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
