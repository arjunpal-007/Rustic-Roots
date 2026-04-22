fetch("/products")
  .then(res => res.json())
  .then(products => {
    const container = document.getElementById("products");

    if (products.length === 0) {
      container.innerHTML = "<p>No products available</p>";
      return;
    }

    products.forEach(p => {
      container.innerHTML += `
        <div class="card">
          <img src="/static/uploads/${p.image}">
          <h3>${p.name}</h3>
          <p>${p.description}</p>
          <strong>₹${p.price}</strong>
          <br><br>
          <button onclick='addToCart(${JSON.stringify(p)})'>
            Add to Cart
          </button>
        </div>
      `;
    });
  });


// ADD TO CART

function addToCart(id, name, price, image) {
  let cart = JSON.parse(localStorage.getItem("cart")) || [];

  const existing = cart.find(p => p.id === id);

  if (existing) {
    existing.quantity += 1;
  } else {
    cart.push({
      id: id,
      name: name,
      price: price,
      image: image,
      quantity: 1
    });
  }

  localStorage.setItem("cart", JSON.stringify(cart));
  alert("✅ Added to cart");
}



