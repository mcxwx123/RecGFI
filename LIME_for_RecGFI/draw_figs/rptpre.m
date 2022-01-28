%rptpre.eps
load ..\data\rptpre.mat
rng default  % For reproducibility
vmat1=cell2mat(rptprelist0(1,1));
vmat2=cell2mat(rptprelist0(1,2));
vmat3=cell2mat(rptprelist0(1,3));
vmat4=cell2mat(rptprelist0(1,4));
mmat1=cell2mat(rptprelist1(1,1));
mmat2=cell2mat(rptprelist1(1,2));
mmat3=cell2mat(rptprelist1(1,3));
mmat4=cell2mat(rptprelist1(1,4));

vmat1=vmat1';
vmat2=vmat2';
vmat3=vmat3';
vmat4=vmat4';
a=1;
b=1;
c=3;
width=0.7;



figure
q=boxplot(vmat1,'symbol','','Whisker',0,'Colors',[0 0 0],'width',width,'positions',a);
set(q,'Linewidth',1.5);
hold on;
w=boxplot(vmat2,'symbol','','Whisker',0,'Colors',[0 0 0],'width',width,'positions',a+c);
set(w,'Linewidth',1.5);
hold on;
e=boxplot(vmat3,'symbol','','Whisker',0,'Colors',[0 0 0],'width',width,'positions',a+2*c);
set(e,'Linewidth',1.5);
hold on;
r=boxplot(vmat4,'symbol','','Whisker',0,'Colors',[0 0 0],'width',width,'positions',a+3*c);
set(r,'Linewidth',1.5);
hold on
t=boxplot(mmat1','symbol','','Whisker',0,'Colors',[0 0 0],'width',width,'positions',a+b);
set(t,'Linewidth',1.5);
hold on;
u=boxplot(mmat2','symbol','','Whisker',0,'Colors',[0 0 0],'width',width,'positions',a+c+b);
set(u,'Linewidth',1.5);
hold on;
i=boxplot(mmat3','symbol','','Whisker',0,'Colors',[0 0 0],'width',width,'positions',a+2*c+b);
set(i,'Linewidth',1.5);
hold on;
o=boxplot(mmat4','symbol','','Whisker',0,'Colors',[0 0 0],'width',width,'positions',a+3*c+b);
set(o,'Linewidth',1.5);
set(gca,'Linewidth',2);
set(gca,'XLim',[a-1 a+3*c+b+1]);
set(gca,'YLim',[0 1]);
%set(gca,'XTickLabelRotation',90);
alpha(.7)
set(gca,'FontSize',23);
set(gcf,'unit','centimeters','position',[20 10 30 10])
set(gca,'Position',[.1 .20 0.85 .75],'linewidth',2);
grid on
set(gca,'xtick',a+0.5*b:c:a+0.5*b+4*c, 'xticklabel', {'0≤#cmt<200','200≤#cmt<400','400≤#cmt<600','600≤#cmt'});
set(gca,'ticklength',[0 0])
ylabel('Predictions');
h = findobj(gca,'Tag','Box');
color2=[0.00,0.45,0.74];
color1=[0.85,0.33,0.10];
colorlist ={color1,color1,color1,color1,color2,color2,color2,color2};

for j=1:length(h)
patch(get(h(j),'XData'),get(h(j),'YData'),cell2mat(colorlist(j)),'FaceAlpha',.5);
end
