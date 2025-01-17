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