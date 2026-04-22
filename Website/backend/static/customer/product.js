
const params = new URLSearchParams(window.location.search);
const id = parseInt(params.get("id"));   // 🔥 IMPORTANT FIX

let currentProduct = null;

fetch("/products")
  .then(res => res.json())
  .then(products => {

    console.log("URL ID:", id);
    console.log("All products:", products);

    currentProduct = products.find(p => Number(p.id) === id);

    if (!currentProduct) {
      alert("Product not found");
      return;
    }

    document.getElementById("img").src =
      "/static/uploads/" + currentProduct.image;

    document.getElementById("name").innerText =
      currentProduct.name;

    document.getElementById("price").innerText =
      "₹" + currentProduct.price;

    document.getElementById("desc").innerText =
      currentProduct.description;
  });

function addToCart() {
  let cart = JSON.parse(localStorage.getItem("cart")) || [];

  const item = cart.find(i => i.id === currentProduct.id);

  if (item) {
    item.quantity += 1;
  } else {
    cart.push({
      id: currentProduct.id,
      name: currentProduct.name,
      price: currentProduct.price,
      image: currentProduct.image,
      quantity: 1
    });
  }

  localStorage.setItem("cart", JSON.stringify(cart));
  alert("Added to cart 🛒");
}

