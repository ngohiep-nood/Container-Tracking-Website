let form = document.forms["form-data"];
const clearBtn = document.getElementById("clear-btn");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  let display = document.getElementById("display");
  let myModal = new bootstrap.Modal(document.getElementById('modal-container'))
  let form_data = new FormData(event.target);
  let cont_id = form_data.get("id").split(',')

  form_data.append("id_list", JSON.stringify(cont_id));
  
  const resp = await fetch(event.target.action, {
    method: "POST",
    body: new URLSearchParams(form_data),
  });
  const body = await resp.json();
  let err_message = []
  display.innerHTML = '';
  for(let r of body) {
    if(r.status == 'success') {
      
      let img_before = document.createElement("img");
      let img_after = document.createElement("img");
      let idElem = document.createElement("h3");
    
      idElem.innerText = "#CONTAINER ID: " + r.id;
      idElem.className = "col-12 text-center mt-2";
      display.classList.add(...['border', 'border-info', 'rounded', 'pb-2'])
      display.appendChild(idElem);
    
      img_before.src = r.img_before;
      img_after.src = r.img_after;
      img_after.className = img_before.className = "img-fluid col-5 mx-2";
      display.appendChild(img_before);
      display.appendChild(img_after);
    }else {
      console.log(r.message)
      err_message.push(r.err_id);
    }
  }

  if(err_message.length) {
    document.getElementById('modal-body').innerHTML = `Cannot find id: ${err_message.join(', ')}`;
    myModal.toggle();
  }
});

clearBtn.addEventListener("click", (e) => {
  e.preventDefault();
  display.innerHTML = "";
});
