function makeRandomNumbers(count){
    const numbers = new Set();
    while(numbers.size <count){
        const randomNum = Math.floor(Math.random()*10)+1;
        numbers.add(randomNum);
    }

    return Array.from(numbers).sort((a, b) => a - b);
}

const randomCardNums = makeRandomNumbers(5);
randomCardNums.forEach((number, index)=>{
    const inputElement = document.getElementById(`card_number_${index+1}`);
    const labelElement = inputElement.nextElementSibling;

    inputElement.value = number;
    labelElement.textContent = number;
})

let checked_value = 0;
let checked_defender = 0;
const cards = document.querySelectorAll('.card_number');
const defender = document.querySelector('#choice_defender');

cards.forEach((card) => {
    card.addEventListener("change", (e) => {
        if (e.target.checked) {
            checked_value = e.target.value; 
        }
    });
});

defender.addEventListener("change", ()=>{
    checked_defender = defender.value;
    //console.log(checked_defender)
})


