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
  VirtualColumnsChangedEvent,
} from "ag-grid-community";
import StackedBarChart from "./StackedBarChart";
import debounce from "lodash.debounce";

interface Props {}

interface State {
  columnDefs: object[];
  searchResultsString: string | null;
  selectedTowns: TownInfo[];
  hoveredTownId: number;
  gridWidth: number;
  displayGrid: boolean;
}

class TownsOverview extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    const searchResults = localStorage.getItem("searchResults");
    this.state = {
      columnDefs: [
        { headerName: "Id", field: "sourceTownId", hide: true },
        { headerName: "Zip Code", field: "sourceTownZip" },
        { headerName: "Town", field: "sourceTownName" },
        {
          headerName: "Commute",
          field: "commuteTime",
          valueFormatter: this.timeFormatter,
          sortable: true,
        },
        {
          headerName: "Yearly Cost Health",
          field: "yearlyCostHealth",
          valueFormatter: this.currencyFormatter,
          sortable: true,
        },
        {
          headerName: "Yearly Cost Home",
          field: "yearlyCostHome",
          valueFormatter: this.currencyFormatter,
          sortable: true,
        },
        {
          headerName: "Yearly Cost Taxes",
          field: "yearlyCostTaxes",
          valueFormatter: this.currencyFormatter,
          sortable: true,
        },
        {
          headerName: "Total Yearly Cost",
          field: "yearlyCostTotal",
          valueFormatter: this.currencyFormatter,
          sortable: true,
        },
        {
          headerName: "Migros",
          field: "migros",
          cellRenderer: this.booleanFormatter,
          sortable: true,
        },
        {
          headerName: "Coop",
          field: "coop",
          cellRenderer: this.booleanFormatter,
          sortable: true,
        },
        {
          headerName: "Aldi",
          field: "aldi",
          cellRenderer: this.booleanFormatter,
          sortable: true,
        },
        {
          headerName: "Lidl",
          field: "lidl",
          cellRenderer: this.booleanFormatter,
          sortable: true,
        },
      ],
      searchResultsString: searchResults,
      selectedTowns: [],
      hoveredTownId: -1,
      gridWidth: 2000,
      displayGrid: false,
    };
    this.dataUpdateHandler = this.dataUpdateHandler.bind(this);
    this.onMouseOutHandler = this.onMouseOutHandler.bind(this);
    this.onMouseOverHandler = this.onMouseOverHandler.bind(this);
    this.firstDataRenderedHandler = this.firstDataRenderedHandler.bind(this);
    this.onVirtualColumnsChangedHandler = this.onVirtualColumnsChangedHandler.bind(this);
  }

  renderBarPlot() {
    if (this.state.selectedTowns.length > 200) {
      return (
        <h4 className="text-light">
          Please filter fewer than 200 towns to display detailed analysis{" "}
        </h4>
      );
    }
    return (
      <StackedBarChart
        data={JSON.parse(JSON.stringify(this.state.selectedTowns))}
        idToMark={this.state.hoveredTownId}
      />
    );
  }

  debounceSetState = debounce((state) => this.setState(state), 50);

  currencyFormatter(params: ValueFormatterParams) {
    return "CHF " + new Intl.NumberFormat("ch").format(params.value);
  }

  timeFormatter(params: ValueFormatterParams) {
    const minutes = Math.floor((params.value / 60) % 60);
    const hours = Math.floor(params.value / 3600);
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
    event.api.forEachNodeAfterFilterAndSort((rowNode, index) => {
      selectedTowns.push(rowNode.data);
    });
    this.setState({ selectedTowns: selectedTowns });
  }

  firstDataRenderedHandler(event: FirstDataRenderedEvent) {
    event.columnApi.autoSizeAllColumns();
    const gridWidth = event.columnApi
      .getAllColumns()
      .filter((col) => col.isVisible())
      .map((col) => col.getActualWidth())
      .reduce((result, num) => result + num) + 20;
    this.setState({gridWidth: gridWidth, displayGrid: true})
  }

  onMouseOverHandler(event: CellMouseOverEvent) {
    this.debounceSetState({ hoveredTownId: event.data.sourceTownId });
  }

  onMouseOutHandler(event: CellMouseOutEvent) {
    this.debounceSetState({ hoveredTownId: -1 });
  }

  onVirtualColumnsChangedHandler(event: VirtualColumnsChangedEvent) {
    debounce(() => event.columnApi.autoSizeAllColumns(), 50)()
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
              onVirtualColumnsChanged={this.onVirtualColumnsChangedHandler}
              rowData={searchResults}
              columnDefs={this.state.columnDefs}
              width={this.state.gridWidth}
              displayGrid={this.state.displayGrid}
            />
          </Col>
        </Row>
        <Row>
          <Col xs={12} className="text-center pt-5">
            <LinkContainer to="/accomodation">
              <Button variant="primary">
                Browse Apartements in this selection!
              </Button>
            </LinkContainer>
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
