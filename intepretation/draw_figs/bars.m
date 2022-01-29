%probar.eps
load ..\data\allproft.mat
rng default  % For reproducibility
figure
alllist=alllist';
cutprol=[alllist(:,14),alllist(:,13),alllist(:,15:19),alllist(:,21),alllist(:,20),alllist(:,22:31)];
posl=sum(cutprol);
negl=91-posl;
total=[posl;negl];
b = bar(total','stacked','FaceColor',[0.00,0.45,0.74]);
set(b,'Linewidth',1.5);
ylabel('#projects')
set(gca,'XTickLabelRotation',90);
set(gca,'XTick',1:1:19);
set(gca,'YLim',[0 95]);
set(gca,'YTickLabel','');
set(gca,'ticklength',[0 0])

alpha(.7)
set(gca,'FontSize',23);
set(gcf,'unit','centimeters','position',[20 10 30 15])
set(gca,'Position',[.05 .5 0.85 .5],'linewidth',2);
hold on
plot([-1,21],[45.5,45.5],'-b', 'LineWidth', 2,'Color',[0.667 0.667 1]);
set(gca,'XLim',[0 20]);
grid on
%set(gca,'Linewidth',2);
set(gca, 'xticklabel', {"#pr\_proj\_owner","#pr\_all\_owner","#cmt\_proj\_owner","#cmt\_all\_owner","#repo\_owner","#stars\_owner","#followers\_owner","#issues\_proj\_owner","#issues\_all\_owner",":gfi\_owner","#gfi\_owner",':gfi\_proj','#gfi\_proj','#iss\_open','iss\_cls\_t','#stars','#cmt','#contributors','#pr'});
