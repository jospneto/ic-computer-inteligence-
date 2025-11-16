class Subject {
  constructor() {
    this.observers = [];
  }
  adicionar(observer) {
    this.observers.push(observer);
  }
  notificar(mensagem) {
    this.observers.forEach(obs => obs.atualizar(mensagem));
  }
}

class Observer {
  atualizar(mensagem) {
    console.log("Notificado:", mensagem);
  }
}

const canal = new Subject();
const usuario1 = new Observer();
const usuario2 = new Observer();

canal.adicionar(usuario1);
canal.adicionar(usuario2);

canal.notificar("Novo vídeo no canal 🎥");
