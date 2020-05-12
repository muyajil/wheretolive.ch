import React from "react";
import { Typeahead } from "react-bootstrap-typeahead";

interface Props {
    onChange: (selected: Array<Object|string>) => void;
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
    fetch("http://localhost:5000/towns/typeahead")
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
      />
    );
  }
}

export default TownTypeahead;