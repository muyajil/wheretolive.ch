import React from "react";
import { AgGridReact } from "ag-grid-react";

import "ag-grid-community/dist/styles/ag-grid.css";
import "ag-grid-community/dist/styles/ag-theme-alpine.css";
import {
  FirstDataRenderedEvent,
  ModelUpdatedEvent,
  CellMouseOutEvent,
  CellMouseOverEvent,
  VirtualColumnsChangedEvent,
  GridReadyEvent,
  RowNode,
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
  onVirtualColumnsChangedHandler: (event: VirtualColumnsChangedEvent) => void;
  onGridReadyHandler: (event: GridReadyEvent) => void;
  isExternalFilterPresent: () => boolean;
  doesExternalFilterPass: (node: RowNode) => boolean;
  width: number;
  displayGrid: boolean;
}

interface State {}
class Table extends React.Component<Props, State> {
  render() {
    return (
      <div
        className={`ag-theme-alpine ${this.props.displayGrid ? "" : "hidden" }`}
        style={{ height: 500, width: "100%", maxWidth: this.props.width}}
      >
        <AgGridReact
          onFirstDataRendered={this.props.firstDataRenderedHandler}
          onModelUpdated={this.props.dataUpdateHandler}
          onCellMouseOut={this.props.onMouseOutHandler}
          onCellMouseOver={this.props.onMouseOverHandler}
          onVirtualColumnsChanged={this.props.onVirtualColumnsChangedHandler}
          isExternalFilterPresent={this.props.isExternalFilterPresent}
          doesExternalFilterPass={this.props.doesExternalFilterPass}
          onGridReady={this.props.onGridReadyHandler}
          columnDefs={this.props.columnDefs}
          rowData={this.props.rowData}
          animateRows={true}
        ></AgGridReact>
      </div>
    );
  }
}

export default Table;
