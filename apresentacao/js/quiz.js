const quiz = [
{
q: "Qual prato é típico do Pará?",
op: ["Tacacá", "Pizza", "Hambúrguer"],
c: 0
},
{
q: "Qual é um ponto turístico natural?",
op: ["Parque do Utinga", "Shopping", "Cinema"],
c: 0
}
];

let atual = 0;
let pontos = 0;

function carregar() {
const p = quiz[atual];

document.getElementById("pergunta").innerText = p.q;

document.getElementById("opcoes").innerHTML =
p.op.map((o, i) =>
`<button onclick="responder(${i})">${o}</button>`
).join("");
}

function responder(i) {
if (i === quiz[atual].c) pontos++;

atual++;

if (atual < quiz.length) {
carregar();
} else {
document.getElementById("quiz").innerHTML = `
<h2>Resultado</h2>
<p>Pontos: ${pontos}/${quiz.length}</p>
`;
}
}

carregar();