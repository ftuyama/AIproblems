clear all
clc

% 1) Criar Padrões de Entrada/Saída
camargos=load('CamargosR.txt');          % Vetor 82 x 12 (de 1931 até 2012)
%itutinga=load('Itutinga.txt');          % Vetor 82 x 12 (de 1931 até 2012)
%furnas=load('Furnas.txt');              % Vetor 82 x 12 (de 1931 até 2012)

Pcamargos=[];
Tcamargos=[];
%Pitutinga=[];
%Titutinga=[];
%Pfurnas=[];
%Tfurnas=[];
for i=1:1:40 
    Pcamargos = [Pcamargos camargos(i,:)'];
    Tcamargos = [Tcamargos camargos(i+1,:)'];  
    %Pitutinga = [Pitutinga itutinga(i,:)'];
    %Titutinga = [Titutinga itutinga(i+1,:)'];
    %Pfurnas=[Pfurnas furnas(i,:)'];
    %Tfurnas=[Tfurnas furnas(i+1,:)'];
end
%P=[Pcamargos; Pitutinga; Tfurnas];
%T=[Tcamargos; Titutinga; Tfurnas];
P=[Pcamargos];
T=[Tcamargos];

% 2) Criar uma arquitetura de rede MLP.
net = feedforwardnet(20);
net = configure(net,P,T);

% 3) Dividir Padrões em Treinamento, Validação e Teste.
net.divideFcn='dividerand';
net.divideParam.trainRatio=1.00;
net.divideParam.valRatio=0.00;
net.divideParam.testRatio=0.00;

% 4) Inicializando os Pesos da Rede.
net=init(net);

% 5) Treinando a Rede Neural.
net.trainParam.showWindow=true;         % Exibe a Interface Gráfica com o Usuário (GUI)
net.layers{1}.dimensions=20;            % Número de Neorônios da Camada Interna
net.layers{1}.transferFcn='tansig';     % Funções de Ativação da Camada Interna
net.layers{2}.transferFcn='purelin';    % Funções de Ativação da Camada de Saída
net.performFcn='mse';                   % Determina o critério de Performance do Treinameno   
%net.trainFcn='trainbr';                % Determina o Algoritmo de Treinamento   
net.trainFcn='trainrp';                 % Determina o Algoritmo de Treinamento     
net.trainParam.epochs=1000000;          % Número Máximo de Épocas de Treinamento
net.trainParam.time=120;                % Tempo Máximo de Treinamento (em segundos)
net.trainParam.lr=0.2;                  % Taxa de Aprendizado 
net.trainParam.min_grad=10^-18;         % Valor Mínimo do Gradiente, Como Critério de Parada 
net.trainParam.max_fail=1000;           % Número Máximo de Interações Sem Decaimento do Gradiente        
[net, tr]=train(net,P,T);

% 6) Simular as respostas de saída da rede MLP.
% 6.1) Plotar Padrões de Treinamento
xP=1:1:(41*12);
xF=(41*12)+1:1:42*12;
XcamargosP=[];
for i=1:1:41
    XcamargosP=[XcamargosP camargos(i,:)];
end
XcamargosF=camargos(42,:);
plot(xP,XcamargosP,'b',xF,XcamargosF,'r')
xlabel('Meses')
ylabel('Vazão')
title('Vazão do Rio Camargos')
grid
% 6.2) Plotar Resultados da Simulação
hold on
xS=1:1:(42*12);
PsA=camargos(1,:)';
Ms=PsA;
for i=1:1:41
    PsD=sim(net,PsA);
    Ms=[Ms PsD];
    PsA=PsD;
end
yS=[];
for i=1:1:42
    yS=[yS Ms(:,i)'];
end
plot(xS,yS,':m');




