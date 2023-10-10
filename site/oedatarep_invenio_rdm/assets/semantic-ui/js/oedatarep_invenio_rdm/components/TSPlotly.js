import React from "react";
import Plotly from "plotly.js-basic-dist-min";
import createPlotlyComponent from 'react-plotly.js/factory';
import PropTypes from "prop-types";

export const TSPlotly = ({ tsdata }) => {

  const Plot = createPlotlyComponent(Plotly)
  var resultValues = [];

  for (const [key, value] of Object.entries(tsdata)) {
    if (key !== "timestamp") {
      resultValues.push({
        name: key,
        x: tsdata.timestamp,
        y: value,
        type: "scatter",
        mode: "lines",
        line: { color: randomHexColor() },
      });
    }
  }

  return (
    <Plot
      data={resultValues}
      layout={{
        autosize: true,
        title: "Time Series",
        xaxis: {
          autorange: true,
          type: "date",
        },
        yaxis: {
          autorange: true,
          type: "linear",
        },
      }}
      useResizeHandler
      style={{ width: "100%", height: "100%" }}
    />
  );
};

TSPlotly.propTypes = {
  tsdata: PropTypes.object.isRequired,
};

function randomInteger(max) {
  return Math.floor(Math.random() * (max + 1));
}

function randomRgbColor() {
  let r = randomInteger(255);
  let g = randomInteger(255);
  let b = randomInteger(255);
  return [r, g, b];
}

function randomHexColor() {
  let [r, g, b] = randomRgbColor();

  let hr = r.toString(16).padStart(2, "0");
  let hg = g.toString(16).padStart(2, "0");
  let hb = b.toString(16).padStart(2, "0");

  return "#" + hr + hg + hb;
}