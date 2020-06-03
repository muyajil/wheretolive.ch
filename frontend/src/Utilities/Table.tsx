import React from "react";
import { AgGridReact } from 'ag-grid-react';

import 'ag-grid-community/dist/styles/ag-grid.css';
import 'ag-grid-community/dist/styles/ag-theme-alpine.css';

interface Props{
    rowData: object[];
    columnDefs: object[];
}

interface State{}

class Table extends React.Component<Props, State>{
    render () {
        return (
            <div className="ag-theme-alpine mx-auto" style={ {height: '500px', width: '90%'} }>
              <AgGridReact
                  columnDefs={this.props.columnDefs}
                  rowData={this.props.rowData}>
              </AgGridReact>
            </div>
          );
    }
}

export default Table;