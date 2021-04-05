function decay_disk = decayDisk(decay_length,a,R_max)

%% doc: %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%{

%}


lambda = 1/decay_length;
decay_length_nm = decay_length;
decay_length_pixels = decay_length_nm/a;

% radial distribution 
x = -R_max:1:R_max;
y = -R_max:1:R_max;
[X,Y] = meshgrid(x,y);
R = sqrt(X.^2 + Y.^2);
Z = lambda*exp(-R/decay_length_pixels);
Z = Z/sum(sum(Z));
decay_disk = Z;

end



