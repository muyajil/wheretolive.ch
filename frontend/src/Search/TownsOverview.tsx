import React from "react";
import Table from "../Utilities/Table";
import TownsHistogram from "./TownsHistogram";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

interface TownInfo {
  aldi: boolean;
  lidl: boolean;
  coop: boolean;
  migros: boolean;
  sourceTownBFSNr: number;
  sourceTownName: string;
  sourceTownId: number;
  sourceTownZip: number;
  yearlyCostHealth: number;
  yearlyCostHome: number;
  yearlyCostTaxes: number;
}

interface Props {
  rowData: TownInfo[];
}

interface State {
  columnDefs: object[];
}

class TownsOverview extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      columnDefs: [
        { headerName: "ZIP Code", field: "sourceTownZip" },
        { headerName: "Town", field: "sourceTownName" },
        { headerName: "Yearly Cost Health", field: "yearlyCostHealth" },
        { headerName: "Yearly Cost Home", field: "yearlyCostHome" },
        { headerName: "Yearly Cost Taxes", field: "yearlyCostTaxes" },
        { headerName: "Migros", field: "migros" },
        { headerName: "Coop", field: "coop" },
        { headerName: "Aldi", field: "aldi" },
        { headerName: "Lidl", field: "lidl" },
      ],
    };
  }

  getRelevantFieldsHisto() {
    const relevantData = new Array(this.props.rowData.length);
    for (let idx = 0; idx < this.props.rowData.length; idx++) {
      relevantData[idx] = {
        yearlyCostHealth: this.props.rowData[idx]["yearlyCostHealth"],
        yearlyCostHome: this.props.rowData[idx]["yearlyCostHome"],
        yearlyCostTaxes: this.props.rowData[idx]["yearlyCostTaxes"],
      };
    }
    return relevantData;
  }

  renderBarPlot() {
    return <h3 className="text-center text-light mt-5">Select less than 50 towns to display detailed data.</h3>
  }

  render() {
    return (
      <div>
        <Row>
          <Col xs={12} lg={6}>
          <TownsHistogram
            data={JSON.stringify(this.getRelevantFieldsHisto())}
            targetTownId={1}
          />
          </Col>
          <Col xs={12} lg={6}>
            {this.renderBarPlot()}
          </Col>
        </Row>
        <Row>
          <Col xs={12}>
          <Table
            rowData={this.props.rowData}
            columnDefs={this.state.columnDefs}
          />
          </Col>
        </Row>
      </div>
    );
  }
}

export default TownsOverview;
