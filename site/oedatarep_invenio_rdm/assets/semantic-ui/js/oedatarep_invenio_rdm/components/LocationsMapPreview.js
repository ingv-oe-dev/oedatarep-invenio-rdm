import React, { useEffect, useState } from "react";
import { Map, TileLayer } from "react-leaflet";
import L from "leaflet";
import { CustomMarker, Loading } from "./CustomComponents";
import PropTypes from "prop-types";

export const LocationsMapPreview = ({ markers }) => {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fallbackTimer = setTimeout(() => {
      setLoading(false);
    }, 3000);

    return () => clearTimeout(fallbackTimer);
  }, []);

  if (!markers || markers.length === 0) {
    return null;
  }

  const bounds = L.latLngBounds(markers.map((marker) => marker.latlng));

  return (
    <div style={{ position: "relative", height: "400px", width: "100%" }}>
      {loading && <Loading />}

      <Map
        bounds={bounds}
        boundsOptions={{ padding: [40, 40], maxZoom: 10}}
        scrollWheelZoom={true}
        style={{ height: "400px", width: "100%" }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          onload={() => setLoading(false)}
        />

        {markers.map((marker, index) => (
          <CustomMarker
            key={`${marker.latlng[0]}-${marker.latlng[1]}-${index}`}
            position={marker}
          />
        ))}
      </Map>
    </div>
  );
};

LocationsMapPreview.propTypes = {
  markers: PropTypes.arrayOf(
    PropTypes.shape({
      latlng: PropTypes.arrayOf(PropTypes.number).isRequired,
      place: PropTypes.string,
      description: PropTypes.string,
    })
  ).isRequired,
};
