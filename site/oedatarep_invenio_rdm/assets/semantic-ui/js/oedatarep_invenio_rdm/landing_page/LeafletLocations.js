import React, { useEffect, useState } from "react";
import { Container, List } from "semantic-ui-react";
import { LocationsMapPreview } from "../components/LocationsMapPreview";
import { Loading } from "../components/CustomComponents";
import PropTypes from "prop-types";

export const LeafletLocations = ({ locations }) => {
  const [locs, setLocations] = useState({});
  const [markers, setMarkers] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const markers = [];
    const locs = [];
    locations.features.forEach((element) => {
      if (element.geometry) {
        switch (element.geometry.type) {
          case "Point":
            markers.push({
              latlng: element.geometry.coordinates.reverse(),
              place: element.place ? element.place : "",
              description: element.description ? element.description : "",
            });
            break;
          default:
            locs.push({
              place: element.place ? element.place : "",
              description: element.description ? element.description : "",
            });
            break;
        }
      } else {
        locs.push({
          place: element.place ? element.place : "",
          description: element.description ? element.description : "",
        });
      }
    });
    setLocations(locs);
    setMarkers(markers);
    setLoading(false);
  }, []);

  return loading ? (
    <Loading />
  ) : (
    <Container>
      {markers.length > 0 ? <LocationsMapPreview markers={markers} /> : ""}
    </Container>
  );
};

LeafletLocations.propTypes = {
  locations: PropTypes.object.isRequired,
};
