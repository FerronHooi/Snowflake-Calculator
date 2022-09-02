const feedDisplay = document.querySelector('#platforms')



fetch('http://localhost:8000/results')
    .then(response => response.json())
    .then(data => console.log(data))