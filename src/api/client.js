// src/api/client.js
const BASE = import.meta.env.VITE_API_URL;

export async function parkingNearLocation({ lat, long, maxdistance }) {
    const res = await fetch(`${BASE}/parking/near_location`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ maxdistance, coordinates: { lat, long } }),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
}

// coords must be [[lon,lat], [lon,lat], ...]
export async function stationsNearRoute({ coords, maxdistance }) {
    const res = await fetch(`${BASE}/stations/near_route`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ maxdistance, coordinates: coords }),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
}
