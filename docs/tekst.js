function clearAllInputFields() {
  // find all divs with id starting with "warehouse-button" and hide them
  var currentNumber = String(button.id).slice(-1);
  document.getElementById("number-of-days-select-" + currentNumber).value =
    null;
  document.getElementById("number-of-hours-day-select-" + currentNumber).value =
    null;
  document.getElementById("percentage-bezetting-" + currentNumber).value = null;
  document.getElementById("warehouse-type-" + currentNumber).innerHTML =
    "Small";
  document.getElementById(
    "warehouse-size-number-" + currentNumber
  ).innerHTML = 2;
  document.getElementById("total-hours-1").innerHTML = "0 uren p/m";
  document.getElementById("total-credits-1").innerHTML = "0 credits p/m";
  document.getElementById("input-storage-tb-per-month").value = null;
}
