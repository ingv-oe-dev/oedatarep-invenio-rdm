import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer } from "react-leaflet";
import { CustomMarker, Loading } from "./CustomComponents";
import PropTypes from "prop-types";

export const LocationsMapPreview = ({ markers }) => {
  const [loading, setLoading] = useState(true);
  const [tileLayer, setMapContainer] = useState({});
  const center = markers[0].latlng;

  useEffect(() => {
    setMapContainer(
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        onload={setLoading(false)}
      />
    );
  }, []);

  return loading ? (
    <Loading />
  ) : (
    <MapContainer center={center} zoom={10} scrollWheelZoom markers={markers}>
      {tileLayer}
      {markers.map((position) => (
        <CustomMarker key={position.latlng.toString()} position={position} />
      ))}
    </MapContainer>
  );
};

LocationsMapPreview.propTypes = {
  markers: PropTypes.array.isRequired,
};
