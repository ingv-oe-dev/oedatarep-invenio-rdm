import React, { Component } from "react";
import { Container } from "semantic-ui-react";
import axios from "axios";
import { TSPlotly } from "../components/TSPlotly";

import PropTypes from "prop-types";

export class Plotly extends Component {
  constructor(props) {
    super(props);
    const columns = props.chartresource[0].preview.columns;
    var tmpState = {};
    for (let i = 0; i < columns.length; i++) {
      const element = columns[i];
      tmpState[element.name] = [];
    }
    tmpState["timestamp"] = [];
    this.state = tmpState;
  }

  componentDidMount() {
    const { chartresource } = this.props;

    axios({
      url: chartresource[0].tsdws_url,
      method: "get",
    })
      .then((response) => {
        const datas = response.data;
        let obj = {};
        for (const [key, value] of Object.entries(datas.data)) {
          obj[key] = value;
        }
        this.setState(obj);
      })
      .catch(function (error) {
        if (error.response) {
          // The request was made and the server responded with a status code
          // that falls out of the range of 2xx
          console.log("Error response.data: \n" + error.response.data);
          console.log("Error response.status: \n" + error.response.status);
          console.log("Error response.headers: \n" + error.response.headers);
        } else if (error.request) {
          // The request was made but no response was received
          // `error.request`
          console.log("Error response.request: \n" + error.request);
        } else {
          // Something happened in setting up the request that triggered an Error
          console.log("Error", error.message);
        }
        console.log(error.config);
      })
      .then(function () {
        // always executed
      });
  }

  componentDidCatch(error) {
    console.error(error);
  }

  render() {
    return (
      <Container>
        <TSPlotly tsdata={this.state} />
      </Container>
    );
  }
}

Plotly.propTypes = {
  chartresource: PropTypes.array.isRequired,
};
