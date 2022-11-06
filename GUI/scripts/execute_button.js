document.addEventListener("DOMContentLoaded", () => {
  const button = document.getElementById("button");
  const button_text = document.getElementById("button_text");
  const ripple = document.getElementById("ripple");

  const title = document.getElementById("title");

  const cards = document.getElementById("cards");
  const card_1 = document.getElementById("card_1");
  const card_2 = document.getElementById("card_2");
  const more = document.getElementById("more");

  const card_info = document.getElementById("card_information");

  var clicked = false;
  button.onclick = () => {
    if (!clicked) {
      clicked = true;
      button.classList.add("activated");
      button_text.innerHTML = "";
      setTimeout(() => {
        ripple.style.display = "inline-block";
      }, 100);

      fill_table();

      setTimeout(() => {
        ripple.style.display = "none";
        button.classList.add("scanned");
        title.classList.add("hide");

        setTimeout(() => {
          cards.style.display = "flex";
          card_1.classList.add("show");
          card_2.classList.add("show");
          more.classList.add("show");
        }, 1000);
      }, 1000);
    }
  };

  more.onclick = () => {
    document.getElementById("card_information").style.display = "contents";
    card_info.classList.add("show");
    cards.style.display = "none";
  };
});

var divs = [];
var important_info = [0, 0, 0, 0]; // name, bank, number, date

function loop_json(tab, rows, values) {
  for (let key in rows) {
    if (key == "5F20") {
      important_info[0] = rows[key];
    } else if (key == "50") {
      important_info[1] = rows[key];
    } else if (key == "5A") {
      important_info[2] = rows[key];
    } else if (key == "5F24") {
      //date
      var date = rows[key];
      important_info[3] = date;
    }

    var div1 = document.createElement("div");
    div1.classList.add("row");

    var div2 = document.createElement("div");
    div2.classList.add("top");

    var p1 = document.createElement("p1");
    p1.classList.add("code");
    p1.innerHTML = key;

    var a = document.createElement("a");
    a.classList.add("code_name");
    a.innerHTML = values[key][0];
    a.target = "_blank";
    a.href = values[key][1];

    div2.append(p1);
    div2.append(a);
    div1.append(div2);
    div1.style.margin = `20px 0 20px ${50 * tab}px`;

    if (rows[key] != "") {
      if (typeof rows[key] == "string") {
        var p2 = document.createElement("p");
        p2.classList.add("info");
        p2.innerHTML = rows[key];
        div1.append(p2);
      } else {
        loop_json(tab + 1, rows[key], values);
      }
    }

    divs.push(div1);
  }
}

function fill_table() {
  const TABLE = document.getElementById("table");

  // fetch("./scripts/json_data.json")
  fetch("./scripts/prueba.json")
    .then((results) => results.json())
    .then((data) => {
      const rows = data["rows"];
      const values = data["value"];
      const _6F_ = rows["6F"];
      const _70_ = rows["70"];
      for (const row of _6F_) {
        loop_json(0, row, values);
      }
      for (const row of _70_) {
        loop_json(0, row, values);
      }

      for (let i = divs.length - 1; i >= 0; i--) {
        TABLE.append(divs[i]);
      }

      const bank = document.getElementById("bank_name");
      const number = document.getElementById("card_number");
      const name = document.getElementById("cardholder_name");
      const date = document.getElementById("date");
      console.log(important_info[1]);
      bank.innerHTML = `${important_info[1]}`;
      number.innerHTML = `${important_info[2]}`;
      name.innerHTML = `${important_info[0]}`;
      date.innerHTML = `${important_info[3]}`;
    });
}
