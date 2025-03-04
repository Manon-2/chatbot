document.addEventListener("DOMContentLoaded", function () {
    const button = document.getElementById("clickButton");
    const message = document.getElementById("message");

    button.addEventListener("click", function () {
        message.textContent = "تم الضغط على الزر!";
        message.classList.add("show");
    });
});
