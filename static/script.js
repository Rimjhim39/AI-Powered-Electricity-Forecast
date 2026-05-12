let chart;
let demandChart;

const API_KEY = "YOUR_API_KEY";

/* ===================== 🚀 MAIN FUNCTION ===================== */

async function predict() {

    const date = document.getElementById("date").value;
    const horizon = document.getElementById("horizon").value;

    try {

        // ✅ Flask relative route
        const response = await fetch("/predict", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                date,
                horizon
            })
        });

        if (!response.ok) {
            throw new Error("Server Error");
        }

        const data = await response.json();

        console.log("Backend Response:", data);

        const prices = data.prices;

        plotGraph(prices);
        plotDemandGraph(prices);

        fillTable(prices);
        updateKPIs(prices);
        generateSmartSuggestion(prices);

        updateDemandSupply(prices);
        updateProsumerData(prices);

        // OPTIONAL
        // await updateWeather();

    } catch (error) {

        console.error("Error:", error);

        alert("Something went wrong. Check console (F12)");
    }
}

/* ===================== 📊 PRICE GRAPH ===================== */

function plotGraph(prices) {

    const ctx = document.getElementById("priceChart").getContext("2d");

    if (chart) chart.destroy();

    chart = new Chart(ctx, {

        type: "line",

        data: {

            labels: prices.map((_, i) => "H" + (i + 1)),

            datasets: [{

                label: "Price (₹)",

                data: prices,

                borderColor: "#00e5ff",

                backgroundColor: "rgba(0,229,255,0.2)",

                tension: 0.4,

                fill: true,

                borderWidth: 3
            }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

/* ===================== 📉 DEMAND GRAPH ===================== */

function plotDemandGraph(prices) {

    const demand = prices.map(p => 200 + p * 30);

    const ctx = document.getElementById("demandChart").getContext("2d");

    if (demandChart) demandChart.destroy();

    demandChart = new Chart(ctx, {

        type: "line",

        data: {

            labels: prices.map((_, i) => "H" + (i + 1)),

            datasets: [

                {
                    label: "Demand (MW)",
                    data: demand,
                    borderColor: "#ff9800"
                },

                {
                    label: "Price (₹)",
                    data: prices,
                    borderColor: "#00e5ff"
                }
            ]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

/* ===================== 📊 KPI ===================== */

function updateKPIs(prices) {

    const current = prices[0];

    const max = Math.max(...prices);

    const min = Math.min(...prices);

    document.getElementById("currentPrice").innerText =
        current.toFixed(2) + " ₹";

    document.getElementById("peakTime").innerText =
        "H" + (prices.indexOf(max) + 1);

    document.getElementById("lowTime").innerText =
        "H" + (prices.indexOf(min) + 1);

    const trend =
        prices.at(-1) > prices[0]
        ? "📈 Increasing"
        : "📉 Decreasing";

    document.getElementById("priceTrend").innerText = trend;
}

/* ===================== 📋 TABLE ===================== */

function fillTable(prices) {

    const tbody = document.querySelector("#priceTable tbody");

    tbody.innerHTML = "";

    prices.forEach((price, i) => {

        let suggestion =
            price < 4 ? "✅ Use"
            : price > 7 ? "❌ Avoid"
            : "⚖ Moderate";

        const demand = Math.round(200 + price * 30);

        tbody.innerHTML += `

            <tr>

                <td>${i + 1}</td>

                <td>${price.toFixed(2)}</td>

                <td>${demand} MW</td>

                <td>${suggestion}</td>

            </tr>
        `;
    });
}

/* ===================== 🤖 SMART SUGGESTION ===================== */

function generateSmartSuggestion(prices) {

    const avg =
        prices.reduce((a, b) => a + b) / prices.length;

    let msg = "";

    if (avg < 5) {

        msg = "💡 Cheap electricity. Run heavy loads now.";

    } else if (avg > 7) {

        msg = "⚠ High prices. Avoid usage & sell energy.";

    } else {

        msg = "⚖ Moderate pricing. Use wisely.";
    }

    const peak =
        prices.indexOf(Math.max(...prices)) + 1;

    const low =
        prices.indexOf(Math.min(...prices)) + 1;

    msg += `<br>🔺 Peak: H${peak}`;

    msg += `<br>🔻 Lowest: H${low}`;

    document.getElementById("recommendation").innerHTML = msg;
}

/* ===================== ⚡ DEMAND/SUPPLY ===================== */

function updateDemandSupply(prices) {

    const avg =
        prices.reduce((a, b) => a + b) / prices.length;

    const demand =
        Math.round(250 + avg * 40);

    const supply =
        Math.round(300 + Math.random() * 100);

    document.getElementById("demand").innerText =
        demand + " MW";

    document.getElementById("supply").innerText =
        supply + " MW";

    document.getElementById("gap").innerText =
        demand > supply
        ? "⚠ Shortage"
        : "✅ Stable";
}

/* ===================== 🔋 PROSUMER ===================== */

function updateProsumerData(prices) {

    const currentPrice = prices[0];

    let battery =
        Math.round(30 + Math.random() * 50);

    let action =
        currentPrice > 7 ? "🔋 Discharge"
        : currentPrice < 4 ? "⚡ Charge"
        : "⚖ Hold";

    document.getElementById("consumption").innerText =
        (5 + Math.random() * 10).toFixed(2) + " kWh";

    document.getElementById("generation").innerText =
        (3 + Math.random() * 8).toFixed(2) + " kWh";

    document.getElementById("battery").innerText =
        battery + "% (" + action + ")";
}

/* ===================== ⚡ BACKGROUND EFFECTS ===================== */

const sparksContainer = document.querySelector(".sparks");

for (let i = 0; i < 12; i++) {

    const bolt = document.createElement("span");

    bolt.style.left = Math.random() * 100 + "%";

    bolt.style.top = Math.random() * 100 + "%";

    bolt.style.animationDelay = Math.random() * 5 + "s";

    sparksContainer.appendChild(bolt);
}

const particleContainer = document.querySelector(".particles");

for (let i = 0; i < 35; i++) {

    const particle = document.createElement("span");

    particle.style.left = Math.random() * 100 + "%";

    particle.style.animationDuration =
        (5 + Math.random() * 10) + "s";

    particle.style.animationDelay =
        Math.random() * 10 + "s";

    particleContainer.appendChild(particle);
}