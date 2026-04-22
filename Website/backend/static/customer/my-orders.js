const nav = document.getElementById("navLinks");
const user = JSON.parse(localStorage.getItem("user"));

fetch("/my-orders")
.then(res => res.json())
.then(data => {

    const box = document.getElementById("orders");

    if (data.length === 0) {
        box.innerHTML = "<p>No orders yet.</p>";
        return;
    }

    data.forEach(o => {

        let items = JSON.parse(o.items).map(
            i => `${i.name} × ${i.quantity || i.qty || 1}`
        ).join("<br>");

        box.innerHTML += `
        <div class="card">
            <h3>Order #${o.id}</h3>
            <p>${items}</p>
            <strong>Total: ₹${o.total}</strong><br><br>
            <span class="badge ${o.status}">${o.status}</span>
            <br><br>
            <button class="invoice-btn" data-id="${o.id}">
                🧾 Download Invoice
            </button>
        </div>
        `;
    });

    // 🔥 IMPORTANT PART (Event Delegation)
    document.querySelectorAll(".invoice-btn").forEach(btn => {
        btn.addEventListener("click", function() {
            const orderId = this.getAttribute("data-id");
            window.location.href = `/invoice/${orderId}`;
        });
    });

});
