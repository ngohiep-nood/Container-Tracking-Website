let form = document.getElementById('form-data');

localStorage.clear()

form.addEventListener('submit', async(e) => {
    e.preventDefault();

    let form_data = new FormData(e.target)
    const resp = await fetch(e.target.action, {
        method: "POST",
        body: new URLSearchParams(form_data),
    });

    const body = await resp.json();

    if(body.status == 'success') {
        localStorage.setItem('access-token', body.access_token)
        localStorage.setItem('refresh-token', body.refresh_token)
        window.location.replace('http://localhost:3000/home/upload')
    } else {
        let myModal = new bootstrap.Modal(document.getElementById('modal-container'))
        document.getElementById('modal-body').innerHTML = body.message;
        myModal.toggle();
    }
})