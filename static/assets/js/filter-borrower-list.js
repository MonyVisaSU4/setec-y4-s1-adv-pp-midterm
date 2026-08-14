const inputEl = document.getElementById("input-filter-search");
const format = (date) => {
    const getDate = new Date(date);
    const format = getDate.toISOString().split("T")[0];

    return format;
}

const handleInputFilterChange = () => {
    const tbody = document.getElementById("customers-table-body");
    tbody.innerHTML = '';
    const input = inputEl.value;

    fetch(`/admin/borrower/filter`)
        .then(res => res.json())
        .then(data => {

            if (!data || data.length === 0) {
                tbody.innerHTML += `<tr>
                    <td colspan="6" class="text-center text-muted py-4">No borrowers found.</td>
                </tr>`;
            }

            data.filter(f => f.email.toLowerCase().includes(input)).map(l => tbody.innerHTML += `<tr>
                        <td class="font-weight-bold">
                            <i class="mdi mdi-account-circle mr-2 text-primary"
                               style="font-size:1.2rem;"></i>
                            ${l.email}
                        </td>
                        <td><code>${l.national_id}</code></td>
                        <td>${l.phone}</td>
                        <td>${l.address}</td>
                        <td>${format(l.created_at)}</td>
                        <td>
                            <a href="${VIEW_BORROWER_URL.replace('/0', '/' + l.customer_id)}"
                               class="btn btn-sm btn-gradient-info btn-icon-text mb-1 mb-md-0"
                               title="View details and loans">
                                <i class="mdi mdi-eye mr-1"></i> View
                            </a>
                            <a href="${EDIT_BORROWER_URL.replace('/0', '/' + l.customer_id)}"
                               class="btn btn-sm btn-gradient-dark btn-icon-text mb-1 mb-md-0"
                               title="Edit Profile">
                                <i class="mdi mdi-lead-pencil mr-1"></i> Edit
                            </a>
                            <button class="btn btn-sm btn-gradient-danger btn-icon-text"
                                    title="Delete Account"
                                    onclick="handleSweetAlert(${l.customer_id}, 'borrower')">
                                <i class="mdi mdi-delete mr-1"></i> Delete
                            </button>
                        </td>
                    </tr>`)
        })
}

inputEl.addEventListener('input', handleInputFilterChange);

handleInputFilterChange();