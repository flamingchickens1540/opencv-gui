var socket = io(window.location.href);

// Interval function that tests message latency by sending a "ping"
// message. The server then responds with a "pong" message and the
// round trip time is measured.
let rt_latency = [];
let start_time;
window.setInterval(function () {
    start_time = (new Date).getTime();
    socket.emit('rt_ping');
}, 250); // Update every 250ms

// Handler for the "pong" message. When the pong is received, the
// time from the ping is stored, and the average of the last 30
// samples is average and displayed.
socket.on('rt_pong', function () {
    const latency = (new Date).getTime() - start_time;
    rt_latency.push(latency);
    rt_latency = rt_latency.slice(-30); // keep last 30 samples
    let sum = 0;
    for (let i = 0; i < rt_latency.length; i++)
        sum += rt_latency[i];
    document.getElementById("latency").innerHTML = (Math.round(10 * sum / rt_latency.length) / 10).toString();
});
