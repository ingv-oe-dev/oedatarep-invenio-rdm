// This file is part of InvenioRDM
// Copyright (C) 2020-2021 CERN.
// Copyright (C) 2020-2021 Northwestern University.
// Copyright (C) 2021 Graz University of Technology.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React from "react";
import ReactDOM from "react-dom";

import { Plotly } from "./Plotly";
import { LeafletLocations } from "./LeafletLocations";

const leafletLocationsDiv = document.getElementById("leaflet-locations");
const recordPlotlyDiv = document.getElementById("recordPlotly");

if (leafletLocationsDiv) {
  ReactDOM.render(
    <LeafletLocations locations={JSON.parse(leafletLocationsDiv.dataset.locations)} />,
    leafletLocationsDiv
  );
}

if (recordPlotlyDiv) {
  ReactDOM.render(
    <Plotly
      chartresource={JSON.parse(recordPlotlyDiv.dataset.chartresource)}
      tsdtoken={recordPlotlyDiv.dataset.tsdtoken}
      tsdsrvurl={recordPlotlyDiv.dataset.tsdsrvurl}
    />,
    recordPlotlyDiv
  );
}