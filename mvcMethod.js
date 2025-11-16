// Model
const usuario = { nome: "Ana", idade: 22 };

// View
function mostrarUsuario(usuario) {
  console.log(`Usuário: ${usuario.nome}, Idade: ${usuario.idade}`);
}

// Controller
function atualizarIdade(usuario, novaIdade) {
  usuario.idade = novaIdade;
  mostrarUsuario(usuario);
}

mostrarUsuario(usuario);
atualizarIdade(usuario, 23); // Usuário: Ana, Idade: 23
