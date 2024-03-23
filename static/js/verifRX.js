function validateInput(value) {
    if (!/^\d+(\.\d+)?$/.test(value)) {
        return false;
    }
    let numberValue = parseFloat(value);
    let decimalPart = numberValue % 1;
    
    if (decimalPart !== 0 && decimalPart !== 0.25 && decimalPart !== 0.5 && decimalPart !== 0.75) {
        return false;
    }
    return true;
}