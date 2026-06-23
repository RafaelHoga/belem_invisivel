let visitas = localStorage.getItem("visitas_apresentacao");

if (!visitas) {
    visitas = 0;
}

visitas++;

localStorage.setItem("visitas_apresentacao", visitas);

document.getElementById("contador").innerText = visitas;