import React from "react";
import { AgGridReact } from "ag-grid-react";

import "ag-grid-community/dist/styles/ag-grid.css";
import "ag-grid-community/dist/styles/ag-theme-alpine.css";
import {
  FirstDataRenderedEvent,
  ModelUpdatedEvent,
  CellMouseOutEvent,
  CellMouseOverEvent,
} from "ag-grid-community";

interface Props {
  rowData: object[];
  columnDefs: object[];
  dataUpdateHandler: (
    event: ModelUpdatedEvent
  ) => void;
  firstDataRenderedHandler: (event: FirstDataRenderedEvent) => void;
  onMouseOutHandler: (event: CellMouseOutEvent) => void;
  onMouseOverHandler: (event: CellMouseOverEvent) => void;
}

interface State {}
// TODO: Function to get selected rows
// TODO: Allow certain filters and sorting
// TODO: Function to get the hovered item
class Table extends React.Component<Props, State> {
  render() {
    return (
      <div
        className="ag-theme-alpine mx-auto"
        style={{ height: "500px", width: "100%"}}
      >
        <AgGridReact
          onFirstDataRendered={this.props.firstDataRenderedHandler}
          onModelUpdated={this.props.dataUpdateHandler}
          onCellMouseOut={this.props.onMouseOutHandler}
          onCellMouseOver={this.props.onMouseOverHandler}
          columnDefs={this.props.columnDefs}
          rowData={this.props.rowData}
          animateRows={true}
        ></AgGridReact>
      </div>
    );
  }
}

export default Table;
