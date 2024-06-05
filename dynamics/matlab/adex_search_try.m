lobal cds
par_t_ref = 2.5;
par_C_m = 1000;
par_g_L = 50;
par_E_L = -60;
par_Delta_T = 2.5;
par_V_th = -50;
par_tau_w = 600;
par_a = 200;
par_b = 20;
par_V_spike = 0;
par_V_reset = -60;

% Get system handles
system_handles = adex_matcont_model();

% Time Span
tspan = [0 1000];  % Simulate from 0 to 1000 ms

% Initial Conditions (Adjust as needed)
y0 = [-65; 0];     % Initial membrane potential and adaptation variable

% ODE Options (Optional)
options = odeset('RelTol', 1e-3, 'AbsTol', 1e-6); % Adjust tolerances if needed

% Run the Simulation to find a stable limit cycle
[t,y] = ode45(system_handles{2}, tspan, y0, options, 10);

% Check if a limit cycle was found (visually)
plot(y(:,1), y(:,2));
xlabel('Membrane Potential (mV)');
ylabel('Adaptation Variable (pA)');
title('Phase Plane Plot to Identify Limit Cycle');

% If a limit cycle is visually identified, proceed to continuation

% Extract a point on the limit cycle (adjust indices based on your plot)
x1 = y(end-100:end,:); 
t1 = t(end-100:end,:);

% Initialisation of limit cycle continuation
[x0,v0] = initOrbLC(@adex_matcont_model, t1, x1, [10], [1], 20, 4, 1e-6);

opt=contset;
opt=contset(opt,'MaxNumPoints',50);

% Continuation of limit cycle
[xlc,vlc,slc,hlc,flc] = cont(@limitcycle,x0,v0,opt);

% Plot the results
figure
plotcycle(xlc,vlc,slc,[1 2]);
