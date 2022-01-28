%featurebox.eps
load ..\data\oneproft.mat
rng default  % For reproducibility
figure
onelist=onelist';
cutprol=[onelist(:,1:5),onelist(:,33),onelist(:,32),onelist(:,34:38),onelist(:,40),onelist(:,42:43),onelist(:,41),onelist(:,39),onelist(:,44),onelist(:,57),onelist(:,12)];
%m=mean(cutprol);
%cutprol=onelist;
%m=mean(onelist);
%disp(m);


a=boxplot(cutprol,'symbol','','Whisker',0,'Colors',[0 0 0]);

set(a,'Linewidth',1.5);
set(gca,'YLim',[-0.21 0.17]);
set(gca,'XTickLabelRotation',90);
grid on
set(gca, 'xticklabel', {'len_title','len_body','#urls','#imgs','#code_snips',"#pr_proj","#pr_all","#cmt_proj","#cmt_all","#repo","#stars_rptr","#followers",'has_comment', 'has_event',"nongfi:gfi",'rpt_is_new',"#issues_all","#issues_proj","#labels",'#comments'});
set(gca,'ticklength',[0 0])

alpha(.7)
set(gca,'FontSize',23);
set(gcf,'unit','centimeters','position',[20 10 30 15])
set(gca,'Position',[.12 .38 0.85 .6],'linewidth',2);

ylabel('Coefficient');
h = findobj(gca,'Tag','Box');
color=[0.00,0.45,0.74];
colorlist ={color,color,color,color,color,color,color,color,color,color,color,color,color,color,color,color,color,color,color,color,color,color,color,color,color,color};

for j=1:length(h)
patch(get(h(j),'XData'),get(h(j),'YData'),cell2mat(colorlist(j)),'FaceAlpha',.7);
end
hold on;
plot(mean(cutprol),'^','MarkerFace','k','MarkerSize',10);
