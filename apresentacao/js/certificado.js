function gerar() {
const nome = document.getElementById("nome").value;

if (!nome) return;

document.getElementById("cert").innerHTML = `
<div class="card">
<h2>Certificado de Explorador</h2>
<p>${nome} participou da experiência Belém Invisível.</p>
<p>✔ Cultura<br>✔ Gastronomia<br>✔ Turismo local</p>
</div>
`;
}