
const carousel = document.getElementById("carouselImages");
const slides = document.querySelectorAll(".slide");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");
const dotsContainer = document.getElementById("dots");

let index = 0;

/* Criar bolinhas */
slides.forEach((_, i) => {
  const dot = document.createElement("span");
  dot.addEventListener("click", () => {
    index = i;
    updateCarousel();
  });
  dotsContainer.appendChild(dot);
});

const dots = document.querySelectorAll(".dots span");

function updateCarousel() {
  carousel.style.transform = `translateX(-${index * 100}%)`;

  dots.forEach(dot => dot.classList.remove("active"));
  dots[index].classList.add("active");
}

nextBtn.addEventListener("click", () => {
  index = (index + 1) % slides.length;
  updateCarousel();
});

prevBtn.addEventListener("click", () => {
  index = (index - 1 + slides.length) % slides.length;
  updateCarousel();
});

/* Auto */
setInterval(() => {
  index = (index + 1) % slides.length;
  updateCarousel();
}, 5000);

updateCarousel();
const hotels = [
  {
    name: "Hotel Amazon Plaza",
    city: "Belém",
    price: "R$ 250/noite",
    desc: "Hotel confortável no centro da cidade com café da manhã incluso.",
    img: "https://source.unsplash.com/400x300/?hotel"
  },
  {
    name: "Grand Mercure Belém",
    city: "Belém",
    price: "R$ 420/noite",
    desc: "Hotel premium com piscina, academia e vista para o rio.",
    img: "https://source.unsplash.com/400x300/?resort"
  },
  {
    name: "Ibis Styles Belém",
    city: "Belém",
    price: "R$ 180/noite",
    desc: "Opção econômica e moderna perto do centro.",
    img: "https://source.unsplash.com/400x300/?room"
  },
  {
    name: "Hotel Tropical",
    city: "Belém",
    price: "R$ 300/noite",
    desc: "Ambiente tropical com área de lazer e restaurante.",
    img: "https://source.unsplash.com/400x300/?beach-hotel"
  },
  {
    name: "Hotel Nazaré Palace",
    city: "Belém",
    price: "R$ 220/noite",
    desc: "Localizado próximo à Basílica de Nazaré.",
    img: "https://source.unsplash.com/400x300/?building"
  },
  {
    name: "Riverside Hotel",
    city: "Belém",
    price: "R$ 380/noite",
    desc: "Vista incrível para o rio com quartos luxuosos.",
    img: "https://source.unsplash.com/400x300/?river-hotel"
  }
];

const hotelList = document.getElementById("hotelList");
const searchInput = document.getElementById("searchInput");

const modal = document.getElementById("modal");
const modalBody = document.getElementById("modalBody");
const closeModal = document.getElementById("closeModal");

function renderHotels(list) {
  hotelList.innerHTML = "";

  list.forEach((hotel, index) => {
    hotelList.innerHTML += `
      <div class="card">
        <img src="${hotel.img}">
        <div class="card-content">
          <h3>${hotel.name}</h3>
          <p>${hotel.city}</p>
          <p>${hotel.desc.substring(0, 60)}...</p>
          <p class="price">${hotel.price}</p>
          <button onclick="openModal(${index})">Ver mais</button>
        </div>
      </div>
    `;
  });
}

function openModal(index) {
  const hotel = hotels[index];

  modalBody.innerHTML = `
    <h2>${hotel.name}</h2>
    <p><strong>Cidade:</strong> ${hotel.city}</p>
    <p>${hotel.desc}</p>
    <p class="price">${hotel.price}</p>
  `;

  modal.style.display = "block";
}

closeModal.onclick = () => {
  modal.style.display = "none";
};

window.onclick = (e) => {
  if (e.target == modal) {
    modal.style.display = "none";
  }
};

searchInput.addEventListener("input", (e) => {
  const value = e.target.value.toLowerCase();

  const filtered = hotels.filter(hotel =>
    hotel.name.toLowerCase().includes(value) ||
    hotel.city.toLowerCase().includes(value)
  );

  renderHotels(filtered);
});

renderHotels(hotels);