# Belém Invisível

Projeto Integrador desenvolvido no **SENAC - Belém (PA)** com o objetivo de promover o turismo local, destacando hospedagens, restaurantes e pontos turísticos da cidade de forma moderna, acessível e intuitiva.

---

## Objetivo do Projeto

O **Belém Invisível** foi criado para:

- Facilitar a descoberta de pontos turísticos da cidade  
- Centralizar informações sobre hotéis e restaurantes  
- Oferecer uma experiência digital amigável e moderna  
- Valorizar o turismo local com tecnologia  

---

## Tecnologias Utilizadas

### Frontend
- HTML5  
- CSS3  
- JavaScript  

### Backend
- Python  
- Django  

### Banco de Dados
- MySQL  

---

## Arquitetura do Projeto

O projeto segue o padrão **MVC (Model-View-Controller)** utilizando Django:

- **Models:** representam os dados (Hotéis, Restaurantes, Usuários)  
- **Views:** lógica de negócio e controle  
- **Templates:** interface com HTML + CSS + JS  

### Estrutura de Pastas

```bash
beleminvisivel/
│
├── core/                # Configurações do Django
├── apps/
│   ├── turismo/         
│   ├── hoteis/         
│   ├── restaurantes/   
│
├── templates/          
├── static/             
├── media/              
│
├── manage.py