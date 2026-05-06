function adminLogin() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  if (!email || !password) {
    document.getElementById("msg").innerText = "Enter email & password";
    return;
  }

  fetch("/admin/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      // ✅ Save admin session
      localStorage.setItem("admin", JSON.stringify(data.admin));

      // 🔥 Redirect to orders page
      window.location.href = "/static/admin/orders.html";
    } else {
      document.getElementById("msg").innerText = "Invalid admin credentials";
    }
  })
  .catch(err => {
    document.getElementById("msg").innerText = "Server error";
  });
}
