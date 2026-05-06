const nav = document.getElementById("navLinks");
const user = JSON.parse(localStorage.getItem("user"));

if (user && user.name) {
  nav.innerHTML = `
    <span style="color:white;margin-right:15px;">
      👋 Hi, <b>${user.name}</b>
    </span>
    <a href="/static/customer/products.html">Products</a>
    <a href="/static/customer/videos.html">Videos</a>
    <a href="/static/customer/testimonials.html">Testimonials</a>
    <a href="/static/customer/cart.html">Cart</a>
    <a href="/static/customer/my-orders.html">My Orders</a>
    <a href="#" onclick="logout()">Logout</a>
  `;
}

function logout() {
  localStorage.removeItem("user");
  alert("Logged out successfully");
  window.location.href = "/static/customer/login.html";
}

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
