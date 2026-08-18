// document.addEventListener("DOMContentLoaded", () => {
//     document.getElementById("upload").addEventListener("change", function () {
//         const fileNameSpan = document.getElementById("file-name");

//         if (this.files.length > 0) {
//             fileNameSpan.textContent = this.files[0].name;
//         } else {
//             fileNameSpan.textContent = "No documents uploaded yet";
//         }
//     });
// });

document.addEventListener("DOMContentLoaded", function () {
    const menu = document.getElementById("excel-menu");
    if (!menu) return; // элемент есть не на всех страницах

    const panel = document.getElementById("excel-menu-panel");
    const summary = menu.querySelector("summary");

    function positionPanel() {
        const rect = summary.getBoundingClientRect();
        panel.style.top = (rect.bottom + 8) + "px";
        panel.style.left = "";
        panel.style.right = (window.innerWidth - rect.right) + "px";
    }

    menu.addEventListener("toggle", function () {
        if (menu.open) {
            positionPanel();
            window.addEventListener("scroll", positionPanel, true);
            window.addEventListener("resize", positionPanel);
        } else {
            window.removeEventListener("scroll", positionPanel, true);
            window.removeEventListener("resize", positionPanel);
        }
    });

    document.addEventListener("click", function (event) {
        if (menu.open && !menu.contains(event.target)) {
            menu.open = false;
        }
    });
});