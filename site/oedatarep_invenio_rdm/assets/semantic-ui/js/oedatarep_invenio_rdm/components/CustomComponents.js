import React from "react";
import { Marker, Popup } from "react-leaflet";
import { List, Placeholder } from "semantic-ui-react";
import { icon } from "../landing_page/LeafletIcons";
import PropTypes from "prop-types";

export const CustomMarker = ({ position }) => {
  const { latlng, place, description } = position;

  return (
    <Marker position={latlng} icon={icon}>
      <Popup>
        <List>
          <List.Item>
            <List.Content>
              {place && <List.Header>{place}</List.Header>}
              {description && (
                <List.Description>{description}</List.Description>
              )}
            </List.Content>
          </List.Item>
        </List>
      </Popup>
    </Marker>
  );
};

export const Loading = () => (
  <Placeholder fluid>
    <Placeholder.Line />
    <Placeholder.Line />
    <Placeholder.Line />
    <Placeholder.Line />
    <Placeholder.Line />
  </Placeholder>
);

CustomMarker.propTypes = {
  position: PropTypes.shape({
    latlng: PropTypes.arrayOf(PropTypes.number).isRequired,
    place: PropTypes.string,
    description: PropTypes.string,
  }).isRequired,
};
