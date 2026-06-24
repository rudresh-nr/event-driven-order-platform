import axios from "axios";

export async function getDashboardMetrics() {
    const response = await axios.get(
        "http://localhost:8000/dashboard-metrics/"
    );

    return response.data;
}