
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
      map: content.querySelector(".map-container")?.outerHTML || "",
      location: content.querySelector(".location")?.textContent,
      rating: content.querySelector(".rating")?.textContent,
      button: content.querySelector(".btn-preco")?.outerHTML,

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
          <p>${hotel.desc ? hotel.desc.substring(0, 60) + '...' : 'Sem descrição'}</p>
          <p class="price">${hotel.price}</p>

          <div class="card-buttons">
            <button class="btn-detalhes" onclick="openModal(${index})">
              Mais detalhes →
            </button>
            ${hotel.button || ""}
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
    ${hotel.map}
    <p class="desc">${hotel.desc}</p>
    ${hotel.amenities ? `
    <h3 class="comodidades">Comodidades</h3>
    <div class="amenities-grid">
    ${hotel.amenities}
    </div>
          ` : ""}

    <p class="price">${hotel.price}</p>

    <p class="nota"><strong>⭐ Nota:</strong> ${hotel.rating || "Sem avaliação"}</p>
     
    <div class="modal-footer">
      ${hotel.button || ""}
    </div>
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