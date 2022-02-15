function [] = plotTCR_CD45(plots_parameters,...
    tcr_x,tcr_y,cd45_x,cd45_y,Z1)

scatter3(tcr_x,tcr_y,100*ones(size(tcr_x)),...
    plots_parameters.marker_size,...
    'MarkerEdgeColor','none',...
    'MarkerFaceColor',plots_parameters.tcr.color)

hold on
scatter3(cd45_x,cd45_y,100*ones(size(cd45_x)),...
    plots_parameters.marker_size,...
    'MarkerEdgeColor','none',...
    'MarkerFaceColor',plots_parameters.cd45.color)
hold off
grid off
box on
view(2)
axis equal
axis tight
f = 0.2;
axis([f*size(Z1,1),...
      (1-f)*size(Z1,1),...
      f*size(Z1,2),...
      (1-f)*size(Z1,2)])

xticks([])
yticks([])
% xticklabels(10*xticks)
% yticklabels(10*yticks)
% colorbar
drawnow

end