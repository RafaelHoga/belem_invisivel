const lugares = [
{
nome: "Ilha do Combu",
desc: "Natureza, chocolate artesanal e rios amazônicos."
},
{
nome: "Parque do Utinga",
desc: "Trilhas ecológicas e contato com a floresta urbana."
},
{
nome: "Mercado de São Brás",
desc: "Cultura popular e gastronomia local."
},
{
nome: "Estação das Docas",
desc: "Vista da baía com restaurantes e cultura."
}
];

function sortear() {
const item = lugares[Math.floor(Math.random() * lugares.length)];

document.getElementById("resultado").innerHTML = `
<div class="card">
<h2>${item.nome}</h2>
<p>${item.desc}</p>
</div>
`;
}