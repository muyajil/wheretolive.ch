import React from "react";
import { Typeahead } from "react-bootstrap-typeahead";

interface Props {
  onChange: (selected: Array<Object | string>) => void;
  selectedTown: Array<Object | string>;
  typeaheadRef: any;
  typeaheadValid: boolean;
  typeaheadInvalid: boolean;
}

interface State {
  typeaheadData: Map<string, string | number>[];
  onChange: (selected: Array<Object | string>) => void;
}

class TownTypeahead extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { typeaheadData: [], onChange: this.props.onChange };
  }

  componentDidMount() {
    fetch(process.env.REACT_APP_BACKEND_URL + "/towns/typeahead")
      .then((response) => response.json())
      .then((data) => {
        this.setState({ typeaheadData: data });
      });
  }

  render() {
    return (
      <Typeahead
        id="town-typeahead"
        options={this.state.typeaheadData}
        onChange={this.state.onChange}
        inputProps={{ required: true }}
        defaultSelected={this.props.selectedTown}
        flip={true}
        ref={this.props.typeaheadRef}
        clearButton={true}
        minLength={3}
        isValid={this.props.typeaheadValid}
        isInvalid={this.props.typeaheadInvalid}
        selectHintOnEnter={true}
      />
    );
  }
}

export default TownTypeahead;
