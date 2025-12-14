async function fetchJSON(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error("API error");
  return res.json();
}

/* Attendance Summary */
async function loadAttendanceSummary() {
  const data = await fetchJSON("/api/attendance-records/");
  let present = data.filter(r => r.attendance_type === "IN").length;
  let out = data.filter(r => r.attendance_type === "OUT").length;

  document.getElementById("attendance-summary").innerHTML =
    `IN: ${present}<br>OUT: ${out}`;
}

/* Camera Status */
async function loadCameraStatus() {
  const data = await fetchJSON("/api/camera-metrics/");
  const counts = { running: 0, error: 0, stopped: 0 };

  data.forEach(c => counts[c.status] = (counts[c.status] || 0) + 1);

  document.getElementById("camera-status").innerHTML =
    `Running: ${counts.running || 0}<br>
     Error: ${counts.error || 0}<br>
     Stopped: ${counts.stopped || 0}`;
}

/* System Health */
async function loadSystemHealth() {
  const data = await fetchJSON("/api/system-metrics/");
  if (!data.length) return;

  const m = data[data.length - 1];

  document.getElementById("system-health").innerHTML =
    `CPU: ${m.cpu_percent}%<br>
     RAM: ${m.memory_percent}%<br>
     GPU: ${m.gpu_utilization}%`;
}

/* Alerts */
async function loadAlerts() {
  const data = await fetchJSON("/api/system-alerts/");
  const list = document.getElementById("alerts-list");
  list.innerHTML = "";

  data.slice(0, 10).forEach(a => {
    const li = document.createElement("li");
    li.textContent = `[${a.level}] ${a.message}`;
    list.appendChild(li);
  });
}

/* Weekly Trend (simple count per day) */
async function loadWeeklyTrend() {
  const data = await fetchJSON("/api/attendance-records/");
  const counts = {};

  data.forEach(r => {
    counts[r.date] = (counts[r.date] || 0) + 1;
  });

  const labels = Object.keys(counts);
  const values = Object.values(counts);

  new Chart(document.getElementById("attendance-chart"), {
    type: "line",
    data: {
      labels,
      datasets: [{
        label: "Attendance",
        data: values,
        borderWidth: 2
      }]
    }
  });
}

/* Init */
document.addEventListener("DOMContentLoaded", () => {
  loadAttendanceSummary();
  loadCameraStatus();
  loadSystemHealth();
  loadAlerts();
  loadWeeklyTrend();
});
