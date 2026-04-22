/* =========================
   LOGIN FUNCTION
========================= */
function login() {
  const email = document.getElementById("email")?.value;
  const password = document.getElementById("password")?.value;

  fetch("/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  })
  .then(res => res.json())
  .then(data => {
    if (data.user) {
      // ✅ USER SAVE
      localStorage.setItem("user", JSON.stringify({
        id: data.user.id,
        name: data.user.name,
        email: data.user.email
      }));

      // ✅ REDIRECT
      window.location.href = "/static/customer/index.html";
    } else {
      const msg = document.getElementById("msg");
      if (msg) msg.innerText = "Invalid login";
    }
  })
  .catch(err => {
    console.error("Login error:", err);
  });
}

/* =========================
   NAVBAR LOGIC (SAFE)
========================= */
document.addEventListener("DOMContentLoaded", () => {
  const nav = document.getElementById("navLinks");
  if (!nav) return; // 🔥 MOST IMPORTANT LINE

  const user = JSON.parse(localStorage.getItem("user"));

  if (user && user.name) {
    nav.innerHTML = `
      <span style="color:white;margin-right:15px;">
        👋 Hi, <b>${user.name}</b>
      </span>
      <a href="/static/customer/products.html">Products</a>
      <a href="/static/customer/best-sellers.html">Best Sellers</a>
      <a href="/static/customer/cart.html">Cart</a>
      <a href="#" onclick="logout()">Logout</a>
    `;
  } else {
    nav.innerHTML = `
      <a href="/static/customer/products.html">Products</a>
      <a href="/static/customer/best-sellers.html">Best Sellers</a>
      <a href="/static/customer/cart.html">Cart</a>
      <a href="/static/customer/login.html">Login</a>
    `;
  }
});

/* =========================
   LOGOUT
========================= */
function logout() {
  localStorage.removeItem("user");
  window.location.href = "/static/customer/login.html";
}



function signup() {
  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  if (!name || !email || !password) {
    document.getElementById("msg").innerText = "All fields required";
    return;
  }

  fetch("/signup", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email, password })
  })
  .then(res => res.json())
  .then(data => {
    if (data.message) {
      document.getElementById("msg").innerText =
        "✅ Signup successful. Please login.";

      setTimeout(() => {
        window.location.href = "/static/customer/login.html";
      }, 1200);
    } else {
      document.getElementById("msg").innerText =
        data.error || "Signup failed";
    }
  })
  .catch(() => {
    document.getElementById("msg").innerText = "Server error";
  });
}
