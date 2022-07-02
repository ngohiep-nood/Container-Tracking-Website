let form = document.forms["form-data"];

container_id_list = [];

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  let form_data = new FormData(event.target);
  const cont_id = form_data.get("id")
  for(let i of container_id_list) {
    if(i == cont_id) {
      console.log("container id has already been existed!");
      return 0;
    }
  }
  const resp = await fetch(event.target.action, {
    method: "POST",
    body: new URLSearchParams(form_data),
  });
  const body = await resp.json();
  // console.log(body);
  if(body.status == 'success') {
    let display = document.getElementById("display");
    let img_before = document.createElement("img");
    let img_after = document.createElement("img");
    let idElem = document.createElement("h3");
  
    idElem.innerText = "#CONTAINER ID " + body.id;
    idElem.className = "col-12 text-center mt-2";
    display.appendChild(idElem);
  
    img_before.src = body.img_before;
    img_after.src = body.img_after;
    img_after.className = img_before.className = "img-fluid col-5 mx-2";
    display.appendChild(img_before);
    display.appendChild(img_after);
  
    container_id_list.push(cont_id);
  }else {
    const myModal = new bootstrap.Modal(document.getElementById('modal-container'))
    document.getElementById('modal-label').innerText = 'Something went wrong!';
    document.getElementById('modal-body').innerHTML = body.message;
    myModal.toggle();
  }
});

const clearBtn = document.getElementById("clear-btn");

clearBtn.addEventListener("click", (e) => {
  e.preventDefault();
  container_id_list = [];
  display.innerHTML = "";
});
