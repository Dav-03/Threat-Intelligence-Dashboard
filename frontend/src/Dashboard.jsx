import { useState, useEffect } from "react"
import { getStats, getIndicators, getAlerts } from "./services/api"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from "recharts"
import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet"
import "leaflet/dist/leaflet.css"

function Dashboard() {
    const [stats, setStats] = useState(null)
    const [loading, setLoading] = useState(true)
    const [indicators, setIndicators] = useState([])
    const [alerts, setAlerts] = useState([])
    const ipIndicators = indicators.filter(ioc => ioc.type === "IPv4")

    useEffect(() => {
        getStats()
            .then(data => {
                setStats(data)
                setLoading(false)
            })
            .catch(err => console.error(err))
    }, [])

    useEffect(() => {
        getStats().then(data => { setStats(data); setLoading(false) })
        getIndicators().then(data => setIndicators(data))
        getAlerts().then(data => setAlerts(data))
    }, [])

    const severityData = stats ? [
        { name: "critical", count: stats.severity_breakdown.critical ?? 0 },
        { name: "high", count: stats.severity_breakdown.high ?? 0 },
        { name: "medium", count: stats.severity_breakdown.medium ?? 0 },
        { name: "low", count: stats.severity_breakdown.low ?? 0 },
    ] : []

    if (loading)
        return <p>Loading...</p>

    else
        return (
            <div>
                <h1>Threat Intel Dashboard</h1>
                <div>
                    <div>
                        <h3>Total IOCs</h3>
                        <p>{stats.total_iocs}</p>
                    </div>
                    <div>
                        <h3>Critical</h3>
                        <p>{stats.severity_breakdown.critical ?? 0}</p>
                    </div>
                    <div>
                        <h3>Medium</h3>
                        <p>{stats.severity_breakdown.medium ?? 0}</p>
                    </div>
                </div>

                // Chart
                <BarChart width={500} height={300} data={severityData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="count" fill="#e05252" />
                </BarChart>
                // IOC table
                <table>
                    <thead>
                        <tr>
                            <th>Type</th>
                            <th>Value</th>
                            <th>Source</th>
                            <th>Severity</th>
                            <th>Timestamp</th>
                        </tr>
                    </thead>
                    <tbody>
                        {indicators.map(ioc => (
                            <tr key={ioc.id}>
                               <td>{ioc.type}</td>
                               <td>{ioc.value}</td>
                               <td>{ioc.source}</td>
                               <td>{ioc.severity}</td>
                               <td>{new Date(ioc.timestamp).toLocaleString()}</td> 
                            </tr>
                        ))}
                    </tbody>
                </table>

                <h2>Recent Alerts</h2>
                <table>
                    <thread>
                        <tr>
                            <th>Rule</th>
                            <th>Descriptions</th>
                            <th>Severity</th>
                            <th>Timestamps</th>
                        </tr>
                    </thread>
                    <tbody>
                        {alerts.map(alert => (
                            <tr key={alert.id}>
                                <td>{alert.rule_name}</td>
                                <td>{alert.description}</td>
                                <td>{alert.severity}</td>
                                <td>{new Date(alert.timestamp).toLocaleString()}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>

                <MapContainer center={[20, 0]} zoom={2} style={{ height: "400px", width: "100%" }}>
                    <TileLayer
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                        attribution='&copy; OpenStreetMap contributors'
                    />
                    {ipIndicators.map(ioc => (
                        <CircleMarker
                            key={ioc.id}
                            center={[0, 0]}
                            radius={6}
                            color={ioc.severity === "critical" ? "red" : "orange"}
                        >
                            <Popup>{ioc.value} — {ioc.severity}</Popup>
                        </CircleMarker>
                    ))}
                </MapContainer>
            </div>
        )
}
export default Dashboard