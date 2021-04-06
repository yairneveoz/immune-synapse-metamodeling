% tests
sq_dep_decay_rTCR_normalized_counts = ...
    squeeze(dep_decay_rTCR_normalized_counts);

% rTCR_data = dlmread('rTCR_hist_model3_negativeDep.m');
figure(6)
% sq_dep_decay_TCR_normalized_counts = ...
%     squeeze(dep_decay_TCR_normalized_counts);
sq_dep_decay_rTCR_normalized_counts(...
    isnan(sq_dep_decay_rTCR_normalized_counts)) = 0;

surf(sq_dep_decay_rTCR_normalized_counts)
colorbar
view(2)





