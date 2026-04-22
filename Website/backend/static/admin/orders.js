fetch("/admin/orders")
.then(res => res.json())
.then(data => {
    const tbody = document.querySelector("#ordersTable tbody");
    tbody.innerHTML = "";

    if (data.length === 0) {
        tbody.innerHTML = "<tr><td colspan='7'>No orders yet</td></tr>";
        return;
    }

    data.forEach(o => {
        tbody.innerHTML += `
            <tr>
                <td>${o.id}</td>
                <td>${o.name}</td>
                <td>${o.phone}</td>
                <td>${o.address}</td>
                <td>₹${o.total}</td>
                <td>
                    <select onchange="updateStatus(${o.id}, this.value)">
                        <option ${o.status==="Pending"?"selected":""}>Pending</option>
                        <option ${o.status==="Shipped"?"selected":""}>Shipped</option>
                        <option ${o.status==="Delivered"?"selected":""}>Delivered</option>
                    </select>
                </td>
                <td>✔</td>
            </tr>
        `;
    });
});

function updateStatus(id, status) {
    fetch(`/admin/update-order-status/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status })
    });
}

const admin = JSON.parse(localStorage.getItem("admin"));

if (!admin) {
  // ❌ not logged in
  window.location.href = "/static/admin/login.html";
}


function logout() {
  localStorage.removeItem("admin");
  window.location.href = "/static/admin/login.html";
}
