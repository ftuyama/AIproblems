clear all
clc

% 1) Criar Padr�es de Entrada/Sa�da
camargos=load('CamargosR.txt');          % Vetor 30 x 12 (de 1970 at� 2000)
itutinga=load('ItutingaR.txt');          % Vetor 30 x 12 (de 1970 at� 2000)
furnas=load('FurnasR.txt');              % Vetor 30 x 12 (de 1970 at� 2000)

tamanho = 29;
Pcamargos = Pcamargos_1 = Tcamargos = [];
Pitutinga = Pitutinga_1 = Titutinga = [];
Pfurnas = Pfurnas_1 = Tfurnas=[];
for i=1:1:tamanho
    Pcamargos_1 = [Pcamargos_1 camargos(i, :)'];
    Pcamargos = [Pcamargos camargos(i+1,:)'];
    Tcamargos = [Tcamargos camargos(i+2,:)'];  
    
    Pitutinga_1 = [Pitutinga_1 itutinga(i,:)'];
    Pitutinga = [Pitutinga itutinga(i+1,:)'];
    Titutinga = [Titutinga itutinga(i+2,:)'];

    Pfurnas_1=[Pfurnas_1 furnas(i,:)'];
    Pfurnas=[Pfurnas furnas(i+1,:)'];
    Tfurnas=[Tfurnas furnas(i+2,:)'];
end
P=[Pcamargos_1; Pcamargos; Pitutinga_1; Pitutinga; Pfurnas_1; Pfurnas];
T=[Tcamargos; Titutinga; Tfurnas];

% 2) Criar uma arquitetura de rede MLP.
net = feedforwardnet([20 30 25]);
net = configure(net,P,T);

% 2.1) Normalizando a Entrada
net.inputs{1}.processParams{2}.ymin =0;
net.inputs{1}.processParams{2}.ymax =1;
net.outputs{2}.processParams{2}.ymin =0;
net.outputs{2}.processParams{2}.ymax =1;

% 3) Dividir Padr�es em Treinamento, Valida��o e Teste.
net.divideFcn='dividerand';
net.divideParam.trainRatio=0.80;
net.divideParam.valRatio=0.10;
net.divideParam.testRatio=0.10;

% 4) Inicializando os Pesos da Rede.
net=init(net);

% 5) Treinando a Rede Neural.
net.trainParam.showWindow=true;         % Exibe a Interface Gr�fica com o Usu�rio (GUI)
net.layers{1}.dimensions=20;            % N�mero de Neor�nios da Camada Interna
net.layers{1}.transferFcn='tansig';     % Fun��es de Ativa��o da Camada Interna
net.layers{4}.transferFcn='purelin';    % Fun��es de Ativa��o da Camada de Sa�da
net.performFcn='mse';                   % Determina o crit�rio de Performance do Treinameno   
net.trainFcn='trainlm';                 % Determina o Algoritmo de Treinamento     
net.trainParam.epochs=1000000;          % N�mero M�ximo de �pocas de Treinamento
net.trainParam.time=120;                % Tempo M�ximo de Treinamento (em segundos)
net.trainParam.lr=0.2;                  % Taxa de Aprendizado 
net.trainParam.min_grad=10^-8;         % Valor M�nimo do Gradiente, Como Crit�rio de Parada 
net.trainParam.max_fail=1000;           % N�mero M�ximo de Intera��es Sem Decaimento do Gradiente        
[net, tr]=train(net,P,T);




%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%Simulação usando Redes Neurais

tamanho = tamanho+1;
xS=1:1:((tamanho+1)*12);

PsA=camargos(1,:)';
PsB=itutinga(1,:)';
PsC=furnas(1,:)';

Ms1=PsA;
Ms1=[Ms1 camargos(2,:)'];

Ms2=PsB;
Ms2=[Ms2 itutinga(2,:)'];

Ms3=PsC;
Ms3=[Ms3 furnas(2,:)'];

for i=2:1:tamanho
    PsA_1 = PsA;
    PsA=camargos(i,:)';
    PsB_1 = PsB;
    PsB=itutinga(i,:)';
    PsC_1 = PsC;
    PsC=furnas(i,:)';


    PsD=sim(net,[PsA_1; PsA; PsB_1; PsB; PsC_1; PsC]);
    PsD1 = PsD(1:12);
    PsD2 = PsD(13:24);
    PsD3 = PsD(25:36);
    Ms1=[Ms1 PsD1];
    Ms2=[Ms2 PsD2];
    Ms3=[Ms3 PsD3];
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Simulação do rio Camargos
% 6) Simular as respostas de sa�da da rede MLP.
% 6.1) Plotar Padr�es de Treinamento
xP=1:1:(tamanho*12);
xF=(tamanho*12)+1:1:(tamanho+1)*12;
XcamargosP=[];
for i=1:1:tamanho
    XcamargosP=[XcamargosP camargos(i,:)];
end
XcamargosF=camargos((tamanho+1),:);
plot(xP,XcamargosP,'b',xF,XcamargosF,'r')
xlabel('Meses')
ylabel('Vazao')
title('Vazao do Rio Camargos')
grid
% 6.2) Plotar Resultados da Simula��o
hold on
xS=1:1:((tamanho+1)*12);
yS=[];
for i=1:1:(tamanho+1)
    yS=[yS Ms1(:,i)'];
end
plot(xS,yS,':m');
figure;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%Simulação do rio itutinga
% 6) Simular as respostas de sa�da da rede MLP.
% 6.1) Plotar Padr�es de Treinamento
xP=1:1:(tamanho*12);
xF=(tamanho*12)+1:1:(tamanho+1)*12;
XitutingaP=[];
for i=1:1:tamanho
    XitutingaP=[XitutingaP itutinga(i,:)];
end
XitutingaF=itutinga((tamanho+1),:);
plot(xP,XitutingaP,'b',xF,XitutingaF,'r')
xlabel('Meses')
ylabel('Vazao')
title('Vazao do Rio Itutinga')
grid
% 6.2) Plotar Resultados da Simula��o
hold on
xS=1:1:((tamanho+1)*12);
yS=[];
for i=1:1:(tamanho+1)
    yS=[yS Ms2(:,i)'];
end
plot(xS,yS,':m');
figure;



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%Simulação do rio FurnasR
% 6) Simular as respostas de sa�da da rede MLP.
% 6.1) Plotar Padr�es de Treinamento
xP=1:1:(tamanho*12);
xF=(tamanho*12)+1:1:(tamanho+1)*12;
XfurnasP=[];
for i=1:1:tamanho
    XfurnasP=[XfurnasP furnas(i,:)];
end
XfurnasF=furnas((tamanho+1),:);
plot(xP,XfurnasP,'b',xF,XfurnasF,'r')
xlabel('Meses')
ylabel('Vazao')
title('Vazao do Rio Furnas')
grid
% 6.2) Plotar Resultados da Simula��o
hold on
xS=1:1:((tamanho+1)*12);
yS=[];
for i=1:1:(tamanho+1)
    yS=[yS Ms3(:,i)'];
end
plot(xS,yS,':m');
