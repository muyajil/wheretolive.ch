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
  GridReadyEvent,
  RowNode,
  GridApi,
} from "ag-grid-community";
import StackedBarChart from "./StackedBarChart";
import debounce from "lodash.debounce";
import TownsOverviewFilter from "./TownsOverviewFilter";

interface Props {}

interface NumberFilter {
  [key: string]: number;
}

interface BooleanFilter {
  [key: string]: boolean;
}

interface State {
  columnDefs: object[];
  searchResultsString: string | null;
  selectedTowns: TownInfo[];
  hoveredTownId: number;
  gridWidth: number;
  displayGrid: boolean;
  booleanFilters: BooleanFilter;
  numberFilters: NumberFilter;
}

class TownsOverview extends React.Component<Props, State> {
  private gridApi?: GridApi;
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
          hide: true,
        },
        {
          headerName: "Yearly Cost Home",
          field: "yearlyCostHome",
          valueFormatter: this.currencyFormatter,
          sortable: true,
          hide: true,
        },
        {
          headerName: "Yearly Cost Taxes",
          field: "yearlyCostTaxes",
          valueFormatter: this.currencyFormatter,
          sortable: true,
          hide: true,
        },
        {
          headerName: "Total Yearly Cost",
          field: "yearlyCostTotal",
          valueFormatter: this.currencyFormatter,
          sortable: true,
        },
        {
          headerName: "Total Montly Cost",
          field: "monthlyCostTotal",
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
      booleanFilters: {},
      numberFilters: {},
    };
    this.dataUpdateHandler = this.dataUpdateHandler.bind(this);
    this.onMouseOutHandler = this.onMouseOutHandler.bind(this);
    this.onMouseOverHandler = this.onMouseOverHandler.bind(this);
    this.firstDataRenderedHandler = this.firstDataRenderedHandler.bind(this);
    this.onVirtualColumnsChangedHandler = this.onVirtualColumnsChangedHandler.bind(
      this
    );
    this.onGridReadyHandler = this.onGridReadyHandler.bind(this);
    this.handleFilterChange = this.handleFilterChange.bind(this);
    this.doesExternalFilterPass = this.doesExternalFilterPass.bind(this);
    this.isExternalFilterPresent = this.isExternalFilterPresent.bind(this);
  }

  renderBarPlot() {
    if (this.state.selectedTowns.length > 200) {
      return (
        <h5 className="text-muted">
          Please filter fewer than 200 towns to display detailed analysis{" "}
        </h5>
      );
    }
    return (
      <StackedBarChart
        data={JSON.parse(JSON.stringify(this.state.selectedTowns))}
        idToMark={this.state.hoveredTownId}
      />
    );
  }

  debounceSetState = debounce((state) => this.setState(state), 100);

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
    this.debounceSetState({ selectedTowns: selectedTowns });
  }

  firstDataRenderedHandler(event: FirstDataRenderedEvent) {
    event.columnApi.autoSizeAllColumns();
    const gridWidth =
      event.columnApi
        .getAllColumns()
        .filter((col) => col.isVisible())
        .map((col) => col.getActualWidth())
        .reduce((result, num) => result + num) + 45;
    event.api.setSortModel([{ colId: "yearlyCostTotal", sort: "asc" }]);
    this.setState({ gridWidth: gridWidth, displayGrid: true });
  }

  onGridReadyHandler(event: GridReadyEvent) {
    this.gridApi = event.api;
  }

  onMouseOverHandler(event: CellMouseOverEvent) {
    this.debounceSetState({ hoveredTownId: event.data.sourceTownId });
  }

  onMouseOutHandler(event: CellMouseOutEvent) {
    this.debounceSetState({ hoveredTownId: -1 });
  }

  onVirtualColumnsChangedHandler(event: VirtualColumnsChangedEvent) {
    debounce(() => event.columnApi.autoSizeAllColumns(), 50)();
  }

  handleFilterChange(event: React.ChangeEvent<HTMLInputElement>) {
    const target = event.target.id;
    if (
      target === "migros" ||
      target === "coop" ||
      target === "lidl" ||
      target === "aldi"
    ) {
      const currentFilters = this.state.booleanFilters;
      currentFilters[target] = event.target.checked;
      this.debounceSetState({ booleanFilters: currentFilters });
    } else {
      const currentFilters = this.state.numberFilters;
      currentFilters[target] = Number.parseInt(event.target.value);
      this.debounceSetState({ numberFilters: currentFilters });
    }
    this.gridApi?.onFilterChanged();
  }

  isExternalFilterPresent() {
    return (
      Object.keys(this.state.booleanFilters).length > 0 ||
      Object.keys(this.state.numberFilters).length > 0
    );
  }

  doesExternalFilterPass(node: RowNode) {
    let pass = true;
    const booleanKeys = Object.keys(this.state.booleanFilters);
    for (let idx = 0; idx < booleanKeys.length; idx++) {
      if (this.state.booleanFilters[booleanKeys[idx]]) {
        pass = pass && node.data[booleanKeys[idx]];
      }
    }
    const numberKeys = Object.keys(this.state.numberFilters);
    for (let idx = 0; idx < numberKeys.length; idx++) {
      switch (numberKeys[idx]) {
        case "maxCommute":
          pass =
            pass &&
            this.state.numberFilters[numberKeys[idx]] * 60 >=
              node.data["commuteTime"];
          break;
        case "minCommute":
          pass =
            pass &&
            this.state.numberFilters[numberKeys[idx]] * 60 <=
              node.data["commuteTime"];
          break;
        case "maxTotalYearly":
          pass =
            pass &&
            this.state.numberFilters[numberKeys[idx]] >=
              node.data["yearlyCostTotal"];
          break;
        case "minTotalYearly":
          pass =
            pass &&
            this.state.numberFilters[numberKeys[idx]] <=
              node.data["yearlyCostTotal"];
          break;
        case "minTotalMonthly":
          pass =
            pass &&
            this.state.numberFilters[numberKeys[idx]] <=
              node.data["monthlyCostTotal"];
          break;
        case "maxTotalMonthly":
          pass =
            pass &&
            this.state.numberFilters[numberKeys[idx]] >=
              node.data["monthlyCostTotal"];
          break;
        default:
      }
    }
    return pass;
  }

  renderOverview(searchResults: TownInfo[]) {
    return (
      <div>
        <Row>
          <Col xs={6}>
            <LinkContainer to="/search">
              <Button variant="primary">&#10094; Change search</Button>
            </LinkContainer>
          </Col>
          <Col xs={6} className="ml-auto text-right">
            <LinkContainer to="/search/accomodations">
              <Button variant="primary">Accomodations &#10095;</Button>
            </LinkContainer>
          </Col>
        </Row>
        <Row className="mt-2">
          <Col xs={12} lg={6}>
            <h4 className="text-light">Distribution of Total Cost of Living</h4>
            <TownsHistogram
              selectedTowns={this.state.selectedTowns}
              targetTownId={this.state.hoveredTownId}
            />
          </Col>
          <Col xs={12} lg={6} className="mt-2 mt-lg-0">
            <h4 className="text-light">Total Cost of Living per Town</h4>
            {this.renderBarPlot()}
          </Col>
        </Row>
        <Row>
          <Col xs={12}>
          <h4 className="text-light">
            {this.state.selectedTowns.length} towns in selection
          </h4>
          </Col>
        </Row>
        <Row>
          <Col xs={12} lg={4} className="mt-2 d-flex justify-content-center">
            <TownsOverviewFilter
              handleChange={this.handleFilterChange}
              booleanFilters={this.state.booleanFilters}
              numberFilters={this.state.numberFilters}
              maxCommute={Math.max(
                ...searchResults.map((townInfo) =>
                  Math.floor(townInfo.commuteTime / 60)
                )
              )}
              maxYearly={Math.max(
                ...searchResults.map((townInfo) =>
                  Math.floor(townInfo.yearlyCostTotal)
                )
              )}
              maxMonthly={Math.max(
                ...searchResults.map((townInfo) =>
                  Math.floor(townInfo.monthlyCostTotal)
                )
              )}
            />
          </Col>
          <Col xs={12} lg={8} className="mt-2 d-flex justify-content-center">
            <Table
              dataUpdateHandler={this.dataUpdateHandler}
              firstDataRenderedHandler={this.firstDataRenderedHandler}
              onMouseOutHandler={this.onMouseOutHandler}
              onMouseOverHandler={this.onMouseOverHandler}
              onVirtualColumnsChangedHandler={
                this.onVirtualColumnsChangedHandler
              }
              onGridReadyHandler={this.onGridReadyHandler}
              isExternalFilterPresent={this.isExternalFilterPresent}
              doesExternalFilterPass={this.doesExternalFilterPass}
              rowData={searchResults}
              columnDefs={this.state.columnDefs}
              width={this.state.gridWidth}
              displayGrid={this.state.displayGrid}
            />
          </Col>
        </Row>
        {/* <Row>
          <Col xs={12} className="text-center pt-4">
            <LinkContainer to="/accomodation">
              <Button variant="primary">
                Browse Apartements in this selection!
              </Button>
            </LinkContainer>
          </Col>
        </Row> */}
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
