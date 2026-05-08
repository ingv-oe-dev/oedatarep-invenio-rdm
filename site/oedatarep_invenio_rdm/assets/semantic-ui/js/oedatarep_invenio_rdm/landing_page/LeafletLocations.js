import React, { useMemo } from "react";
import { Container } from "semantic-ui-react";
import { LocationsMapPreview } from "../components/LocationsMapPreview";
import PropTypes from "prop-types";

export const LeafletLocations = ({ locations }) => {
  const markers = useMemo(() => {
    if (!locations || !Array.isArray(locations.features)) {
      return [];
    }

    return locations.features
      .filter(
        (feature) =>
          feature.geometry &&
          feature.geometry.type === "Point" &&
          Array.isArray(feature.geometry.coordinates) &&
          feature.geometry.coordinates.length >= 2
      )
      .map((feature) => {
        const [lng, lat] = feature.geometry.coordinates;

        return {
          latlng: [lat, lng],
          place: feature.place || "",
          description: feature.description || "",
        };
      });
  }, [locations]);

  if (markers.length === 0) {
    return null;
  }

  return (
    <Container>
      <LocationsMapPreview markers={markers} />
    </Container>
  );
};

LeafletLocations.propTypes = {
  locations: PropTypes.shape({
    features: PropTypes.arrayOf(
      PropTypes.shape({
        geometry: PropTypes.shape({
          type: PropTypes.string,
          coordinates: PropTypes.arrayOf(PropTypes.number),
        }),
        place: PropTypes.string,
        description: PropTypes.string,
      })
    ),
  }).isRequired,
};
