
const pontos = [
  { lat: -1.4558, lng: -48.4902, nome: "Ver-o-Peso", desc: "O maior mercado a céu aberto da América Latina", cor: "#1D9E75", icone: "🛒" },
  { lat: -1.4561, lng: -48.5028, nome: "Estação das Docas", desc: "Complexo turístico e cultural às margens da Baía do Guajará", cor: "#378ADD", icone: "⚓" },
  { lat: -1.4515, lng: -48.4928, nome: "Teatro da Paz", desc: "Teatro neoclássico inaugurado em 1878, ícone da Belle Époque amazônica", cor: "#7F77DD", icone: "🎭" },
  { lat: -1.4543, lng: -48.5042, nome: "Forte do Castelo", desc: "Forte histórico de 1616, ponto de fundação da cidade", cor: "#D85A30", icone: "🏰" },
  { lat: -1.4620, lng: -48.4989, nome: "Basílica de Nazaré", desc: "Igreja que sedia o Círio de Nazaré, a maior procissão católica do mundo", cor: "#E24B4A", icone: "⛪" },
  { lat: -1.4506, lng: -48.4964, nome: "Museu do Estado do Pará", desc: "Palácio histórico com acervo cultural e artístico do Pará", cor: "#BA7517", icone: "🏛️" },
  { lat: -1.2593841480153865, lng: -48.558876029730975, nome: "ilha de cotijuba", desc: "A Ilha de Cotijuba é uma ilha turística de Belém conhecida pelas praias de água doce, natureza e clima tranquilo, sendo um dos destinos mais visitados da região.", cor:"#378ADD", icone:"⚓"},
  { lat: -1.4386, lng: -48.4719, nome: "Hotel Ibis", desc: "Hotel moderno localizado na Av. Duque de Caxias, no bairro Marco.", cor: "#1D9E75", icone: "🏨"},
  { lat: -1.4455, lng: -48.4782, nome: "Hotel Ipe", desc: "Hotel localizado na Av. Governador José Malcher, no bairro São Brás.", cor: "#1D9E75", icone: "🏨"},
  {
    lat: -1.4550,
    lng: -48.4894,
    nome: "Belém Soft Hotel",
    desc: "Hotel localizado na Av. Brás de Aguiar, no bairro Nazaré.",
    cor: "#1D9E75",
    icone: "🏨"
  },
  // LUGARES TURÍSTICOS
  {
    lat: -1.4561,
    lng: -48.5028,
    nome: "Estação das Docas",
    desc: "Complexo turístico às margens da Baía do Guajará.",
    cor: "#378ADD",
    icone: "⚓"
  },

  {
    lat: -1.5165,
    lng: -48.5042,
    nome: "Ilha do Combu",
    desc: "Ilha localizada no Rio Guamá, famosa pelos restaurantes e natureza.",
    cor: "#378ADD",
    icone: "🌿"
  },

  // RESTAURANTES
  {
    lat: -1.4517,
    lng: -48.5010,
    nome: "Casa do Saulo",
    desc: "Restaurante paraense localizado no Espaço Cultural Casa das Onze Janelas.",
    cor: "#D85A30",
    icone: "🍽️"
  },

  {
    lat: -1.4477,
    lng: -48.4859,
    nome: "Estilo Bistrô",
    desc: "Bistrô sofisticado localizado na Travessa Wandenkolk.",
    cor: "#D85A30",
    icone: "🍷"
  },

  {
    lat: -1.4558,
    lng: -48.4872,
    nome: "Família Sicilia",
    desc: "Restaurante italiano localizado na Av. Conselheiro Furtado.",
    cor: "#D85A30",
    icone: "🍝"
  }

];
 
const categorias = [
  { cor: "#1D9E75", label: "Mercado" },
  { cor: "#378ADD", label: "Turismo" },
  { cor: "#7F77DD", label: "Cultura" },
  { cor: "#D85A30", label: "História" },
  { cor: "#E24B4A", label: "Religião" },
  { cor: "#BA7517", label: "Museu" },
  { cor: "#BA7517", label: "Museu" },
];
 
const legend = document.getElementById("legend");
categorias.forEach(c => {
  const el = document.createElement("div");
  el.style.cssText = `display:flex;align-items:center;gap:6px;font-size:13px;color:var(--color-text-secondary);`;
  el.innerHTML = `<span style="width:10px;height:10px;border-radius:50%;background:${c.cor};display:inline-block;"></span>${c.label}`;
  legend.appendChild(el);
});
 
const map = L.map("map", { zoomControl: true }).setView([-1.4558, -48.4902], 14);
 
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  maxZoom: 19,
}).addTo(map);
 
pontos.forEach(p => {
  const icon = L.divIcon({
    className: "",
    html: `<div style="background:${p.cor};width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:18px;border:2.5px solid #fff;box-shadow:0 2px 6px rgba(0,0,0,0.25);">${p.icone}</div>`,
    iconSize: [36, 36],
    iconAnchor: [18, 18],
    popupAnchor: [0, -20],
  });
 
  L.marker([p.lat, p.lng], { icon })
    .addTo(map)
    .bindPopup(`
      <div style="font-family:sans-serif;min-width:180px;">
        <div style="font-size:15px;font-weight:500;margin-bottom:4px;">${p.icone} ${p.nome}</div>
        <div style="font-size:13px;color:#555;line-height:1.5;">${p.desc}</div>
      </div>
    `, { maxWidth: 240 });
});

// FORMULÁRIO

let form = document.getElementById("formContato");

form.addEventListener("submit", function (event) {

  event.preventDefault();

  let nome = document.getElementById("nome").value.trim();
  let email = document.getElementById("email").value.trim();
  let mensagem = document.getElementById("mensagem").value.trim();

  let feedback = document.getElementById("feedback");

  if (nome === "" || email === "" || mensagem === "") {
    feedback.innerText = "Preencha todos os campos!";
    feedback.style.color = "red";
    return;
  }

  feedback.innerText = "Mensagem enviada com sucesso! 🐶";
  feedback.style.color = "green";

  form.reset();
});

