const form = document.getElementById("productForm");
const productsDiv = document.getElementById("products");

form.onsubmit = async (e) =>{
    e.preventDefault();
    const formData = new FormData(form);

    await fetch("/admin/add-product", {
  method: "POST",
  body: formData
})
.then(res => res.json())
.then(data => {
  alert(data.message);
  window.location.reload(); // or redirect
})};


function loadProducts() {
    fetch("/admin/products")
    .then(res => res.json())
    .then(products => {
        productsDiv.innerHTML = "";
        products.forEach(p => {
            productsDiv.innerHTML += `
                <div style="border:1px solid #ccc; padding:10px; margin:10px">
                    <b>${p.name}</b> – ₹${p.price}<br>
                    ${p.description}<br><br>

                    <button onclick="editProduct(${p.id})">Edit</button>
                    <button onclick="deleteProduct(${p.id})">Delete</button>
                </div>
            `;
        });
    });
}

function deleteProduct(id) {
    fetch(`/admin/delete-product/${id}`, {
        method: "DELETE"
    }).then(loadProducts);
}

function editProduct(id) {
    const name = prompt("New name?");
    const price = prompt("New price?");
    const description = prompt("New description?");

    fetch(`/admin/update-product/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, price, description })
    }).then(loadProducts);
}

loadProducts();
