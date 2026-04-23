
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

function getHotelsFromHTML() {

  const templates = document.querySelectorAll("#hotel-data .hotel");
  
  return Array.from(templates).map(template => {
    const content = template.content;
    
    return {
      name: content.querySelector(".name")?.textContent,
      city: content.querySelector(".city")?.textContent,
      price: content.querySelector(".price")?.textContent,
      desc: content.querySelector(".desc")?.textContent,
      location: content.querySelector(".location")?.textContent,
      rating: content.querySelector(".rating")?.textContent,

      features: Array.from(content.querySelectorAll(".features li"))
        .map(li => li.textContent),

      images: Array.from(content.querySelectorAll(".images img"))
        .map(img => img.src),
      
      amenities: content.querySelector(".amenities")?.innerHTML || ""
    };
  });
}

const hotels = getHotelsFromHTML();

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
        
        <div class="card-carousel" id="carousel-${index}">
          ${hotel.images.map((img, i) => `
            <img src="${img}" class="card-slide ${i === 0 ? 'active' : ''}">
          `).join("")}

          <button class="card-prev" onclick="moveSlide(${index}, -1)">❮</button>
          <button class="card-next" onclick="moveSlide(${index}, 1)">❯</button>
        </div>

        <div class="card-content">
          <h3>${hotel.name}</h3>
          <p class="city">${hotel.city}</p>
          <p>${hotel.desc.substring(0, 60)}...</p>
          <p class="price">${hotel.price}</p>

          <div class="card-buttons">
            <button class="btn-detalhes" onclick="openModal(${index})">
              Mais detalhes →
            </button>
            <button class="btn-preco">
              Ver Preços
            </button>
          </div>
        </div>

      </div>
    `;
  });
}

function openModal(index) {
  const hotel = hotels[index];

  modalBody.innerHTML = `
    
    <div class="modal-carousel">
      ${hotel.images.map((img, i) => `
        <img src="${img}" class="modal-slide ${i === 0 ? 'active' : ''}">
      `).join("")}

      <button class="modal-prev" onclick="moveModalSlide(-1)">❮</button>
      <button class="modal-next" onclick="moveModalSlide(1)">❯</button>
    </div>

    <h2>${hotel.name}</h2>

    <p class="location"><strong><i class="fa-solid fa-map-location-dot"></i> Localização:</strong> ${hotel.location || hotel.city}</p>
    <iframe class="map-container" map src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3988.5323893341506!2d-48.49157792417147!3d-1.4547272358351913!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x92a48f95cb9ab92b%3A0x647cbf2a05c04c00!2sRadisson%20Hotel%20Maiorana%20Belem!5e0!3m2!1spt-BR!2sbr!4v1776949026860!5m2!1spt-BR!2sbr" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
    <iframe class="map-container" map src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1185.8247202782486!2d-48.47094787885234!3d-1.4025211431133155!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x92a48b0051d506ed%3A0x8ec2a0a62d923724!2sAmazon%20Park%20Hotel!5e0!3m2!1spt-BR!2sbr!4v1776955594955!5m2!1spt-BR!2sbr" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
    <p class="desc">${hotel.desc}</p>

    <ul>
      ${hotel.features.map(f => `<li>✔ ${f}</li>`).join("")}
    </ul>

    ${hotel.amenities ? `
    <h3 class="comodidades">Comodidades</h3>
    <div class="amenities-grid">
    ${hotel.amenities}
    </div>
          ` : ""}

    <p class="price">${hotel.price}</p>

    <p class="nota"><strong>⭐ Nota:</strong> ${hotel.rating || "Sem avaliação"}</p>

    <button class="btn-preco"> Ver Preços </button>
  `;

  modal.style.display = "block";
}

closeModal.onclick = () => modal.style.display = "none";

window.onclick = (e) => {
  if (e.target === modal) modal.style.display = "none";
};

searchInput.addEventListener("input", (e) => {
  const value = e.target.value.toLowerCase();

  const filtered = hotels.filter(hotel =>
    hotel.name.toLowerCase().includes(value) ||
    hotel.city.toLowerCase().includes(value)
  );

  renderHotels(filtered);
});

/* CARROSSEL DOS CARDS */
const currentSlides = {};

function moveSlide(cardIndex, direction) {
  const carousel = document.getElementById(`carousel-${cardIndex}`);
  const slides = carousel.querySelectorAll(".card-slide");

  if (!currentSlides[cardIndex]) {
    currentSlides[cardIndex] = 0;
  }

  slides[currentSlides[cardIndex]].classList.remove("active");

  currentSlides[cardIndex] =
    (currentSlides[cardIndex] + direction + slides.length) % slides.length;

  slides[currentSlides[cardIndex]].classList.add("active");
}

renderHotels(hotels);

let modalIndex = 0;

function moveModalSlide(direction) {
  const slides = document.querySelectorAll(".modal-slide");

  slides[modalIndex].classList.remove("active");

  modalIndex = (modalIndex + direction + slides.length) % slides.length;

  slides[modalIndex].classList.add("active");
}