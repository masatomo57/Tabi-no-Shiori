document.querySelector("#add").addEventListener("click", () => {
    let table = document.getElementById("form_table");
    let newRow = table.insertRow();

    let newCell = newRow.insertCell();
    newCell.appendChild(document.createTextNode(extraFormAction));

    newCell = newRow.insertCell();
    newCell.appendChild(document.createTextNode(extraFormDate));

    newCell = newRow.insertCell();
    newCell.appendChild(document.createTextNode(extraFormStartTime + "~" + extraFormEndTime));
});
