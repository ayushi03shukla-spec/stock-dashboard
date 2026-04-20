let chart;

async function loadData(symbol) {
    try {
        const res = await fetch(`http://127.0.0.1:8000/data/${symbol}`);
        const data = await res.json();

        console.log("DATA:", data);

        if (!Array.isArray(data) || data.length === 0) {
            alert("No data found");
            return;
        }

        // 🔥 Ensure proper values
        const labels = data.map(d => d.Date);
        const prices = data.map(d => Number(d.Close));

        // Remove NaN values
        const cleanLabels = [];
        const cleanPrices = [];

        for (let i = 0; i < prices.length; i++) {
            if (!isNaN(prices[i])) {
                cleanLabels.push(labels[i]);
                cleanPrices.push(prices[i]);
            }
        }

        if (chart) chart.destroy();

        const ctx = document.getElementById("chart").getContext("2d");

        chart = new Chart(ctx, {
            type: "line",
            data: {
                labels: cleanLabels,
                datasets: [{
                    label: symbol + " Price",
                    data: cleanPrices,
                    borderWidth: 2,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        ticks: {
                            maxTicksLimit: 6
                        }
                    }
                }
            }
        });

    } catch (err) {
        console.error("ERROR:", err);
    }
}

document.getElementById("company").addEventListener("change", (e) => {
    loadData(e.target.value);
});

loadData("TCS");
async function loadMovers() {
    const res = await fetch("http://127.0.0.1:8000/top-movers");
    const data = await res.json();

    document.getElementById("movers").innerHTML = `
        <p>📈 Top Gainer: ${data.top_gainer.symbol}</p>
        <p>📉 Top Loser: ${data.top_loser.symbol}</p>
    `;
}

loadMovers();