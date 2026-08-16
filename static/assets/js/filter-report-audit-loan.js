const tbodyEl = document.getElementById('report-table-body');
const statusEl = document.getElementById('rep-status');
const sdateEl = document.getElementById('rep-start');
const edateEl = document.getElementById('rep-end');
const emptyRow = `<tr>
    <td colspan="8" class="text-center text-muted py-4">No loan records match the
        query.
    </td>
</tr>`;

[sdateEl, statusEl, edateEl].forEach(a => a.addEventListener('change', () => {
    const status = statusEl.value;
    const sdate = sdateEl.value;
    const edate = edateEl.value;
    const params = new URLSearchParams();
    tbodyEl.innerHTML = '';

    if (status && status !== 'all') params.set('report_status', status);
    if (sdate) params.set('report_sdate', sdate);
    if (edate) params.set('report_edate', edate);

    fetch(`/admin/report/filter?${params.toString()}`)
        .then(res => res.json())
        .then(data => {
            if (data && data.length > 0) {
                data.map(l => {
                    tbodyEl.innerHTML += `<tr>
                                    <td class="font-weight-bold">${l.email}</td>
                                    <td>$${l.amount.toFixed(2)}</td>
                                    <td>${l.interest_rate}%</td>
                                    <td>${l.tenure_month} mo</td>
                                    <td class="font-weight-bold text-dark">
                                        $${l.total_payable.toFixed(2)}
                                    </td>
                                    <td><span class="badge badge-${l.status}">${l.status}</span></td>
                                    <td>${new Date(l.start_date).toISOString().split("T")[0]}</td>
                                  </tr>`;
                }).join('')
            } else {
                tbodyEl.innerHTML += emptyRow
            }


        })
}));