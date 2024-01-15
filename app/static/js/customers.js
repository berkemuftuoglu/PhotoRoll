function openEditModal(customerId, customerEmail, customerName, customerCompanyName, customerCompanyNumber, customerAddress) {
    // Fill the form fields with the current customer data
    document.getElementById('editCustomerId').value = customerId;
    document.getElementById('editCustomerEmail').value = customerEmail;
    document.getElementById('editCustomerName').value = customerName;
    document.getElementById('editCustomerCompanyName').value = customerCompanyName;
    document.getElementById('editCustomerCompanyNumber').value = customerCompanyNumber;
    document.getElementById('editCustomerAddress').value = customerAddress;

    // Open the modal
    document.getElementById('editCustomerModal').classList.add('is-active');
}

function closeEditModal() {
    // Close the modal
    document.getElementById('editCustomerModal').classList.remove('is-active');
}

const editCustomerForm = document.getElementById('editCustomerForm');
if (editCustomerForm) {
    editCustomerForm.addEventListener('submit', function(event) {
        event.preventDefault();
        
        // Extract data from the form
        const customerId = document.getElementById('editCustomerId').value;
        const customerEmail = document.getElementById('editCustomerEmail').value;
        const customerName = document.getElementById('editCustomerName').value;
        const customerCompanyName = document.getElementById('editCustomerCompanyName').value;
        const customerCompanyNumber = document.getElementById('editCustomerCompanyNumber').value;
        const customerAddress = document.getElementById('editCustomerAddress').value;

        // Update customer data in the database
        fetch('/update_customer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id: customerId,
                email: customerEmail,
                name: customerName,
                company_name: customerCompanyName,
                company_number: customerCompanyNumber,
                address: customerAddress
            })
        })
        .then(response => response.json())
        .then(data => {
            // Handle the response
            closeEditModal();
            // Refresh the part of the page with customer data or reload the page
            location.reload(); 
        })
        .catch(error => console.error('Error updating customer:', error));
    });
}
