import React from "react";
import Histogram from "../Utilities/Histogram";
import TownInfo from "./TownInfo";

interface Props {
  selectedTowns: TownInfo[];
  targetTownId: number;
  monthlySwitch: boolean;
}

interface State {}

class TownsHistogram extends React.Component<Props, State> {

  formatTooltip(value: any, name: any, props: any) {
    return [new Intl.NumberFormat("ch").format(value), "Number of Towns"];
  }

  formatLabel(label: any) {
    return "Total Cost Of Living (CHF): " + label;
  }

  getRelevantFieldsHisto() {
    const relevantData = new Array(this.props.selectedTowns.length);
    for (let idx = 0; idx < this.props.selectedTowns.length; idx++) {
      if (this.props.monthlySwitch){
        relevantData[idx] = {
          id: this.props.selectedTowns[idx]["sourceTownId"],
          yearlyCostHealth: this.props.selectedTowns[idx]["monthlyCostHealth"],
          yearlyCostHome: this.props.selectedTowns[idx]["monthlyCostHome"],
          yearlyCostTaxes: this.props.selectedTowns[idx]["monthlyCostTaxes"],
        };
      } else {
        relevantData[idx] = {
          id: this.props.selectedTowns[idx]["sourceTownId"],
          yearlyCostHealth: this.props.selectedTowns[idx]["yearlyCostHealth"],
          yearlyCostHome: this.props.selectedTowns[idx]["yearlyCostHome"],
          yearlyCostTaxes: this.props.selectedTowns[idx]["yearlyCostTaxes"],
        };
      }
    }
    return relevantData;
  }

  render() {
    return (
      <Histogram
        formatTooltip={this.formatTooltip}
        formatLabel={this.formatLabel}
        data={this.getRelevantFieldsHisto()}
        idToMark={this.props.targetTownId}
        xName="Total Cost of Living"
        yName="Number of towns in bracket"
      />
    );
  }
}

export default TownsHistogram;
