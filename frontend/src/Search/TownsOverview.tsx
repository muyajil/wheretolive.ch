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
  ColumnApi,
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
  searchResults: TownInfo[];
  selectedTowns: TownInfo[];
  hoveredTownId: number;
  gridWidth: number;
  displayGrid: boolean;
  divKey: number;
}

function renderTime(seconds: number){
  const minutes = Math.floor((seconds / 60) % 60);
  const hours = Math.floor(seconds / 3600);
  return ("0" + hours).slice(-2) + ":" + ("0" + minutes).slice(-2) + " h";
}

class TownsOverview extends React.Component<Props, State> {
  private gridApi?: GridApi;
  private columnApi?: ColumnApi;
  private booleanFilters: BooleanFilter;
  private numberFilters: NumberFilter;
  private monthlySwitch: boolean;
  private maxTotalYearly: number;
  private maxTotalMonthly: number;
  private maxCommute: number;
  private hoverAllowed: boolean;
  private searchFormState: any;
  constructor(props: Props) {
    super(props);
    this.hoverAllowed = false;
    const searchFormStateString = localStorage.getItem("searchFormState");
    this.searchFormState = searchFormStateString
      ? JSON.parse(searchFormStateString)
      : {};
    const searchResultString = localStorage.getItem("searchResults");
    let searchResults;
    const booleanFilters = localStorage.getItem("booleanFilters");
    const numberFilters = localStorage.getItem("numberFilters");
    const monthlySwitch = localStorage.getItem("monthlySwitch");

    this.maxCommute = 0;
    this.maxTotalMonthly = 0;
    this.maxTotalYearly = 0;

    this.numberFilters = {};
    this.booleanFilters = {};
    this.monthlySwitch = monthlySwitch === "true";
    if (searchResultString) {
      searchResults = JSON.parse(searchResultString);
      this.numberFilters["maxTotalYearly"] = Math.max(
        ...searchResults.map((townInfo: TownInfo) =>
          Math.floor(townInfo.yearlyCostTotal)
        )
      );
      this.maxTotalYearly = this.numberFilters["maxTotalYearly"];
      this.numberFilters["minTotalYearly"] = 0;
      this.numberFilters["maxCommute"] = this.searchFormState["commuteTime"]
      this.maxCommute = this.numberFilters["maxCommute"];
      this.numberFilters["minCommute"] = 0;
      this.numberFilters["maxTotalMonthly"] = Math.max(
        ...searchResults.map((townInfo: TownInfo) =>
          Math.floor(townInfo.monthlyCostTotal)
        )
      );
      this.maxTotalMonthly = this.numberFilters["maxTotalMonthly"];
      this.numberFilters["minTotalMonthly"] = 0;

      if (booleanFilters && booleanFilters !== "") {
        this.booleanFilters = JSON.parse(booleanFilters);
      }
      if (numberFilters && numberFilters !== "") {
        this.numberFilters = {
          ...this.numberFilters,
          ...JSON.parse(numberFilters),
        };
      }
    }

    this.state = {
      columnDefs: [
        { headerName: "Id", field: "sourceTownId", hide: true },
        { headerName: "Zip Code", field: "sourceTownZip", sortable: true },
        { headerName: "Town", field: "sourceTownName", sortable: true },
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
          headerName: "Monthly Cost Health",
          field: "monthlyCostHealth",
          valueFormatter: this.currencyFormatter,
          sortable: true,
          hide: true,
        },
        {
          headerName: "Monthly Cost Home",
          field: "yearlyCostHome",
          valueFormatter: this.currencyFormatter,
          sortable: true,
          hide: true,
        },
        {
          headerName: "Monthly Cost Taxes",
          field: "monthlyCostTaxes",
          valueFormatter: this.currencyFormatter,
          sortable: true,
          hide: true,
        },
        {
          headerName: "Total Yearly Cost",
          field: "yearlyCostTotal",
          valueFormatter: this.currencyFormatter,
          sortable: true,
          hide: this.monthlySwitch,
        },
        {
          headerName: "Total Monthly Cost",
          field: "monthlyCostTotal",
          valueFormatter: this.currencyFormatter,
          sortable: true,
          hide: !this.monthlySwitch,
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
      searchResults: searchResults,
      selectedTowns: [],
      hoveredTownId: -1,
      gridWidth: 2000,
      displayGrid: false,
      divKey: Date.now(),
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
    this.resetFilters = this.resetFilters.bind(this);
  }

  resetFilters() {
    this.numberFilters = {
      maxTotalYearly: this.maxTotalYearly,
      minTotalYearly: 0,
      maxTotalMonthly: this.maxTotalMonthly,
      minTotalMonthly: 0,
      maxCommute: this.maxCommute,
      minCommute: 0,
    };
    this.booleanFilters = {};
    this.setState({
      divKey: Date.now(),
    });
    this.gridApi?.onFilterChanged();
  }

  renderBarPlot() {
    if (this.state.selectedTowns.length > 200) {
      return (
        <h5 className="text-muted">
          Details can only be shown for fewer than 200 towns.{" "}
        </h5>
      );
    }
    return (
      <StackedBarChart
        data={JSON.parse(JSON.stringify(this.state.selectedTowns))}
        idToMark={this.state.hoveredTownId}
        monthlySwitch={this.monthlySwitch}
      />
    );
  }

  debounceSetState = debounce((state) => this.setState(state), 100);

  currencyFormatter(params: ValueFormatterParams) {
    return "CHF " + new Intl.NumberFormat("ch").format(params.value);
  }

  timeFormatter(params: ValueFormatterParams) {
    return renderTime(params.value);
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
        .reduce((result, num) => result + num) + 30;
    this.gridApi?.onFilterChanged();
    this.setState({ gridWidth: gridWidth, displayGrid: true });
  }

  onGridReadyHandler(event: GridReadyEvent) {
    this.gridApi = event.api;
    this.columnApi = event.columnApi;
  }

  onMouseOverHandler(event: CellMouseOverEvent) {
    if (this.hoverAllowed) {
      this.debounceSetState({ hoveredTownId: event.data.sourceTownId });
    }
  }

  onMouseOutHandler(event: CellMouseOutEvent) {
    if (this.hoverAllowed) {
      this.debounceSetState({ hoveredTownId: -1 });
    }
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
      this.booleanFilters[target] = event.target.checked;
      localStorage.setItem(
        "booleanFilters",
        JSON.stringify(this.booleanFilters)
      );
      this.debounceSetState({
        divKey: Date.now(),
      });
    } else if (target === "monthlySwitch") {
      this.monthlySwitch = event.target.checked;
      localStorage.setItem("monthlySwitch", String(this.monthlySwitch));
    } else {
      this.numberFilters[target] = Number.parseInt(event.target.value);
      localStorage.setItem("numberFilters", JSON.stringify(this.numberFilters));
      this.debounceSetState({
        divKey: Date.now(),
      });
    }
    if (event.target.id === "monthlySwitch") {
      if (event.target.checked) {
        this.numberFilters["maxTotalMonthly"] = Math.floor(
          this.numberFilters["maxTotalYearly"] / 12
        );
      } else {
        this.numberFilters["maxTotalYearly"] = Math.floor(
          this.numberFilters["maxTotalMonthly"] * 12
        );
      }
      this.columnApi?.hideColumn("yearlyCostTotal", event.target.checked);
      this.columnApi?.hideColumn("monthlyCostTotal", !event.target.checked);
      this.columnApi?.autoSizeAllColumns();
    }
    this.gridApi?.onFilterChanged();
  }

  isExternalFilterPresent() {
    return (
      Object.keys(this.booleanFilters).length > 0 ||
      Object.keys(this.numberFilters).length > 0
    );
  }

  doesExternalFilterPass(node: RowNode) {
    let pass = true;
    const booleanKeys = Object.keys(this.booleanFilters);
    for (let idx = 0; idx < booleanKeys.length; idx++) {
      if (this.booleanFilters[booleanKeys[idx]]) {
        pass = pass && node.data[booleanKeys[idx]];
      }
    }
    const numberKeys = Object.keys(this.numberFilters);
    for (let idx = 0; idx < numberKeys.length; idx++) {
      switch (numberKeys[idx]) {
        case "maxCommute":
          pass =
            pass &&
            this.numberFilters[numberKeys[idx]] * 60 >=
              node.data["commuteTime"];
          break;
        case "minCommute":
          pass =
            pass &&
            this.numberFilters[numberKeys[idx]] * 60 <=
              node.data["commuteTime"];
          break;
        case "maxTotalYearly":
          if (!this.monthlySwitch) {
            pass =
              pass &&
              this.numberFilters[numberKeys[idx]] >=
                node.data["yearlyCostTotal"];
          }
          break;
        case "minTotalYearly":
          if (!this.monthlySwitch) {
            pass =
              pass &&
              this.numberFilters[numberKeys[idx]] <=
                node.data["yearlyCostTotal"];
          }
          break;
        case "minTotalMonthly":
          if (this.monthlySwitch) {
            pass =
              pass &&
              this.numberFilters[numberKeys[idx]] <=
                node.data["monthlyCostTotal"];
          }
          break;
        case "maxTotalMonthly":
          if (this.monthlySwitch) {
            pass =
              pass &&
              this.numberFilters[numberKeys[idx]] >=
                node.data["monthlyCostTotal"];
          }
          break;
        default:
      }
    }
    return pass;
  }

  componentDidMount() {
    new Promise((resolve) => setTimeout(resolve, 500)).then(
      () => (this.hoverAllowed = true)
    );
  }

  renderOverview(searchResults: TownInfo[]) {
    return (
      <div>
        <Row>
          <Col xs={6}>
            <LinkContainer to="/search">
              <Button variant="secondary">&#10094; Change search</Button>
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
              monthlySwitch={this.monthlySwitch}
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
              <strong>{this.state.selectedTowns.length}</strong> towns filtered from{" "}
              <strong>{this.state.searchResults.length}</strong> within{" "}
              <strong>{renderTime(this.numberFilters["maxCommute"]*60)}</strong> of{" "}
              <strong>{this.searchFormState["selectedTown"][0]["label"]}</strong>
            </h4>
          </Col>
        </Row>
        <Row>
          <Col xs={12} lg={4} className="mt-2 d-flex justify-content-center">
            <TownsOverviewFilter
              handleChange={this.handleFilterChange}
              handleReset={this.resetFilters}
              booleanFilters={this.booleanFilters}
              numberFilters={this.numberFilters}
              maxCommute={this.maxCommute}
              maxYearly={this.maxTotalYearly}
              maxMonthly={this.maxTotalMonthly}
              divKey={this.state.divKey}
              monthlySwitch={this.monthlySwitch}
            />
          </Col>
          <Col xs={12} lg={8} className="mt-2">
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
      </div>
    );
  }

  render() {
    if (
      this.state.searchResults === null ||
      this.state.searchResults === undefined
    ) {
      return <Redirect to="/search" />;
    } else {
      return this.renderOverview(this.state.searchResults);
    }
  }
}

export default TownsOverview;
