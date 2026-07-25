#!/usr/bin/env python3
"""发动机非线性动力学可视化 - Duffing 振子(叶片/转子振动经典非线性模型)
方程: ẍ + δẋ + αx + βx³ = γcos(ωt)
展示:周期->分岔->混沌 的典型非线性动力学行为
优化版:减少采样点,保证快速生成
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.sans-serif'] = ['PingFang SC', 'Arial Unicode MS', 'Heiti TC', 'sans-serif']
rcParams['axes.unicode_minus'] = False
rcParams['figure.dpi'] = 110

OUT = "/Users/wyf/Desktop/code/document/04-tech/engine_nonlinear_dynamics/images"
BG = '#1e1e2e'; FG = '#cdd6f4'; DIM = '#6c7086'
C_PERIOD = '#1e66f5'; C_CHAOS = '#f38ba8'; C_BIF = '#f9e2af'; C_LYA = '#a6e3a1'

def deriv(x, v, t, delta, alpha, beta, gamma, omega):
    return v, -delta*v - alpha*x - beta*x**3 + gamma*np.cos(omega*t)

def step(x, v, t, dt, *args):
    k1x, k1v = deriv(x, v, t, *args)
    k2x, k2v = deriv(x+0.5*dt*k1x, v+0.5*dt*k1v, t+0.5*dt, *args)
    k3x, k3v = deriv(x+0.5*dt*k2x, v+0.5*dt*k2v, t+0.5*dt, *args)
    k4x, k4v = deriv(x+dt*k3x, v+dt*k3v, t+dt, *args)
    nx = x + (dt/6)*(k1x+2*k2x+2*k3x+k4x)
    nv = v + (dt/6)*(k1v+2*k2v+2*k3v+k4v)
    return nx, nv

def simulate(gamma, T=300, dt=0.01, burn=150, delta=0.3, alpha=-1, beta=1, omega=1.2):
    n = int(T/dt); x, v = 0.1, 0.0
    xs = np.empty(n); vs = np.empty(n)
    for i in range(n):
        x, v = step(x, v, i*dt, dt, delta, alpha, beta, gamma, omega)
        xs[i] = x; vs[i] = v
    b = int(burn/dt)
    return xs[b:], vs[b:]

def style(ax):
    ax.set_facecolor(BG); ax.tick_params(colors=FG)
    for s in ax.spines.values(): s.set_color(DIM)

# === 1. 相图 ===
print("1/5 相图...")
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
xp, vp = simulate(0.2)
axes[0].plot(xp, vp, lw=0.4, color=C_PERIOD)
axes[0].set_title('相图 · 周期 (γ=0.2)', color=FG)
axes[0].set_xlabel('x 位移'); axes[0].set_ylabel('dx/dt 速度')
xc, vc = simulate(0.5)
axes[1].plot(xc, vc, lw=0.2, color=C_CHAOS, alpha=0.8)
axes[1].set_title('相图 · 混沌 (γ=0.5)', color=FG)
axes[1].set_xlabel('x 位移'); axes[1].set_ylabel('dx/dt 速度')
for ax in axes: style(ax)
fig.patch.set_facecolor(BG)
fig.suptitle('相图:激励幅值 γ 增大导致周期 -> 混沌', color=FG, fontsize=13)
fig.tight_layout(); fig.savefig(f'{OUT}/01_phase_portrait.png', facecolor=BG); plt.close(fig)

# === 2. 分岔图 ===
print("2/5 分岔图...")
gammas = np.linspace(0.20, 0.60, 90)
fig, ax = plt.subplots(figsize=(10, 5))
period = 2*np.pi/1.2; step_p = max(1, int(period/0.01))
for g in gammas:
    xs, _ = simulate(g, T=400, dt=0.01, burn=250)
    pts = xs[::step_p][:40]
    ax.scatter(np.full(len(pts), g), pts, s=0.4, c=C_BIF, alpha=0.6)
style(ax)
ax.set_xlabel('γ 激励幅值'); ax.set_ylabel('x (Poincaré 采样)')
ax.set_title('分岔图:γ 增大 -> 倍周期分岔 -> 混沌(发动机典型失稳路径)', color=FG)
fig.patch.set_facecolor(BG); fig.tight_layout()
fig.savefig(f'{OUT}/02_bifurcation.png', facecolor=BG); plt.close(fig)

# === 3. 庞加莱截面 ===
print("3/5 庞加莱截面...")
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
xp, vp = simulate(0.2, T=1500, dt=0.01, burn=300)
pts_p_x = xp[::step_p]; pts_p_v = vp[::step_p]
axes[0].scatter(pts_p_x, pts_p_v, s=10, c=C_PERIOD)
axes[0].set_title('庞加莱截面 · 周期(有限离散点)', color=FG)
xc, vc = simulate(0.5, T=2500, dt=0.01, burn=300)
pts_c_x = xc[::step_p]; pts_c_v = vc[::step_p]
axes[1].scatter(pts_c_x, pts_c_v, s=1.5, c=C_CHAOS, alpha=0.5)
axes[1].set_title('庞加莱截面 · 混沌(奇异吸引子截面,分形结构)', color=FG)
for ax in axes:
    style(ax); ax.set_xlabel('x'); ax.set_ylabel('dx/dt')
fig.patch.set_facecolor(BG); fig.tight_layout()
fig.savefig(f'{OUT}/03_poincare.png', facecolor=BG); plt.close(fig)

# === 4. 时间响应 ===
print("4/5 时间响应...")
fig, axes = plt.subplots(2, 1, figsize=(11, 5))
xp, _ = simulate(0.2, T=80, dt=0.01, burn=0)
tp = np.arange(len(xp))*0.01
axes[0].plot(tp, xp, lw=0.8, color=C_PERIOD)
axes[0].set_title('时间响应 · 周期(长期可预测)', color=FG); axes[0].set_ylabel('x')
xc, _ = simulate(0.5, T=80, dt=0.01, burn=0)
tc = np.arange(len(xc))*0.01
axes[1].plot(tc, xc, lw=0.8, color=C_CHAOS)
axes[1].set_title('时间响应 · 混沌(长期不可预测,蝴蝶效应)', color=FG)
axes[1].set_ylabel('x'); axes[1].set_xlabel('t 时间')
for ax in axes: style(ax)
fig.patch.set_facecolor(BG); fig.tight_layout()
fig.savefig(f'{OUT}/04_time_series.png', facecolor=BG); plt.close(fig)

# === 5. 最大 Lyapunov 指数 ===
print("5/5 Lyapunov 指数...")
def max_lyap(gamma, T=150, dt=0.02, delta=0.3, alpha=-1, beta=1, omega=1.2):
    x1, v1 = 0.1, 0.0; x2, v2 = x1+1e-6, v1
    n = int(T/dt); d0 = 1e-6; s = 0; c = 0
    for i in range(n):
        t = i*dt
        x1, v1 = step(x1, v1, t, dt, delta, alpha, beta, gamma, omega)
        x2, v2 = step(x2, v2, t, dt, delta, alpha, beta, gamma, omega)
        if i % 5 == 0:
            d = np.hypot(x2-x1, v2-v1)
            if d > 0:
                s += np.log(d/d0); c += 1
                x2 = x1 + d0*(x2-x1)/d; v2 = v1 + d0*(v2-v1)/d
    return s/(c*dt) if c else 0

gs = np.linspace(0.20, 0.55, 15)
lys = [max_lyap(g) for g in gs]
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(gs, lys, 'o-', color=C_LYA, lw=1.5, markersize=5)
ax.axhline(0, color=DIM, ls='--', lw=0.8)
ax.fill_between(gs, 0, lys, where=[l>0 for l in lys], color=C_CHAOS, alpha=0.2, label='混沌区 λ>0')
style(ax)
ax.set_xlabel('γ 激励幅值'); ax.set_ylabel('最大 Lyapunov 指数 λ')
ax.set_title('Lyapunov 指数:λ>0=混沌,λ<0=周期(混沌的定量判据)', color=FG)
ax.legend(facecolor=BG, labelcolor=FG)
fig.patch.set_facecolor(BG); fig.tight_layout()
fig.savefig(f'{OUT}/05_lyapunov.png', facecolor=BG); plt.close(fig)

import os
print("\n✅ 5 张图生成完毕:")
for f in sorted(os.listdir(OUT)):
    if f.endswith('.png'):
        print(f"  {f}  {os.path.getsize(f'{OUT}/{f}')//1024} KB")
