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
  import { range } from "./UtilityFunctions";

  interface Row {
    [key: string]: number;
  }

  interface Props {
    data: Row[];
    formatTooltip: (value: any, name: any, props: any) => string[];
    formatLabel: (label: any) => string;
    idToMark: number;
    xName: string;
    yName: string;
  }

  interface State {}

  class Histogram extends React.Component<Props, State> {
    getNiceEdges(maxInputValue: number) {
      let chosenBinWidth;
      const maxValueToBinWidth = [
        [2500, 50],
        [5000, 100],
        [10000, 250],
        [25000, 500],
        [50000, 1000],
        [100000, 2500],
        [250000, 5000],
        [500000, 10000],
        [1000000, 25000],
        [2500000, 50000],
        [5000000, 100000],
        [10000000, 250000],
      ];
      for (let [maxValue, binWidth] of maxValueToBinWidth) {
        if (maxInputValue <= maxValue) {
          chosenBinWidth = binWidth;
          break;
        }
      }
      if (chosenBinWidth === undefined) {
        chosenBinWidth = 5000;
      }

      const rightEdge =
        (Math.floor(maxInputValue / chosenBinWidth) + 2) * chosenBinWidth;
      return range(0, rightEdge, chosenBinWidth);
    }

    getTotalRowValue(row: Row) {
      let value = 0;
      for (let key of Object.keys(row)) {
        if (key !== "id") {
          value += row[key];
        }
      }
      return value;
    }

    getMaxValue() {
      let maxValue = 0;
      for (let row of this.props.data) {
        const value = this.getTotalRowValue(row);
        if (value >= maxValue) {
          maxValue = value;
        }
      }
      return maxValue;
    }

    getIntervalNames(edges: number[]){
      const intervalNames = new Array(edges.length - 1)

      for (let idx = 0; idx < edges.length-1; idx++){
        const leftEdge = edges[idx];
        const rightEdge = edges[idx + 1];
        const interval =
          new Intl.NumberFormat("ch").format(leftEdge) +
          "-" +
          new Intl.NumberFormat("ch").format(rightEdge);
        intervalNames[idx] = interval;
      }
      return intervalNames;
    }

    getPlotData() {
      console.log('getPlotData was called.')
      const maxValue = this.getMaxValue();
      const edges = this.getNiceEdges(maxValue);
      const intervalWidth = edges[1] - edges[0]
      const intervalNames = this.getIntervalNames(edges);
      const countsPerInterval = new Array(edges.length-1).fill(0);

      let idxToMark;
      for (let row of this.props.data) {
        const totalValue = this.getTotalRowValue(row);
        
        const idx = Math.floor(totalValue/intervalWidth);
        if (row["id"] === this.props.idToMark) {
          idxToMark = idx;
        }
        countsPerInterval[idx]++;
      }

      let plotData = new Array(countsPerInterval.length-1);
      for (let idx = 0; idx < countsPerInterval.length; idx++){
        plotData[idx] = {interval: intervalNames[idx], count: countsPerInterval[idx]}
      }

      return { idxToMark: idxToMark, data: plotData };
    }

    render() {
      const plotData = this.getPlotData();
      return (
        <ResponsiveContainer width="100%" aspect={3}>
          <BarChart data={plotData["data"]}>
            <XAxis dataKey="interval" name={this.props.xName} />
            <YAxis name={this.props.yName} />
            <Tooltip
              formatter={this.props.formatTooltip}
              labelFormatter={this.props.formatLabel}
            />
            <Bar dataKey="count">
              {plotData["data"].map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={index === plotData["idxToMark"] ? "#DC143C" : "#6c757d"}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      );
    }
  }

  export default Histogram;
