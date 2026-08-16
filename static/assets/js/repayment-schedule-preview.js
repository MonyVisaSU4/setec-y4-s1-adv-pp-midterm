const tbodyEl = document.getElementById('preview-schedule-body');
const borrowerSelectEl = document.getElementById('customer_id');
const principleEl = document.getElementById('amount');
const interestEl = document.getElementById('interest_rate');
const tenureEl = document.getElementById('tenure_months');
const startDateEl = document.getElementById('start_date');

const handlePreview = () => {
    const borrowerSelect = borrowerSelectEl.value;
    const principle = principleEl.value;
    const interest = interestEl.value;
    const tenure = tenureEl.value;
    const startDate = new Date(startDateEl.value);
    const tenure_year = tenure / 12
    const total_interest = principle * (interest / 100) * tenure_year
    const total_payable = principle + total_interest
    const amount_due = total_payable / tenure;
    tbodyEl.innerHTML = '';

    const repaymentSchedule = []

    for (var i = 0; i < tenure; i++) {
        const dueDate = new Date(startDate);
        dueDate.setMonth(dueDate.getMonth() + i + 1);

        repaymentSchedule.push({
            due_date: dueDate,
            amount_due: amount_due
        })
    }

    if (repaymentSchedule.length > 0) {
        tbodyEl.innerHTML += repaymentSchedule.map(r => `
            <tr>
                <td class="font-weight-bold">${r.due_date.toISOString().split('T')[0]}</td>
                <td>$${r.amount_due.toFixed(2)}</td>
            </tr>
        `).join('');
    } else {
        tbodyEl.innerHTML += `
            <tr>
                <td class="font-weight-bold">---</td>
                <td class="font-weight-bold">---</td>
            </tr>
        `;
    }
}

[startDateEl, interestEl, tenureEl, borrowerSelectEl, principleEl].forEach(
    el => el.addEventListener('change', () => handlePreview())
)

handlePreview();