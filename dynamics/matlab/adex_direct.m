function dydt = fun_eval(t, kmrgd, par_I_stim)
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

if kmrgd(1) >= par_V_th
kmrgd(1) = par_V_reset;
kmrgd(2) = kmrgd(2) + par_b;
end

dydt=[(-par_g_L*(kmrgd(1)-par_E_L)+(par_g_L*par_Delta_T*exp((kmrgd(1)-par_V_th)/par_Delta_T))+kmrgd(2)+par_I_stim)/par_C_m;
(par_a*(kmrgd(1)-par_E_L)-kmrgd(2))/par_tau_w;];

