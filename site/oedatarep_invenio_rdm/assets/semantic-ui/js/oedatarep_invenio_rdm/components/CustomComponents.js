import React from "react";
import { Marker, Popup } from "react-leaflet";
import { List, Placeholder } from "semantic-ui-react";
import { icon } from "../landing_page/LeafletIcons";
import PropTypes from "prop-types";

export const CustomMarker = ({ position }) => {
  return (
    <Marker position={position.latlng} icon={icon}>
      <Popup>
        <List>
          <List.Item>
            <List.Content>
              <List.Header>{position.place}</List.Header>
              <List.Description> {position.description}</List.Description>
            </List.Content>
          </List.Item>
        </List>
      </Popup>
    </Marker>
  );
};

export const Loading = () => (
  <Placeholder>
    <Placeholder.Line />
    <Placeholder.Line />
    <Placeholder.Line />
    <Placeholder.Line />
    <Placeholder.Line />
  </Placeholder>
);

CustomMarker.propTypes = {
  position: PropTypes.object.isRequired,
};
