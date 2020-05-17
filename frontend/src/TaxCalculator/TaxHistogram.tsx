import React from "react";
import {
  ResponsiveContainer,
  BarChart,
  XAxis,
  YAxis,
  Cell,
  Tooltip,
  Bar,
} from "recharts";

interface Props {
  data: Map<string, Object>[];
  targetTownIdx: number;
}

interface State {
  data: Map<string, Object>[];
}

class TaxHistogram extends React.Component<Props, State> {

  formatTooltip(value:any, name:any, props:any){
    return [new Intl.NumberFormat('ch').format(value), "Number of Towns"]
  }

  formatLabel(label:any){

    return ("Tax Bracket (CHF): " + label)
  }

  render() {
    return (
      <ResponsiveContainer width="100%" aspect={3}>
        <BarChart
          data={this.props.data}
        >
          <XAxis dataKey="range" name="Tax Brackets"/>
          <YAxis name="Number of towns in tax bracket"/>
          <Tooltip formatter={this.formatTooltip} labelFormatter={this.formatLabel}/>
          <Bar dataKey="count">
            {this.props.data.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={index === this.props.targetTownIdx ? "#DC143C" : "#6c757d"}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    );
  }
}

export default TaxHistogram;
