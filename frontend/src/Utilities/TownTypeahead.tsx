import React from "react";
import { Typeahead } from "react-bootstrap-typeahead";

interface Props {
    onChange: (selected: Array<Object|string>) => void;
    selectedTown: Array<Object|string>;
}

interface State {
  typeaheadData: Map<string, string|number>[];
  onChange: (selected: Array<Object|string>) => void;
}

class TownTypeahead extends React.Component<Props, State> {

  constructor(props: Props) {
      super(props);
      this.state = {typeaheadData: [], onChange: this.props.onChange}
  }

  componentDidMount() {
    fetch(process.env.REACT_APP_BACKEND_PROTOCOL + "://" + process.env.REACT_APP_BACKEND_HOST +":" + process.env.REACT_APP_BACKEND_PORT +"/towns/typeahead")
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
        placeholder="Choose a town"
        onChange={this.state.onChange}
        inputProps={{required: true}}
        defaultSelected={this.props.selectedTown}
      />
    );
  }
}

export default TownTypeahead;