const express = require("express");
const cors = require("cors");

const app = express();
app.use(cors());

app.get("/hoteis", (req, res) => {
    res.json([
        {
            nome: "Atrium Quinta de Pedras",
            descricao: "Hotel histórico no centro",
            preco: 390,
            avaliacao: 4.1
        },
        {
            nome: "Mercure Belém Boulevard",
            descricao: "Conforto e modernidade",
            preco: 440,
            avaliacao: 4.1
        },
        {
            nome: "Radisson Hotel Belém",
            descricao: "Luxo e ótima localização",
            preco: 403,
            avaliacao: 4.4
        },
        {
            nome: "Ibis Styles Belém Batista Campos",
            descricao: "Econômico e moderno",
            preco: 303,
            avaliacao: 4.0
        },
        {
            nome: "Hotel Princesa Louçã",
            descricao: "Clássico no centro",
            preco: 350,
            avaliacao: 4.2
        },
        {
            nome: "Hotel Sagres",
            descricao: "Piscina e estrutura completa",
            preco: 280,
            avaliacao: 4.0
        },
        {
            nome: "Ibis Belém Aeroporto",
            descricao: "Prático e acessível",
            preco: 220,
            avaliacao: 3.9
        },
        {
            nome: "Golden Tulip Belém",
            descricao: "Vista e conforto premium",
            preco: 410,
            avaliacao: 4.3
        }
    ]);
});

app.listen(3000, () => {
    console.log("API rodando em http://localhost:3000");
}); 