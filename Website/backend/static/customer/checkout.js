const form = document.getElementById("checkoutForm");
const msg = document.getElementById("msg");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const cart = JSON.parse(localStorage.getItem("cart"));

    console.log("CART FROM STORAGE:", cart);

    if (!cart || cart.length === 0) {
        msg.innerText = "Cart is empty!";
        return;
    }

    const total = cart.reduce(
        (sum, item) => sum + Number(item.price) * Number(item.qty),
        0
    );

    const orderData = {
        name: document.getElementById("name").value,
        phone: document.getElementById("phone").value,
        address: document.getElementById("address").value,
        items: cart,
        total: total
    };

    console.log("SENDING ORDER:", orderData);

    try {
        const res = await fetch("/place-order", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(orderData)
        });

        const data = await res.json();

        if (!res.ok) throw new Error(data.error);

        msg.innerText = data.message;
        localStorage.removeItem("cart");
        form.reset();

    } catch (err) {
        console.error(err);
        msg.innerText = "Order failed";
    }
});
