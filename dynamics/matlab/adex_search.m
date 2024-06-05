clc
clear all

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

par_I_stim = 5000;

int = [0,0]
[t,y] = ode45(@(t,y) adexde(t,y,par_I_stim),[0,20000],int');

V_m_trajectories = y(:, 1);
w_trajectories = y(:, 2);

% Plot phase plane
figure;
plot(V_m_trajectories, w_trajectories);
xlabel('V_m');
ylabel('w');
title('Phase Plane Trajectories');
grid on;




