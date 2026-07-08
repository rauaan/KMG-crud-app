document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("upload").addEventListener("change", function () {
        const fileNameSpan = document.getElementById("file-name");

        if (this.files.length > 0) {
            fileNameSpan.textContent = this.files[0].name;
        } else {
            fileNameSpan.textContent = "No documents uploaded yet";
        }
    });
});