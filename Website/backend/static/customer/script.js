document.addEventListener("DOMContentLoaded", () => {

    fetch("/products")
    .then(res => res.json())
    .then(data => {
        const box = document.getElementById("products");
        if (!box) {
            console.log("Products container not found");
            return;
        }

        box.innerHTML = "";

        data.forEach(p => {
            const div = document.createElement("div");
            div.className = "card";
            div.innerHTML = `
                <img src="/static/uploads/${p.image}"
                     onclick="openProduct(${p.id})"
                     style="cursor:pointer;">

                <h3 onclick="openProduct(${p.id})"
                    style="cursor:pointer;">
                    ${p.name}
                </h3>

                <p>₹${p.price}</p>

                <button onclick='addToCart(${JSON.stringify(p)})'>
                    Add to Cart
                </button>
            `;
            box.appendChild(div);
        });
    })
    .catch(err => {
        console.error("Product fetch error:", err);
    });

});

// PRODUCT DETAIL REDIRECT
function openProduct(id) {
    window.location.href =
        `/static/customer/product.html?id=${id}`;
}

// ADD TO CART
function addToCart(product) {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    const found = cart.find(p => p.id === product.id);

    if (found) {
        found.qty += 1;
    } else {
        product.qty = 1;
        cart.push(product);
    }

    localStorage.setItem("cart", JSON.stringify(cart));
    alert("Added to cart");
}
