import React, { Ref } from "react";
import { AgGridReact } from "ag-grid-react";

import "ag-grid-community/dist/styles/ag-grid.css";
import "ag-grid-community/dist/styles/ag-theme-alpine.css";
import {
  FirstDataRenderedEvent,
  ModelUpdatedEvent,
  GridReadyEvent,
} from "ag-grid-community";

interface Props {
  rowData: object[];
  columnDefs: object[];
  dataUpdateHandler: (
    event: FirstDataRenderedEvent | ModelUpdatedEvent
  ) => void;
  gridReadyHandler: (event: GridReadyEvent) => void;
}

interface State {}
// TODO: Function to get selected rows
// TODO: Allow certain filters and sorting
// TODO: Function to get the hovered item
class Table extends React.Component<Props, State> {
  render() {
    return (
      <div
        className="ag-theme-alpine-dark mx-auto"
        style={{ height: "500px", width: "100%" }}
      >
        <AgGridReact
          onFirstDataRendered={this.props.dataUpdateHandler}
          onModelUpdated={this.props.dataUpdateHandler}
          onGridReady={this.props.gridReadyHandler}
          columnDefs={this.props.columnDefs}
          rowData={this.props.rowData}
        ></AgGridReact>
      </div>
    );
  }
}

export default Table;
