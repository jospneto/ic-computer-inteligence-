class Veiculo {
  dirigir() {}
}

class Carro extends Veiculo {
  dirigir() { console.log("Dirigindo um carro 🚗"); }
}

class Moto extends Veiculo {
  dirigir() { console.log("Pilotando uma moto 🏍️"); }
}

function veiculoFactory(tipo) {
  if (tipo === "carro") return new Carro();
  if (tipo === "moto") return new Moto();
}

const v1 = veiculoFactory("carro");
v1.dirigir(); // Dirigindo um carro 🚗
