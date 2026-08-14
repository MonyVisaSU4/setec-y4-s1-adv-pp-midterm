const pricipleEL = document.getElementById('amount');
const interestEL = document.getElementById('interest_rate');
const tenureEL = document.getElementById('tenure_months');

const handleCal = () => {
    const priciple = parseFloat(pricipleEL.value);
    const interest = parseFloat(interestEL.value);
    const tenure = parseFloat(tenureEL.value);
    const emi = document.getElementById('calc-emi');
    const payable = document.getElementById('calc-total');
    const totalInterest = document.getElementById('calc-interest');

    if (!priciple || !interest || !tenure) {
        emi.innerText = '---';
        payable.innerText = '---';
        totalInterest.innerText = '---';
    } else {
        const caltotalInterest = priciple * (interest / 100) * (tenure / 12);
        const calpayable = priciple + caltotalInterest;
        const calemi = calpayable / tenure;

        emi.innerText = '$' + calemi.toFixed(2);
        payable.innerText = '$' + calpayable.toFixed(2);
        totalInterest.innerText = caltotalInterest.toFixed(2);
    }
}

[pricipleEL, interestEL, tenureEL].forEach(el =>
    el.addEventListener('input' || 'change', () => {
        handleCal();
    }))

handleCal();