import React from "react";
import Table from "../Utilities/Table";
import TownsHistogram from "./TownsHistogram";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import { Redirect } from "react-router-dom";
import Button from "react-bootstrap/Button";
import { LinkContainer } from "react-router-bootstrap";
import TownInfo from "./TownInfo";
import {
  ModelUpdatedEvent,
  FirstDataRenderedEvent,
  GridReadyEvent,
  ValueFormatterParams,
} from "ag-grid-community";

interface Props {
}

interface State {
  columnDefs: object[];
  searchResultsString: string | null;
  selectedTowns: TownInfo[];
}

class TownsOverview extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    const searchResults = localStorage.getItem("searchResults");
    this.state = {
      columnDefs: [
        { headerName: "Zip Code", field: "sourceTownZip" },
        { headerName: "Town", field: "sourceTownName" },
        {
          headerName: "Commute",
          field: "commuteTime",
          valueFormatter: this.timeFormatter,
        },
        {
          headerName: "Yearly Cost Health",
          field: "yearlyCostHealth",
          valueFormatter: this.currencyFormatter,
        },
        {
          headerName: "Yearly Cost Home",
          field: "yearlyCostHome",
          valueFormatter: this.currencyFormatter,
        },
        {
          headerName: "Yearly Cost Taxes",
          field: "yearlyCostTaxes",
          valueFormatter: this.currencyFormatter,
        },
        {
          headerName: "Total Yearly Cost",
          field: "yearlyCostTotal",
          valueFormatter: this.currencyFormatter,
        },
        { headerName: "Migros", field: "migros" },
        { headerName: "Coop", field: "coop" },
        { headerName: "Aldi", field: "aldi" },
        { headerName: "Lidl", field: "lidl" },
      ],
      searchResultsString: searchResults,
      selectedTowns: []
    };
    this.dataUpdateHandler = this.dataUpdateHandler.bind(this);
    this.gridReadyHandler = this.gridReadyHandler.bind(this);
  }

  renderBarPlot() {
    return (
      <h3 className="text-center text-light mt-5">
        Select less than 50 towns to display detailed data.
      </h3>
    );
  }

  currencyFormatter(params: ValueFormatterParams) {
    return "CHF " + new Intl.NumberFormat("ch").format(params.value);
  }

  timeFormatter(params: ValueFormatterParams) {
    const minutes = Math.floor(params.value / 60);
    const hours = Math.floor(minutes / 60);
    return ("0" + hours).slice(-2) + ":" + ("0" + minutes).slice(-2) + " h";
  }

  dataUpdateHandler(event: FirstDataRenderedEvent | ModelUpdatedEvent) {
    const selectedTowns = new Array();
    event.api.forEachNodeAfterFilter((rowNode, index) => {
      selectedTowns.push(rowNode.data)
    })
    this.setState({selectedTowns: selectedTowns});
  }

  gridReadyHandler(event: GridReadyEvent) {
    event.api.sizeColumnsToFit();
  }

  renderOverview(searchResults: TownInfo[]) {
    return (
      <div>
        <Row>
          <Col xs={12}>
            <LinkContainer to="/search">
              <Button variant="link">&#10094; Change search</Button>
            </LinkContainer>
          </Col>
        </Row>
        <Row>
          <Col xs={12} lg={6}>
            <TownsHistogram selectedTowns={this.state.selectedTowns} targetTownId={1} />
          </Col>
          <Col xs={12} lg={6}>
            {this.renderBarPlot()}
          </Col>
        </Row>
        <Row>
          <Col xs={12}>
            <Table
              dataUpdateHandler={this.dataUpdateHandler}
              gridReadyHandler={this.gridReadyHandler}
              rowData={searchResults}
              columnDefs={this.state.columnDefs}
            />
          </Col>
        </Row>
      </div>
    );
  }

  render() {
    if (this.state.searchResultsString === null) {
      return <Redirect to="/search" />;
    } else {
      return this.renderOverview(Object.values(JSON.parse(this.state.searchResultsString)));
    }
  }
}

export default TownsOverview;
