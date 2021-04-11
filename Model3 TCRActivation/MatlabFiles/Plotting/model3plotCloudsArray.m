function model3plotCloudsArray()

%% doc: %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%{


Input:
Calls: orangeGrayColormap,
       parulaGrayColormap,
       radialDistributionArray,
       
Output:

%}
%
%% colors and colormaps: %%%%%%%%%%%%%%
% TCR_color = [0.0, 0.6, 0.0];
% CD45_color = [1.0, 0.0, 0.0];

Nc = 64;
% orange_blue_colormap = orangeBlueColormap(Nc);
% orange_gray_colormap = orangeGrayColormap(Nc);
orange_fixed_colormap = orangeFixedColormap(Nc);
% magenta_fixed_colormap = magentaFixedColormap(Nc);
%
%% sizes: %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
N_cols = 5;
N_rows = 6;

% subplots and gaps sizes (relative to the figure size):
gapx0 = 0.12; % relative initial gap on the left.
gapy0 = 0.125; % relative initial gap on the bottom.
gapx = 0.015; % relative gap x between subplots.
gapy = 0.02; % relative gap x between subplots.
size_x = 0.75/N_cols; % relative subplots x size.
size_y = 0.75/N_rows; % relative subplots y size.

% origins of the individual subplots:
origins_x = gapx0 + (size_x + gapx)*[0:N_cols-1];
origins_y = gapy0 + (size_y + gapy)*[0:N_rows-1];

%
%% array sizes: %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
array_size_x_microns = 2;
array_size_y_microns = 2;

array_size_x_pixels = array_size_x_microns*100;
array_size_y_pixels = array_size_y_microns*100;
%
%% TCR_locations %%%%%%%%%%%%%%%%%%%%%%
% TCR_cluster_density = 1000;
% TCR_r1 = 0;
TCR_r2 = 0.25; % microns
pixel_size = 10; % nm

%%% create TCR locations: %%%%%%%%%%%%%
% [TCR_x_pixels0,TCR_y_pixels0] = radialDistributionArray(...
%     TCR_cluster_density,TCR_r1,TCR_r2,pixel_size,...
%     array_size_x_microns,array_size_y_microns);

% TCR_x_pixels = TCR_x_pixels0 - 100*array_size_x_microns/2;
% TCR_y_pixels = TCR_y_pixels0 - 100*array_size_y_microns/2;

%% start subplots loops: %%%%%%%%%%%%%%
N_rows = 6;
N_cols = 5;

depletions = [-250,0:10:200];
decayLengths = 10:10:200;

% selected indices to plot as subplots:
s_dep_ind = [1,2:5:22]; % selected, N = N_rows
s_dec_ind = [2,5,10,15,20]; % selected, N = N_cols

%% plot clouds: %%%%%%%%%%%%%%%%%%%%%%%
figure(13)
clf
set(gcf, 'Units', 'pixels',...
        'OuterPosition', [400, 50, 700, 800]);
    
axis_off = 1;
R_max = ceil(array_size_x_pixels/2);
CD45_decay_length_nm = 10;
lim1 = 60; % 100
shift_x = 100; % pixels
shift_y = 100; % pixels

for col_ind = 1:N_cols
    for row_ind = 1:N_rows

        % index of depletion value:
        idep = s_dep_ind(row_ind);
        % index of decay_length value:

        idec = s_dec_ind(col_ind);

        % name (letter) of point
    %     iname = samples_data(s2).name;

        pos1 = ([origins_x(col_ind),...
                 origins_y(row_ind),...
                 size_x, size_y]); % N_rows+1 - 

        h1 = subplot('Position',pos1);

        %% calculate locations: %%%%%%%%%%%%%%%%%%%%%
        %% CD45: %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        depletion_range_nm = depletions(idep);

        CD45_cluster_density = 1000;
        CD45_r1 = TCR_r2 + depletion_range_nm/1000; % nm
        CD45_r2 = CD45_r1 + 0.3; % nm 0.3

        [CD45_x_pixels0,CD45_y_pixels0] = radialDistributionArray(...
            CD45_cluster_density,CD45_r1,CD45_r2,pixel_size,...
            array_size_x_microns,array_size_y_microns);

%         CD45_x_pixels = CD45_x_pixels0 - array_size_x_pixels/2;
%         CD45_y_pixels = CD45_y_pixels0 - array_size_y_pixels/2;

        %% calculate clouds (phosphorylation probability)
        % CD45 decay:
        CD45_decay_disk = decayDisk(...
            CD45_decay_length_nm,pixel_size,R_max);
        norm_CD45_decay_disk = CD45_decay_disk/sum(sum(CD45_decay_disk));

        %%% aLck decay:
        aLck_decay_length_nm = decayLengths(idec); 

        aLck_decay_disk = decayDisk(...
            aLck_decay_length_nm,pixel_size,R_max);
        norm_aLck_decay_disk = aLck_decay_disk/sum(sum(aLck_decay_disk));

        % sum of decays:
        sum_norm_decay_disk = norm_aLck_decay_disk - norm_CD45_decay_disk;

        % phosphorylayion probability > 0:
        sum_norm_decay_disk(sum_norm_decay_disk < 0) = 0;

        % 2D covolution of decay_disk with CD45 locations:
        decay_probability_array = aLckProbabilityArray(...
        sum_norm_decay_disk,array_size_x_pixels,array_size_y_pixels,...
        CD45_x_pixels0,CD45_y_pixels0);

        %%
        %% plot clouds: %%%%%%%%%%%%%%%%%%%
        h2 = surf(decay_probability_array);
        view(2)
        h2.EdgeColor = 'none';
        h2.FaceAlpha = 1.0;
%         colormap(magenta_fixed_colormap)
        colormap(orange_fixed_colormap)
        alpha color
        alpha scaled
        axis equal

        axis(shift_x + [-lim1 lim1 -lim1 lim1])
        xticks(shift_x + [-50:50:50])
        yticks(shift_y + [-50:50:50])
        xticklabels({10*[-50:50:50]})
        yticklabels({10*[-50:50:50]})
    %     xlabel('x(nm)')
    %     ylabel('y(nm)')
        %%
        if axis_off
            set(gca,'xtick',[],'ytick',[])
            set(gca,'xlabel',[],'ylabel',[])
        end

    end
end

end


