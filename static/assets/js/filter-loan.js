const tbodyEl = document.getElementById('loans-table-body');
const statusEl = document.getElementById('filter-status');
const sdateEl = document.getElementById('filter-start-date');
const edateEl = document.getElementById('filter-end-date');
const toYMD = (date) => {
    const d = new Date(date);
    const yyyy = d.getFullYear();
    const mm = String(d.getMonth() + 1).padStart(2, '0'); // months are 0-indexed!
    const dd = String(d.getDate()).padStart(2, '0');
    return `${yyyy}-${mm}-${dd}`;
};
const empty_row = `<tr>
    <td colspan="9" class="text-center text-muted py-4">No loans match the
        filters.
    </td>
</tr>`;
const row = (l) => `<tr>
    <td className="font-weight-bold">${l.email}</td>
    <td className="font-weight-bold"> $${l.amount.toFixed(2)} </td>
    <td> ${l.interest_rate.toFixed(0)}%</td>
    <td> ${l.tenure_month} mo</td>
    <td> $${l.total_payable.toFixed(2)} </td>
    <td>
        <span class="badge badge-${l.status.toLowerCase()}">
            ${l.status}
        </span>
     </td>
    <td> ${toYMD(l.start_date)} </td>
    <td>
        <a href="${VIEW_LOAN_URL.replace('0', l.loan_id)}"
           class="btn btn-sm btn-gradient-info btn-icon-text mb-1 mb-md-0">
            <i class="mdi mdi-file-document mr-1"></i>Details
        </a>
    </td>
</tr>`;

const renderRows = (data) => {
    tbodyEl.innerHTML = (data && data.length > 0)
        ? data.map(row).join('')
        : empty_row;
};

const filter = (loan) => {
    console.log(`Data: ${loan}`)
}

[sdateEl, statusEl, edateEl].forEach(d => d.addEventListener('change', () => {
    const status = statusEl.value;
    const sdate = sdateEl.value;
    const edate = edateEl.value;
    const params = new URLSearchParams();
    tbodyEl.innerHTML = '';

    if (status && status !== 'all') params.set('status', status)
    if (sdate) params.set('sdate', sdate)
    if (edate) params.set('edate', edate)

    fetch(`/admin/loan/filter?${params.toString()}`).then(res => res.json())
        .then(renderRows)
}))