import MetricCard from "./MetricCard";
import { useEffect, useState } from "react";
import { getDashboardMetrics } from "../api/dashboard";

function Dashboard() {
    const [metrics, setMetrics] = useState(null);

    useEffect(()=> {
        async function loadMetrics(){
            try {
                const data = await getDashboardMetrics();
                setMetrics(data);
            }catch(error){
                console.error(error);
            }
        }

        loadMetrics();
    },[]);

    if (!metrics) {
    return <p>Loading metrics...</p>;
    }

    return (
        <div className="dashboard-grid">
            <MetricCard title="Order Created" value={metrics.orders_created}/>
            <MetricCard title="Event Published" value={metrics.events_published}/>
            <MetricCard title="Event Consumed" value={metrics.events_consumed}/>
            <MetricCard title="Outbox Backlog" value={metrics.outbox_backlog}/>
        </div>
    );
}

export default Dashboard;