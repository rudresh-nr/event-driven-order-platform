function StatusBadge({ status }) {

    let icon = "⚪";

    if (status === "CANCELLED") {
        icon = "🔴";
    } else if (status === "CONFIRMED") {
        icon = "🟢";
    } else if (status === "CREATED") {
        icon = "🟡";
    }

    return (
        <span>
            {icon} {status}
        </span>
    );
}

export default StatusBadge;