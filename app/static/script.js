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
<!-- Chart.js -->

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<script>

const productionLabels = {{ production_labels|tojson }};
const productionValues = {{ production_values|tojson }};

const waterLabels = {{ water_labels|tojson }};
const waterValues = {{ water_values|tojson }};

const companyLabels = {{ company_labels|tojson }};
const companyValues = {{ company_values|tojson }};
const companyIds = {{ company_ids|tojson }};

const wellLabels = {{ well_labels|tojson }};
const wellValues = {{ well_values|tojson }};
const wellIds = {{ well_ids|tojson }};

const wellTypeLabels = {{ well_type_labels|tojson }};
const wellTypeValues = {{ well_type_values|tojson }};

const companyFilter = document.getElementById("companyFilter");
const wellFilter = document.getElementById("wellFilter");
// ==========================
// Filter handling
// ==========================

function applyFilters() {

    const company = companyFilter.value;
    const well = wellFilter.value;

    const params = new URLSearchParams();

    if (company)
        params.append("company_id", company);

    if (well)
        params.append("well_id", well);

    window.location = "?" + params.toString();
}

companyFilter.addEventListener("change", applyFilters);
wellFilter.addEventListener("change", applyFilters);

// ==========================
// Production Trend
// ==========================

new Chart(document.getElementById("productionChart"), {

    type: "line",

    data: {

        labels: productionLabels,

        datasets: [{

            label: "Чистая нефть",

            data: productionValues,

            borderWidth: 3,

            tension: 0.3,

            fill: false

        }]

    },

    options: {

        responsive: true,

        interaction: {
            mode: "index",
            intersect: false
        },

        plugins: {

            tooltip: {
                enabled: true
            }

        }

    }

});

// ==========================
// Water Cut
// ==========================

new Chart(document.getElementById("waterChart"), {

    type: "bar",

    data: {

        labels: waterLabels,

        datasets: [{

            label: "Обводненность (%)",

            data: waterValues

        }]

    },

    options: {

        responsive: true,

        plugins: {

            tooltip: {
                enabled: true
            }

        }

    }

});

// ==========================
// Company Production
// ==========================

new Chart(document.getElementById("companyChart"), {

    type: "bar",

    data: {

        labels: companyLabels,

        datasets: [{

            label: "Чистая нефть",

            data: companyValues

        }]

    },

    options: {

        responsive: true,

        plugins: {

            tooltip: {
                enabled: true
            }

        },

        onClick(event, elements) {

            if (!elements.length)
                return;

            const index = elements[0].index;

            window.location =
                "?company_id=" + companyIds[index];

        }

    }

});

// ==========================
// Well Production
// ==========================

new Chart(document.getElementById("wellChart"), {

    type: "bar",

    data: {

        labels: wellLabels,

        datasets: [{

            label: "Чистая нефть",

            data: wellValues

        }]

    },

    options: {

        responsive: true,

        plugins: {

            tooltip: {
                enabled: true
            }

        },

        onClick(event, elements) {

            if (!elements.length)
                return;

            const index = elements[0].index;

            const params = new URLSearchParams();

            if (companyFilter.value)
                params.append("company_id", companyFilter.value);

            params.append("well_id", wellIds[index]);

            window.location = "?" + params.toString();

        }

    }

});

// ==========================
// Well Types
// ==========================

new Chart(document.getElementById("wellTypeChart"), {

    type: "doughnut",

    data: {

        labels: wellTypeLabels,

        datasets: [{

            data: wellTypeValues

        }]

    },

    options: {

        responsive: true,

        plugins: {

            tooltip: {
                enabled: true
            }

        }

    }

});

// ==========================
// Company Share
// ==========================

new Chart(document.getElementById("companyShareChart"), {

    type: "pie",

    data: {

        labels: companyLabels,

        datasets: [{

            data: companyValues

        }]

    },

    options: {

        responsive: true,

        plugins: {

            tooltip: {
                enabled: true
            },

            legend: {
                position: "bottom"
            }

        }

    }

});

</script>