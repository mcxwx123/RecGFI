%preres.eps
load ..\data\predata.mat
figure

h1 = histogram(list0,'FaceColor',[0.00,0.45,0.74],'linewidth',1.5);
hold on
h2 = histogram(list1,'FaceColor',[0.85,0.33,0.10],'linewidth',1.5);
hold on

h1.Normalization = 'probability';
h1.BinWidth = 0.25;
h2.Normalization = 'probability';
h2.BinWidth = 0.25;
h1.NumBins = 20;
h2.NumBins = 20;
plot([0.5 0.5], get(gca, 'YLim'), '-b', 'LineWidth', 2,'Color',[0.667 0.667 1]);%[1 0.5 0]
xlabel('Probability of predictions')
ylabel('Normalized distribution')
%set(gca,'YTickLabel','');
set(gca,'ticklength',[0 0])
title('prediction: non-newcomer             prediction: newcomer')
grid on
legend('solved by non-newcomer','solved by newcomer')

alpha(.6)
set(gca,'FontSize',23);
set(gcf,'unit','centimeters','position',[20 10 30 13])
set(gca,'Position',[.1 .2 0.85 .7],'linewidth',2);
