#!/usr/bin/env python3
"""发动机非线性动力学可视化 - Duffing 振子(叶片/转子振动经典非线性模型)
方程: ẍ + δẋ + αx + βx³ = γcos(ωt)
展示:周期→分岔→混沌 的典型非线性动力学行为
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.sans-serif'] = ['PingFang SC', 'Arial Unicode MS', 'Heiti TC', 'sans-serif']
rcParams['axes.unicode_minus'] = False
rcParams['figure.dpi'] = 120

OUT = "/Users/wyf/Desktop/code/document/04-tech/engine_nonlinear_dynamics/images"
BG = '#1e1e2e'; FG = '#cdd6f4'; DIM = '#6c7086'
C_PERIOD = '#1e66f5'; C_CHAOS = '#f38ba8'; C_BIF = '#f9e2af'; C_LYA = '#a6e3a1'

def deriv(state, t, delta, alpha, beta, gamma, omega):
    x, v = state
    return np.array([v, -delta*v - alpha*x - beta*x**3 + gamma*np.cos(omega*t)])

def rk4(state, t, dt, *args):
    k1 = deriv(state, t, *args)
    k2 = deriv(state + 0.5*dt*k1, t + 0.5*dt, *args)
    k3 = deriv(state + 0.5*dt*k2, t + 0.5*dt, *args)
    k4 = deriv(state + dt*k3, t + dt, *args)
    return state + (dt/6)*(k1 + 2*k2 + 2*k3 + k4)

def simulate(delta, alpha, beta, gamma, omega, T=400, dt=0.005, burn=200):
    n = int(T/dt); state = np.array([0.1, 0.0]); out = np.zeros((n, 2))
    for i in range(n):
        state = rk4(state, i*dt, dt, delta, alpha, beta, gamma, omega)
        out[i] = state
    return out[int(burn/dt):]

def style(ax):
    ax.set_facecolor(BG); ax.tick_params(colors=FG)
    for s in ax.spines.values(): s.set_color(DIM)

# === 1. 相图:周期 vs 混沌 ===
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
traj = simulate(0.3, -1, 1, 0.2, 1.2)
axes[0].plot(traj[:,0], traj[:,1], lw=0.4, color=C_PERIOD)
axes[0].set_title('相图 · 周期 (γ=0.2)', color=FG)
axes[0].set_xlabel('x 位移'); axes[0].set_ylabel('dx/dt 速度')
traj2 = simulate(0.3, -1, 1, 0.5, 1.2)
axes[1].plot(traj2[:,0], traj2[:,1], lw=0.2, color=C_CHAOS, alpha=0.8)
axes[1].set_title('相图 · 混沌 (γ=0.5)', color=FG)
axes[1].set_xlabel('x 位移'); axes[1].set_ylabel('dx/dt 速度')
for ax in axes: style(ax)
fig.patch.set_facecolor(BG)
fig.suptitle('相图:激励幅值 γ 增大导致周期 → 混沌', color=FG, fontsize=13)
fig.tight_layout(); fig.savefig(f'{OUT}/01_phase_portrait.png', facecolor=BG); plt.close(fig)

# === 2. 分岔图 ===
print("计算分岔图...")
gammas = np.linspace(0.20, 0.60, 220)
fig, ax = plt.subplots(figsize=(10, 5))
period = 2*np.pi/1.2; step = int(period/0.005)
for g in gammas:
    tr = simulate(0.3, -1, 1, g, 1.2, T=700, dt=0.005, burn=500)
    pts = tr[::step][:60]
    ax.scatter(np.full(len(pts), g), pts[:,0], s=0.3, c=C_BIF, alpha=0.6)
style(ax)
ax.set_xlabel('γ 激励幅值'); ax.set_ylabel('x (Poincaré 采样)')
ax.set_title('分岔图:γ 增大 → 倍周期分岔 → 混沌(发动机典型失稳路径)', color=FG)
fig.patch.set_facecolor(BG); fig.tight_layout()
fig.savefig(f'{OUT}/02_bifurcation.png', facecolor=BG); plt.close(fig)

# === 3. 庞加莱截面 ===
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
traj = simulate(0.3, -1, 1, 0.2, 1.2, T=3000, dt=0.005, burn=500)
pts = traj[::step]
axes[0].scatter(pts[:,0], pts[:,1], s=10, c=C_PERIOD)
axes[0].set_title('庞加莱截面 · 周期(有限离散点)', color=FG)
traj2 = simulate(0.3, -1, 1, 0.5, 1.2, T=5000, dt=0.005, burn=500)
pts2 = traj2[::step]
axes[1].scatter(pts2[:,0], pts2[:,1], s=1.5, c=C_CHAOS, alpha=0.5)
axes[1].set_title('庞加莱截面 · 混沌(奇异吸引子截面,分形结构)', color=FG)
for ax in axes:
    style(ax); ax.set_xlabel('x'); ax.set_ylabel('dx/dt')
fig.patch.set_facecolor(BG); fig.tight_layout()
fig.savefig(f'{OUT}/03_poincare.png', facecolor=BG); plt.close(fig)

# === 4. 时间响应 ===
fig, axes = plt.subplots(2, 1, figsize=(11, 5))
traj_p = simulate(0.3, -1, 1, 0.2, 1.2, T=120, dt=0.005, burn=0)
tp = np.arange(len(traj_p))*0.005
axes[0].plot(tp, traj_p[:,0], lw=0.8, color=C_PERIOD)
axes[0].set_title('时间响应 · 周期(长期可预测)', color=FG); axes[0].set_ylabel('x')
traj_c = simulate(0.3, -1, 1, 0.5, 1.2, T=120, dt=0.005, burn=0)
tc = np.arange(len(traj_c))*0.005
axes[1].plot(tc, traj_c[:,0], lw=0.8, color=C_CHAOS)
axes[1].set_title('时间响应 · 混沌(长期不可预测,蝴蝶效应)', color=FG)
axes[1].set_ylabel('x'); axes[1].set_xlabel('t 时间')
for ax in axes: style(ax)
fig.patch.set_facecolor(BG); fig.tight_layout()
fig.savefig(f'{OUT}/04_time_series.png', facecolor=BG); plt.close(fig)

# === 5. 最大 Lyapunov 指数 ===
print("计算 Lyapunov 指数...")
def max_lyap(delta, alpha, beta, gamma, omega, T=300, dt=0.01):
    s1 = np.array([0.1, 0.0]); s2 = s1 + 1e-6
    n = int(T/dt); d0 = 1e-6; sum_log = 0; count = 0
    for i in range(n):
        t = i*dt
        s1 = rk4(s1, t, dt, delta, alpha, beta, gamma, omega)
        s2 = rk4(s2, t, dt, delta, alpha, beta, gamma, omega)
        if i % 10 == 0:
            d = np.linalg.norm(s2 - s1)
            if d > 0:
                sum_log += np.log(d/d0); count += 1
                s2 = s1 + d0*(s2-s1)/d
    return sum_log/(count*dt) if count else 0

gs = np.linspace(0.20, 0.55, 28)
lys = [max_lyap(0.3, -1, 1, g, 1.2) for g in gs]
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(gs, lys, 'o-', color=C_LYA, lw=1.5, markersize=4)
ax.axhline(0, color=DIM, ls='--', lw=0.8)
ax.fill_between(gs, 0, lys, where=[l>0 for l in lys], color=C_CHAOS, alpha=0.2, label='混沌区 λ>0')
style(ax)
ax.set_xlabel('γ 激励幅值'); ax.set_ylabel('最大 Lyapunov 指数 λ')
ax.set_title('Lyapunov 指数:λ>0=混沌,λ<0=周期(混沌的定量判据)', color=FG)
ax.legend(facecolor=BG, labelcolor=FG)
fig.patch.set_facecolor(BG); fig.tight_layout()
fig.savefig(f'{OUT}/05_lyapunov.png', facecolor=BG); plt.close(fig)

print("✅ 5 张图生成完毕:")
import os
for f in sorted(os.listdir(OUT)):
    if f.endswith('.png'):
        print(f"  {f}  {os.path.getsize(f'{OUT}/{f}')//1024} KB")
