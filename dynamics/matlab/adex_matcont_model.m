function out = adex_matcont_model
out{1} = @init;
out{2} = @fun_eval;
out{3} = [];
out{4} = [];
out{5} = [];
out{6} = [];
out{7} = [];
out{8} = [];
out{9} = [];

% --------------------------------------------------------------------------
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


% --------------------------------------------------------------------------
function [tspan,y0,options] = init
handles = feval(adexde);
y0=[0,0];
options = odeset('Jacobian',[],'JacobianP',[],'Hessians',[],'HessiansP',[]);
tspan = [0 10];

% --------------------------------------------------------------------------
function jac = jacobian(t,kmrgd,par_t_ref,par_C_m,par_g_L,par_E_L,par_Delta_T,par_V_th,par_tau_w,par_a,par_b,par_V_spike,par_V_reset,par_I_stim)
% --------------------------------------------------------------------------
function jacp = jacobianp(t,kmrgd,par_t_ref,par_C_m,par_g_L,par_E_L,par_Delta_T,par_V_th,par_tau_w,par_a,par_b,par_V_spike,par_V_reset,par_I_stim)
% --------------------------------------------------------------------------
function hess = hessians(t,kmrgd,par_t_ref,par_C_m,par_g_L,par_E_L,par_Delta_T,par_V_th,par_tau_w,par_a,par_b,par_V_spike,par_V_reset,par_I_stim)
% --------------------------------------------------------------------------
function hessp = hessiansp(t,kmrgd,par_t_ref,par_C_m,par_g_L,par_E_L,par_Delta_T,par_V_th,par_tau_w,par_a,par_b,par_V_spike,par_V_reset,par_I_stim)
%---------------------------------------------------------------------------
function tens3  = der3(t,kmrgd,par_t_ref,par_C_m,par_g_L,par_E_L,par_Delta_T,par_V_th,par_tau_w,par_a,par_b,par_V_spike,par_V_reset,par_I_stim)
%---------------------------------------------------------------------------
function tens4  = der4(t,kmrgd,par_t_ref,par_C_m,par_g_L,par_E_L,par_Delta_T,par_V_th,par_tau_w,par_a,par_b,par_V_spike,par_V_reset,par_I_stim)
%---------------------------------------------------------------------------
function tens5  = der5(t,kmrgd,par_t_ref,par_C_m,par_g_L,par_E_L,par_Delta_T,par_V_th,par_tau_w,par_a,par_b,par_V_spike,par_V_reset,par_I_stim)
