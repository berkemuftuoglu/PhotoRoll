function openEditModal(serviceId, serviceName, serviceDescription) {
    document.getElementById('editServiceId').value = serviceId;
    document.getElementById('editServiceName').value = serviceName;
    document.getElementById('editServiceDescription').value = serviceDescription;
    document.getElementById('editServiceModal').classList.add('is-active');
}

function closeEditModal() {
    document.getElementById('editServiceModal').classList.remove('is-active');
}

const editServiceForm = document.getElementById('editServiceForm');
if (editServiceForm) {
    editServiceForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const serviceId = document.getElementById('editServiceId').value;
        const serviceName = document.getElementById('editServiceName').value;
        const serviceDescription = document.getElementById('editServiceDescription').value;

        fetch('/update_service', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id: serviceId,
                name: serviceName,
                description: serviceDescription
            })
        })
        .then(response => response.json())
        .then(data => {
            closeEditModal();
            location.reload();
        })
        .catch(error => console.error('Error updating service:', error));
    });
}

function filterTable() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("filterInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("servicesTable");
    tr = table.getElementsByTagName("tr");

    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[1]; // Index 1 for service name
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }       
    }
}