clc
clear all;

% Number of mass and spring
nb=20;

% Time step
dt=0.5;
% Duration
T=50;
% Calculation of the computing times
t = dt:dt:T;

% Calculation of F2
F2=zeros(nb,size(t,2));
F2(nb,:)=2*(sin(0.8.*t)+sin(0.3.*t)).*exp(-0.1.*t);
F2(3,:)=3*cos(0.85.*t);
F2(8,:)=2*sin(1.15.*t);

% Building of matrices K and M
Raideur=15;
K=-1*(diag(diag(ones(nb-1)),1)+diag(diag(ones(nb-1)),-1))+2*diag(diag(ones(nb)));
K(end,end)=1;
K=K*Raideur;

% Reference FEM solution
UREF=K^(-1)*F2;

% Number of PGD modes to be computed
nbMPGD=30;
% Initialization
PHI=zeros(nb,nbMPGD);
ALPHA=ones(nbMPGD,size(t,2));

% Time vector for integration
Nt = length(t);

% ---------- PGD Algorithm ----------
% Initialize residual as the full solution
R = UREF;  % Residual to be approximated

% Loop over PGD modes
for m = 1:nbMPGD
    fprintf('Computing PGD mode %d...\n', m);
    
    % Initial guess for alpha_m(t) (normalized random)
    alpha_m = randn(1, Nt);
    alpha_m = alpha_m / norm(alpha_m);
    
    % ---- Step 1: Solve for phi_m (space function) ----
    % Equation: ∫ (alpha_m * alpha_m') dt * K * phi_m = ∫ alpha_m * R dt
    
    % Compute time integrals
    A_alpha = (alpha_m * alpha_m') * dt;  % ∫ α_m(t)α_m(t) dt
    b_phi = zeros(nb, 1);
    for i = 1:Nt
        b_phi = b_phi + alpha_m(i) * R(:, i) * dt;
    end
    
    % Solve for phi_m
    phi_m = (A_alpha * K) \ (K * b_phi);
    
    % Normalize phi_m
    phi_m = phi_m / norm(phi_m);
    
    % ---- Step 2: Solve for alpha_m(t) (time function) ----
    % Equation: (phi_m' * K * phi_m) * alpha_m(t) = phi_m' * R(:,t)
    
    % Compute scalar
    k_mm = phi_m' * K * phi_m;
    
    % Solve for alpha_m at each time step
    for i = 1:Nt
        alpha_m(i) = (phi_m' * R(:, i)) / k_mm;
    end
    
    % ---- Store mode ----
    PHI(:, m) = phi_m;
    ALPHA(m, :) = alpha_m;
    
    % ---- Update residual ----
    R = R - phi_m * alpha_m;
    
    % ---- Plot current mode ----
    figure(10);
    subplot(nbMPGD, 2, 2*m-1);
    plot(phi_m, 'b-o');
    xlabel('DOF');
    ylabel('\phi_m(x)');
    title(sprintf('PGD Mode %d (space)', m));
    grid on;
    
    subplot(nbMPGD, 2, 2*m);
    plot(t, alpha_m, 'r-');
    xlabel('Time');
    ylabel('\alpha_m(t)');
    title(sprintf('PGD Time function %d', m));
    grid on;
    
    % ---- Plot current approximation ----
    U_current = PHI(:, 1:m) * ALPHA(1:m, :);
    
    figure(20);
    subplot(nbMPGD, 1, m);
    plot(t, U_current(end, :), 'b-', t, UREF(end, :), 'r--');
    xlabel('Time');
    ylabel('Displacement at last DOF');
    title(sprintf('PGD Approximation with %d mode(s)', m));
    legend('PGD', 'FEM Reference');
    grid on;
end

% Final PGD approximation
UPGD = PHI * ALPHA;

% Final comparison plot
figure(30);
plot(t, UPGD(end, :), '.', t, UREF(end, :), '-');
xlabel('Time');
ylabel('Displacement at last DOF');
legend('PGD', 'FEM');
title('Final PGD vs FEM Comparison');
grid on;

% Compute relative error
error_norm = norm(UPGD(:) - UREF(:)) / norm(UREF(:));
fprintf('Relative error (norm): %.4f\n', error_norm);

% Display mode energies
mode_energies = diag(PHI' * K * PHI);
fprintf('Mode energies:\n');
for m = 1:nbMPGD
    fprintf('  Mode %d: %.4e\n', m, mode_energies(m));
end