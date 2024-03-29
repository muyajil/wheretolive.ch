import Form from "react-bootstrap/Form";
import React from "react";
import Col from "react-bootstrap/Col";
import TownTypeahead from "../../Utilities/TownTypeahead";
import {renderMinutes} from "../../Utilities/UtilityFunctions";

interface Props {
  handleChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  handleTypeaheadChange: (selected: Array<Object | string>) => void;
  typeaheadRef: any;
  selectedTown: Array<Object | string>;
  commuteTime: number;
  onlyTrainCommute: boolean;
  typeaheadValid: boolean;
  typeaheadInvalid: boolean;
}

interface State {}

class CommuteInfo extends React.Component<Props, State> {
  render() {
    return (
      <Col xs={12} lg={6} xl={3} className="pl-lg-5 pr-lg-5 border-right-lg">
        <h5>
          <strong>Commute Information:</strong>
        </h5>
        <Form.Group controlId="town">
          <Form.Label>Workplace Town</Form.Label>
          <TownTypeahead // check if value equivalent is offered by typeahead
            onChange={this.props.handleTypeaheadChange}
            selectedTown={this.props.selectedTown}
            typeaheadRef={this.props.typeaheadRef}
            typeaheadInvalid={this.props.typeaheadInvalid}
            typeaheadValid={this.props.typeaheadValid}
          />
        </Form.Group>
        <Form.Group controlId="commuteTime">
          <Form.Label>Maximum Commute Time</Form.Label>
          <p>{renderMinutes(this.props.commuteTime)}</p>
          <Form.Control
            value={this.props.commuteTime}
            onChange={this.props.handleChange}
            min={0}
            max={240}
            step={5}
            type="range"
          />
        </Form.Group>
        <Form.Group controlId="onlyTrainCommute">
          <Form.Check
            checked={this.props.onlyTrainCommute}
            onChange={this.props.handleChange}
            type="switch"
            label="Only consider time spent in train"
          />
        </Form.Group>
      </Col>
    );
  }
}

export default CommuteInfo;
