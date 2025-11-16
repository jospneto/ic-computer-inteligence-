% --------------------------------
% Limpeza de fatos existentes
% --------------------------------
:- retractall(cacador(_,_,_)).
:- retractall(wumpus(_,_)).
:- retractall(buraco(_,_)).
:- retractall(ouro(_,_)).
:- retractall(pegar(_,_)).
:- retractall(acoes(_)).
:- retractall(atirou(_,_)).
:- retractall(visitado(_,_)).
:- retractall(loop(_)).

% --------------------------------
% Declarações dinâmicas
% --------------------------------
:- dynamic cacador/3.
:- dynamic wumpus/2.
:- dynamic buraco/2.
:- dynamic ouro/2.
:- dynamic pegar/2.
:- dynamic acoes/1.
:- dynamic atirou/2.
:- dynamic visitado/2.
:- dynamic loop/1.

:- multifile mundo/2.
:- multifile heuristica/2.

% --------------------------------
% Estado inicial
% --------------------------------
cacador(1, 1, leste).
visitado(1, 1).

% ---------------------------- %
% Predicados do ambiente       %
% ---------------------------- %

tem_ouro(sim) :-
    pegar(X, Y),
    ouro(X, Y), !.
tem_ouro(nao).

tem_flecha(nao) :-
    atirou(_, _), !.
tem_flecha(sim).

% ---------------- Percepções ----------------

tem_brilho(sim) :-
    tem_ouro(G),
    G == nao,
    cacador(X, Y, _),
    ouro(X, Y), !.
tem_brilho(nao).

tem_brisa(sim) :-
    (   cacador(X, Y, _),
        N is Y+1,
        buraco(X, N), !
    ;   cacador(X, Y, _),
        S is Y-1,
        buraco(X, S), !
    ;   cacador(X, Y, _),
        L is X+1,
        buraco(L, Y), !
    ;   cacador(X, Y, _),
        O is X-1,
        buraco(O, Y), !
    ).
tem_brisa(nao).

tem_fedor(sim) :-
    (   cacador(X, Y, _),
        N is Y+1,
        wumpus(X, N), !
    ;   cacador(X, Y, _),
        S is Y-1,
        wumpus(X, S), !
    ;   cacador(X, Y, _),
        L is X+1,
        wumpus(L, Y), !
    ;   cacador(X, Y, _),
        O is X-1,
        wumpus(O, Y), !
    ).
tem_fedor(nao).

tem_parede(sim) :-
    (   mundo(C, _),
        cacador(C, _, leste), !
    ;   mundo(_, L),
        cacador(_, L, norte), !
    ;   cacador(1, _, oeste), !
    ;   cacador(_, 1, sul), !
    ).
tem_parede(nao).

tem_grito(sim) :-
    wumpus_esta(morto), !.
tem_grito(nao).

% ---------------- Condições ----------------

jogador_esta(morto) :-
    cacador(X, Y, _),
    wumpus(X, Y), !.
jogador_esta(morto) :-
    cacador(X, Y, _),
    buraco(X, Y), !.
jogador_esta(vivo).

wumpus_esta(morto) :-
    atirou(X, Y),
    wumpus(X, Y), !.
wumpus_esta(vivo).

% ---------------- Utilitários ----------------

nas_fronteiras(X, Y) :-
    mundo(W, H),
    X > 0,
    X =< W,
    Y > 0,
    Y =< H.

percepcoes([Fedor, Brisa, Brilho, Parede, Grito]) :-
    tem_fedor(Fedor),
    tem_brisa(Brisa),
    tem_brilho(Brilho),
    tem_parede(Parede),
    tem_grito(Grito), !.

% ---------------- Movimentação ----------------

mover(X, Y) :-
    assertz(acoes(mover)),
    nas_fronteiras(X, Y),
    format("- Movendo-se para ~dx~d~n", [X, Y]),
    direcao(X, Y, D),
    retractall(cacador(_, _, _)),
    asserta(cacador(X, Y, D)),
    assertz(visitado(X, Y)), !.
mover(X, Y) :-
    format('!: Nao pode mover-se para ~dx~d~n', [X, Y]).

direcao(X, Y, D) :-
    cacador(Xi, Yi, _),
    X > Xi, Y == Yi, D = leste, !.
direcao(X, Y, D) :-
    cacador(Xi, Yi, _),
    X == Xi, Y > Yi, D = norte, !.
direcao(X, Y, D) :-
    cacador(Xi, Yi, _),
    X < Xi, Y == Yi, D = oeste, !.
direcao(X, Y, D) :-
    cacador(Xi, Yi, _),
    X == Xi, Y < Yi, D = sul, !.
direcao(_, _, D) :-
    cacador(_, _, D).

% ---------------- Ações ----------------

atirar(_, _) :-
    tem_flecha(nao),
    write('!: Nao tenho mais flechas.'), !.
atirar(X, Y) :-
    assertz(acoes(atirou)),
    tem_flecha(sim),
    assertz(atirou(X, Y)).

% Vizinhos
vizinhos(N) :-
    findall([X, Y], vizinhos(X, Y), N).

vizinhos(X, Y) :-
    cacador(Xi, Yi, _),
    L is Xi+1,
    nas_fronteiras(L, Yi),
    X = L, Y = Yi.
vizinhos(X, Y) :-
    cacador(Xi, Yi, _),
    S is Yi-1,
    nas_fronteiras(Xi, S),
    X = Xi, Y = S.
vizinhos(X, Y) :-
    cacador(Xi, Yi, _),
    N is Yi+1,
    nas_fronteiras(Xi, N),
    X = Xi, Y = N.
vizinhos(X, Y) :-
    cacador(Xi, Yi, _),
    O is Xi-1,
    nas_fronteiras(O, Yi),
    X = O, Y = Yi.

% Ações do jogador
acao(exit) :-
    write('Bye, bye!'), nl,
    imprime_resultado, nl,
    imprime_mundo, nl,
    abort.

acao([mover, X, Y]) :-
    mover(X, Y).

acao([atirar, X, Y]) :-
    atirar(X, Y).

acao(pegar) :-
    (   assertz(acoes(pegar)),
        cacador(X, Y, _),
        assertz(pegar(X, Y)),
        ouro(X, Y),
        tem_ouro(nao)
    ->  write('!: Encontrou ouro! '), nl
    ;   true
    ).

acao([virar, D]) :- 
    (
        D == esquerda, assertz(acoes([virar, esquerda])), cacador(X, Y, Di), 
        (
            Di == leste, Dj = norte, retractall(cacador(_, _, _)), asserta(cacador(X, Y, Dj));
            Di == norte, Dj = oeste, retractall(cacador(_, _, _)), asserta(cacador(X, Y, Dj));
            Di == oeste, Dj = sul, retractall(cacador(_, _, _)), asserta(cacador(X, Y, Dj));
            Di == sul, Dj = leste, retractall(cacador(_, _, _)), asserta(cacador(X, Y, Dj))
        );
        D == direita, assertz(acoes([virar, direita])), cacador(X, Y, Di), 
        (
            Di == leste, Dj = sul, retractall(cacador(_, _, _)), asserta(cacador(X, Y, Dj));
            Di == norte, Dj = leste, retractall(cacador(_, _, _)), asserta(cacador(X, Y, Dj));
            Di == oeste, Dj = norte, retractall(cacador(_, _, _)), asserta(cacador(X, Y, Dj));
            Di == sul, Dj = oeste, retractall(cacador(_, _, _)), asserta(cacador(X, Y, Dj))
        )
    ), !.

acao(adiante) :- 
    assertz(acoes(adiante)),
    (
        cacador(X, Y, D), nas_fronteiras(X, Y), D == leste, retractall(cacador(_, _, _)), L is X+1, asserta(cacador(L, Y, D));
        cacador(X, Y, D), nas_fronteiras(X, Y), D == norte, retractall(cacador(_, _, _)), N is Y+1, asserta(cacador(X, N, D));
        cacador(X, Y, D), nas_fronteiras(X, Y), D == oeste, retractall(cacador(_, _, _)), O is X-1, asserta(cacador(O, Y, D));
        cacador(X, Y, D), nas_fronteiras(X, Y), D == sul, retractall(cacador(_, _, _)), S is Y-1, asserta(cacador(X, S, D))
    ),
    assertz(visitado(X, Y)), !.

acao(random) :-
    vizinhos(N),
    length(N, L),
    random_between(1, L, R),
    nth1(R, N, [X, Y]),
    mover(X, Y).

acao(noop).

% ---------------- Pontuação ----------------

placar(S) :-
    findall(P, pontos(P), Ps),
    sum_list(Ps, S).

pontos(P) :-
    passos(T),
    P is -T.
pontos(P) :-
    jogador_esta(morto),
    P is -1000.
pontos(P) :-
    tem_ouro(sim),
    P is 1000.

passos(S) :-
    findall(A, acoes(A), As),
    length(As, S).

% ---------------- Impressão ----------------

imprime_resultado :-
    (   format('~n~tResult~t~40|~n'),
        placar(S),
        passos(T),
        format('Passos: ~`.t ~d~40|', [T]), nl,
        format('Placar: ~`.t ~d~40|', [S]), nl,
        tem_ouro(sim),
        cacador(1, 1, _)
    ->  format('Resultado: ~`.t ~p~40|', [ganhou]), nl
    ;   format('Resultado: ~`.t ~p~40|', [perdeu]), nl
    ).

imprime_mundo :-
    jogador_esta(P),
    cacador(Hx, Hy, _),
    format('~n~tmundo~t~40|~n'),
    format('Jogador: ~`.t ~p em ~dx~d~40|', [P, Hx, Hy]), nl,
    wumpus_esta(W),
    wumpus(Wx, Wy),
    format('Wumpus: ~`.t ~p em ~dx~d~40|', [W, Wx, Wy]), nl,
    tem_ouro(G),
    ouro(Gx, Gy),
    format('Ouro: ~`.t~p em ~dx~d~40|', [G, Gx, Gy]), nl,
    findall([Px, Py], buraco(Px, Py), Ps),
    format('Buraco: ~`.t ~p~40|', [Ps]), nl.

% ---------------- Execução ----------------

run(random) :-
    random_between(2, 4, X1), random_between(2, 4, Y1), assertz(ouro(X1, Y1)),
    random_between(2, 4, X2), random_between(2, 4, Y2), assertz(wumpus(X2, Y2)),
    random_between(2, 4, X3), random_between(2, 4, Y3), assertz(buraco(X3, Y3)),
    random_between(2, 4, X4), random_between(2, 4, Y4), assertz(buraco(X4, Y4)),
    random_between(2, 4, X5), random_between(2, 4, Y5), assertz(buraco(X5, Y5)),
    run.

run([Gx, Gy], [Wx, Wy], [P1x, P1y], [P2x, P2y], [P3x, P3y]) :-
    assertz(ouro(Gx, Gy)),
    assertz(wumpus(Wx, Wy)),
    assertz(buraco(P1x, P1y)),
    assertz(buraco(P2x, P2y)),
    assertz(buraco(P3x, P3y)),
    run.

run :-
    runloop(0).

runloop(100) :-
    write('!: Numero maximo de passos executado.'), nl,
    acao(exit), !.

runloop(T) :-
    (   cacador(X, Y, D),
        percepcoes(P),
        format('~d: Na posicao ~dx~d virado para ~p, as percepcoes sao ~p. ',
               [T, X, Y, D, P]),
        heuristica(P, A),
        format('Acao escolhida: ~p.~n', [A]),
        acao(A),
        jogador_esta(morto) ->  write('Voce morreu.'), nl,
        acao(exit), !
    ;   Ti is T+1,
        runloop(Ti)
    ).
