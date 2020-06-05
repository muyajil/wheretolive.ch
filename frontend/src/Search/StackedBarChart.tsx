import React from "react";
import {
  ResponsiveContainer,
  BarChart,
  XAxis,
  YAxis,
  Tooltip,
  Bar,
  Cell,
} from "recharts";

interface Row {
  [key: string]: number;
}

interface Props {
  data: Row[];
  idToMark: number;
}

interface State {}

class StackedBarChart extends React.Component<Props, State> {
  formatTooltip(value: any, name: any, props: any) {
    let formattedName;
    if (name === "yearlyCostHome") {
      formattedName = "Yearly Cost Home";
    } else if (name === "yearlyCostTaxes") {
      formattedName = "Yearly Cost Taxes";
    } else {
      formattedName = "Yearly Cost Health";
    }
    return ["CHF " + new Intl.NumberFormat("ch").format(value), formattedName];
  }

  formatLabel(name: any){
    return <strong>{name}</strong>
  }

  render() {
    return (
      <ResponsiveContainer width="100%" aspect={3}>
        <BarChart data={this.props.data}>
          <XAxis dataKey="sourceTownName" name="Town" hide={false} />
          <YAxis
            name="Total Cost"
            tickFormatter={(value) => new Intl.NumberFormat("ch").format(value)}
            hide={true}
          />
          <Tooltip labelFormatter={this.formatLabel} formatter={this.formatTooltip} />
          <Bar dataKey="yearlyCostTaxes" stackId="a">
            {this.props.data.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={
                  entry["sourceTownId"] === this.props.idToMark
                    ? "#DC143C"
                    : "#9c3e3e"
                }
              />
            ))}
          </Bar>
          <Bar dataKey="yearlyCostHealth" stackId="a">
            {this.props.data.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={
                  entry["sourceTownId"] === this.props.idToMark
                    ? "#DC143C"
                    : "#b26516"
                }
              />
            ))}
          </Bar>
          <Bar dataKey="yearlyCostHome" stackId="a">
            {this.props.data.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={
                  entry["sourceTownId"] === this.props.idToMark
                    ? "#DC143C"
                    : "#9ba315"
                }
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    );
  }
}

export default StackedBarChart;
