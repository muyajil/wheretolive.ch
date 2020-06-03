import React from "react";
import Histogram from "../Utilities/Histogram";

interface Props {
  data: string;
  targetTownId: number;
}

interface State {
}

class TownsHistogram extends React.Component<Props, State> {

  formatTooltip(value:any, name:any, props:any){
    return [new Intl.NumberFormat('ch').format(value), "Number of Towns"]
  }

  formatLabel(label:any){
    return ("Total Cost Of Living (CHF): " + label)
  }

  render() {
    return (
      <Histogram 
        formatTooltip={this.formatTooltip}
        formatLabel={this.formatLabel}
        data={JSON.parse(this.props.data)}
        idToMark={this.props.targetTownId}
        xName="Total Cost of Living"
        yName="Number of towns in bracket"
      />
    );
  }
}

export default TownsHistogram;