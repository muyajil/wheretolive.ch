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
  ValueFormatterParams,
  CellMouseOverEvent,
  CellMouseOutEvent,
} from "ag-grid-community";

interface Props {}

interface State {
  columnDefs: object[];
  searchResultsString: string | null;
  selectedTowns: TownInfo[];
  hoveredTownId: number;
}

class TownsOverview extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    const searchResults = localStorage.getItem("searchResults");
    this.state = {
      columnDefs: [
        { headerName: "Id", field: "sourceTownId", hide: true},
        { headerName: "Zip Code", field: "sourceTownZip" },
        { headerName: "Town", field: "sourceTownName" },
        {
          headerName: "Commute",
          field: "commuteTime",
          valueFormatter: this.timeFormatter,
          sortable: true,
          filter: 'agNumberColumnFilter'
        },
        {
          headerName: "Yearly Cost Health",
          field: "yearlyCostHealth",
          valueFormatter: this.currencyFormatter,
          sortable: true,
          filter: 'agNumberColumnFilter'
        },
        {
          headerName: "Yearly Cost Home",
          field: "yearlyCostHome",
          valueFormatter: this.currencyFormatter,
          sortable: true,
          filter: 'agNumberColumnFilter'
        },
        {
          headerName: "Yearly Cost Taxes",
          field: "yearlyCostTaxes",
          valueFormatter: this.currencyFormatter,
          sortable: true,
          filter: 'agNumberColumnFilter'
        },
        {
          headerName: "Total Yearly Cost",
          field: "yearlyCostTotal",
          valueFormatter: this.currencyFormatter,
          sortable: true,
          filter: 'agNumberColumnFilter'
        },
        {
          headerName: "Migros",
          field: "migros",
          cellRenderer: this.booleanFormatter,
          sortable: true
        },
        {
          headerName: "Coop",
          field: "coop",
          cellRenderer: this.booleanFormatter,
          sortable: true
        },
        {
          headerName: "Aldi",
          field: "aldi",
          cellRenderer: this.booleanFormatter,
          sortable: true
        },
        {
          headerName: "Lidl",
          field: "lidl",
          cellRenderer: this.booleanFormatter,
          sortable: true
        },
      ],
      searchResultsString: searchResults,
      selectedTowns: [],
      hoveredTownId: -1,
    };
    this.dataUpdateHandler = this.dataUpdateHandler.bind(this);
    this.onMouseOutHandler = this.onMouseOutHandler.bind(this);
    this.onMouseOverHandler = this.onMouseOverHandler.bind(this);
    this.firstDataRenderedHandler = this.firstDataRenderedHandler.bind(this);
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

  booleanFormatter(params: ValueFormatterParams) {
    if (params.value) {
      return "&#10004;";
    } else {
      return "&#10006;";
    }
  }

  dataUpdateHandler(event: ModelUpdatedEvent) {
    // eslint-disable-next-line
    const selectedTowns = new Array();
    event.api.forEachNodeAfterFilter((rowNode, index) => {
      selectedTowns.push(rowNode.data);
    });
    this.setState({ selectedTowns: selectedTowns });
  }

  firstDataRenderedHandler(event: FirstDataRenderedEvent){
    event.api.sizeColumnsToFit();
  }

  onMouseOverHandler(event: CellMouseOverEvent){
    this.setState({hoveredTownId: event.data.sourceTownId})
  }

  onMouseOutHandler(event: CellMouseOutEvent){
    this.setState({hoveredTownId: -1})
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
            <TownsHistogram
              selectedTowns={this.state.selectedTowns}
              targetTownId={this.state.hoveredTownId}
            />
          </Col>
          <Col xs={12} lg={6}>
            {this.renderBarPlot()}
          </Col>
        </Row>
        <Row>
          <Col xs={12}>
            <Table
              dataUpdateHandler={this.dataUpdateHandler}
              firstDataRenderedHandler={this.firstDataRenderedHandler}
              onMouseOutHandler={this.onMouseOutHandler}
              onMouseOverHandler={this.onMouseOverHandler}
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
      return this.renderOverview(
        Object.values(JSON.parse(this.state.searchResultsString))
      );
    }
  }
}

export default TownsOverview;
