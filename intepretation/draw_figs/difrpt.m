%ftvalue.eps
load ..\data\ftvalue.mat
rng default  % For reproducibility
vmat1=[];
vmat2=[];
vmat3=[];
vmat4=[];

for s=1:106
    vmat1=[vmat1;cell2mat(valuelist(1,s))];
end
for s=1:106
    vmat2=[vmat2;cell2mat(valuelist(2,s))];
end
for s=1:106
    vmat3=[vmat3;cell2mat(valuelist(3,s))];
end
for s=1:106
    vmat4=[vmat4;cell2mat(valuelist(4,s))];
end
vmat1=vmat1';
vmat2=vmat2';
vmat3=vmat3';
vmat4=vmat4';
a=1;
b=5;
c=1;
width=0.7;
cutprol=[vmat1(:,34:35),vmat1(:,44),vmat1(:,39)];
figure
q=boxplot(cutprol,'symbol','','Colors',[0 0 0],'width',width,'positions',a:b:a+3*b);
set(q,'Linewidth',1.5);
cutprol=[vmat2(:,34:35),vmat2(:,44),vmat2(:,39)];
hold on;
w=boxplot(cutprol,'symbol','','Colors',[0 0 0],'width',width,'positions',a+c:b:a+c+3*b);
set(w,'Linewidth',1.5);
cutprol=[vmat3(:,34:35),vmat3(:,44),vmat3(:,39)];
hold on;
e=boxplot(cutprol,'symbol','','Colors',[0 0 0],'width',width,'positions',a+2*c:b:a+2*c+3*b);
set(e,'Linewidth',1.5);
cutprol=[vmat4(:,34:35),vmat4(:,44),vmat4(:,39)];
hold on;
r=boxplot(cutprol,'symbol','','Colors',[0 0 0],'width',width,'positions',a+3*c:b:a+3*c+3*b);
set(r,'Linewidth',1.5);
set(gca,'Linewidth',2);
set(gca,'XLim',[a-1 a+3*c+3*b+1],'YLim',[-0.21 0.2]);
%set(gca,'XTickLabelRotation',45);
alpha(.7)
set(gca,'FontSize',23);
set(gcf,'unit','centimeters','position',[20 10 30 15])
set(gca,'Position',[.13 .25 0.85 .7],'linewidth',2);
grid on
set(gca,'xtick',a+1.5*c:b:a+1.5*c+3*b, 'xticklabel', {'#cmt_proj','#cmt_all','#issues_proj','#issues_all'});
set(gca,'ticklength',[0 0]);
ylabel('Coefficient');
hold off 

%legend([data1 data2],{'First','Third'})
%legend('data1','data2','data3','data4')
h = findobj(gca,'Tag','Box');
color2=[0 0.5 0.5];
color1=[162 20 47]/255;
color3=[0.85,0.33,0.10];
color4=[0.00,0.45,0.74];
colorlist ={color1,color1,color1,color1,color2,color2,color2,color2,color3,color3,color3,color3,color4,color4,color4,color4};

for j=1:length(h)
patch(get(h(j),'XData'),get(h(j),'YData'),cell2mat(colorlist(j)),'FaceAlpha',.7);
end

legend([q(1),w(1),e(1),r(1)], {'#cmt\_proj<200','200≤#cmt\_proj<400','400≤#cmt\_proj<600','600≤#cmt\_proj'});


