let get_id = 0;
const amountDueEl = document.getElementById('modalAmountDue');
const amountPaidEl = document.getElementById('modalRepayAmount');
const paidDateEl = document.getElementById('modalPayDate');
const repaymentForm = document.getElementById('repaymentForm');

function showModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.classList.add('show');
    modal.style.display = 'block';
    document.body.classList.add('modal-open');

    const backdrop = document.createElement('div');
    backdrop.className = 'modal-backdrop fade show';
    backdrop.id = modalId + '-backdrop';
    document.body.appendChild(backdrop);
}

function hideModal() {
    const modal = document.getElementById('repaymentModal');
    modal.classList.remove('show');
    modal.style.display = 'none';
    document.body.classList.remove('modal-open');

    const backdrop = document.getElementById('repaymentModal-backdrop');
    if (backdrop) backdrop.remove();
}

// Called from the "Repay" button in the table: onclick="handleRepayment({{ o.id }})"
function handleRepayment(id) {
    fetch(`/admin/loan/repay/${id}`)
        .then(res => res.json())
        .then(data => {
            get_id = id;
            amountDueEl.value = data['modal_amount_due'];
            amountPaidEl.value = '';
            paidDateEl.value = data['modal_pay_date'];
            showModal('repaymentModal');
        })
        .catch(err => console.error('Failed to load repayment info:', err));
}

// Handles the actual "Record Payment" submit
repaymentForm.addEventListener('submit', function (e) {
    e.preventDefault();
    fetch(`/admin/loan/repay/${get_id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
            modalRepayAmount: amountPaidEl.value,
            modalPayDate: paidDateEl.value
        })
    })
        .then(res => res.json())
        .then(() => {
            hideModal();
            location.reload(); // simplest way to refresh the table with new data
        })
        .catch(err => console.error('Failed to submit repayment:', err));
});