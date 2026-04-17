const hotelList = document.getElementById("hotelList");
const search = document.getElementById("search");

let hotels = [];
let sliders = {};

// 🔥 BUSCAR DA API
fetch("http://localhost:3000/hoteis")
    .then(res => res.json())
    .then(data => {

        // adiciona imagens fake (pra funcionar bonito)
        hotels = data.map(h => ({
            ...h,
            imagens: [
                "https://source.unsplash.com/400x300/?hotel",
                "https://source.unsplash.com/400x300/?hotel-room",
                "https://source.unsplash.com/400x300/?hotel-lobby"
            ]
        }));

        mostrarHoteis(hotels);
    });

function mostrarHoteis(lista) {
    hotelList.innerHTML = "";

    lista.forEach((hotel, i) => {
        sliders[i] = { atual: 0 };

        const card = document.createElement("div");
        card.classList.add("card");

        const dots = hotel.imagens.map((_, index) =>
            `<span class="dot" onclick="irPara(${i}, ${index})"></span>`
        ).join("");

        card.innerHTML = `
            <div class="carousel">
                <div class="slides" id="slide-${i}">
                    ${hotel.imagens.map(img => `<img src="${img}">`).join("")}
                </div>

                <button class="prev" onclick="mudar(${i}, -1)">❮</button>
                <button class="next" onclick="mudar(${i}, 1)">❯</button>

                <div class="dots">${dots}</div>
            </div>

           <div class="card-content">
                <h2>${hotel.nome}</h2>
                <p>${hotel.descricao}</p>
                <p class="avaliacao">⭐ ${hotel.avaliacao}</p>
                <p class="price">A partir de R$ ${hotel.preco}</p>
                <button class="btn">Ver disponibilidade</button>
            </div>
        `;

        hotelList.appendChild(card);

        setTimeout(() => atualizarSlide(i), 50);
    });
}

// CONTROLES
function mudar(i, dir) {
    const total = hotels[i].imagens.length;
    sliders[i].atual = (sliders[i].atual + dir + total) % total;
    atualizarSlide(i);
}

function irPara(i, index) {
    sliders[i].atual = index;
    atualizarSlide(i);
}

function atualizarSlide(i) {
    const slide = document.getElementById(`slide-${i}`);
    slide.style.transform = `translateX(-${sliders[i].atual * 100}%)`;

    const dots = slide.parentElement.querySelectorAll(".dot");
    dots.forEach(d => d.classList.remove("active"));
    dots[sliders[i].atual].classList.add("active");
}

// BUSCA
search.addEventListener("input", () => {
    const valor = search.value.toLowerCase();
    const filtrados = hotels.filter(h =>
        h.nome.toLowerCase().includes(valor)
    );
    mostrarHoteis(filtrados);
});