---
theme: academic

highlighter: shiki
canvasWidth: 980
colorSchema: 'light'
# transition: slide-fade
title: diffusion_schrodinger_bridge
fonts:
  sans: 'Noto Sans SC'
  serif: 'Noto Sans SC'
  mono: 'Cascadia Code'
---

# **Diffusion Schrödinger Bridge**

---

# 大纲

- Motivation
- Methodology
- Results
- Main onclusions

---

# Motivation

背景：

- 计算量
- 找到粒子在两个不同时间的分布下最可能的路径。

---

# Methodology

> 🔰 Trivial 

- 🔰Schrödinger Bridges           （模型）
- 🔰Score-Based Diffusions        （模型）
- 🔰Iterative Proportional Fitting（算法）
- ✅Diffusion Schrödinger Bridge	（算法）

---

# Methodology - Schrödinger Bridges
Schrödinger bridge 和 Static Schrödinger bridge

## 普通的Schrödinger Bridges 

$$
\pi^{\star}=\arg \min \left\{\mathrm{KL}(\pi \mid p): \pi \in \mathscr{P}_{N+1}, \pi_0=p_{\text {data }}, \pi_N=p_{\text {prior }}\right\}
$$

---

# 🔰Methodology - Schrödinger Bridges

## Static Schrödinger Bridge

$$
\pi^{\mathrm{s}, \star}=\arg \min \left\{\mathrm{KL}\left(\pi^{\mathrm{s}} \mid p_{0, N}\right): \pi^{\mathrm{s}} \in \mathscr{P}_2, \pi_0^{\mathrm{s}}=p_{\text {data }}, \pi_N^{\mathrm{s}}=p_{\text {prior }}\right\}
$$

$\pi$与$\pi^{\mathrm{s}}$的主要差别在于：

- $\pi$ 是 $N+1$ 维 （关注了从$0 \cdots N$时刻）
- $\pi^s$ 是 $2$ 维 （只关注 $0$, $N$时刻）

---

# 🔰Methodology - Schrödinger Bridges

## Link with optimal transport

$$
% \begin{equation}

\begin{aligned}
\text{Original:}&\\
\pi^{\mathrm{s}, \star}&=\arg \min \left\{\mathrm{KL}\left(\pi^{\mathrm{s}} \mid p_{0, N}\right): \pi^{\mathrm{s}} \in \mathscr{P}_2, \pi_0^{\mathrm{s}}=p_{\text {data }}, \pi_N^{\mathrm{s}}=p_{\text {prior }}\right\}  \\
\pi^{\mathrm{s}, \star}&=\arg \min \left\{\mathrm{H}(\pi^s,p_{0, N})-\mathrm{H}(\pi^s): \pi^{\mathrm{s}} \in \mathscr{P}_2, \pi_0^{\mathrm{s}}=p_{\text {data }}, \pi_N^{\mathrm{s}}=p_{\text {prior }}\right\} \\
\pi^{\mathrm{s}, \star}&=\arg \min \left\{-\mathbb{E}_{\pi^s}[p_{0, N}]-\mathrm{H}(\pi^s): \pi^{\mathrm{s}} \in \mathscr{P}_2, \pi_0^{\mathrm{s}}=p_{\text {data }}, \pi_N^{\mathrm{s}}=p_{\text {prior }}\right\} \\
(\text{How?})\pi^{\mathrm{s}, \star}&=\arg \min \left\{-\mathbb{E}_{\pi^{\mathrm{s}}}\left[\log p_{N \mid 0}\left(X_N \mid X_0\right)\right]-\mathrm{H}\left(\pi^{\mathrm{s}}\right): \pi^{\mathrm{s}} \in \mathscr{P}_2, \pi_0^{\mathrm{s}}=p_{\text {data }}, \pi_N^{\mathrm{s}}=p_{\text {prior }}\right\}
\end{aligned} 
% \end{equation}
$$

---

# Methodology - Iterative Proportional Fitting (IPF)
这里的记号比较奇怪，和之前不太一样。上标代表的是当前的迭代次数，也就是说迭代n次代表n个“来回”：
$$
\begin{aligned}
\pi^{2 n+1} & =\arg \min \left\{\mathrm{KL}\left(\pi \mid \pi^{2 n}\right): \pi \in \mathscr{P}_{N+1}, \pi_N=p_{\text {prior }}\right\} \\
\pi^{2 n+2} & =\arg \min \left\{\mathrm{KL}\left(\pi \mid \pi^{2 n+1}\right): \pi \in \mathscr{P}_{N+1}, \pi_0=p_{\text {data }}\right\} 
\end{aligned}
$$
已知：
$$
p^0\left(x_{0: N}\right)=p\left(x_{0: N}\right)
$$
向后更新：
$$
q^n\left(x_{0: N}\right)=p_{\text {prior }}\left(x_N\right) \prod_{k=0}^{N-1} p_{k \mid k+1}^n\left(x_k \mid x_{k+1}\right), \text{with }  p_{k \mid k+1}^n\left(x_k \mid x_{k+1}\right)=\frac{p_{k+1 \mid k}^n\left(x_{k+1} \mid x_k\right) p_k^n\left(x_k\right)}{p_{k+1}^n\left(x_{k+1}\right)}
$$
向前更新：
$$
p^{n+1}\left(x_{0: N}\right)=p_{\mathrm{data}}\left(x_0\right) \prod_{k=0}^{N-1} q_{k+1 \mid k}^n\left(x_{k+1} \mid x_k\right), \text{with }q_{k+1 \mid k}^n\left(x_{k+1} \mid x_k\right)=\frac{q_{k \mid k+1}^n\left(x_k \mid x_{k+1}\right) q_{k+1}^n\left(x_{k+1}\right)}{q_k^n\left(x_k\right)}
$$

---

# (Before)Methodology - Diffusion Schrödinger Bridge

有：
$$
% \begin{equation}
\begin{aligned}
  p_{k \mid k+1}\left(x_k \mid x_{k+1}\right)&=\frac{p_k\left(x_k\right) p_{k+1 \mid k}\left(x_{k+1} \mid x_k\right)}{p_{k+1}\left(x_{k+1}\right)} \\
  &=p_{k+1 \mid k}\left(x_{k+1} \mid x_k\right) \frac{p_k\left(x_k\right)}{p_{k+1}\left(x_{k+1}\right)}\\
  &=p_{k+1 \mid k}\left(x_{k+1} \mid x_k\right) \exp \left[\log p_k\left(x_k\right)-\log p_{k+1}\left(x_{k+1}\right)\right]

\end{aligned}  
% \end{equation}
$$

使用泰勒展开：我们对 $\log p_{k+1}$ 在 $x_{k+1}$ 处进行泰勒展开。泰勒展开是:
$$
\log p_{k+1}\left(x_{k+1}\right) \approx \log p_{k+1}\left(x_k\right)+\frac{x_{k+1}-x_k}{1 !} \nabla \log p_{k+1}\left(x_k\right)
$$

代入泰勒展开: 将泰勒展开代入原始公式后并化简：
$$
p_{k \mid k+1}\left(x_k \mid x_{k+1}\right) \approx p_{k+1 \mid k}\left(x_{k+1} \mid x_k\right) \exp \left[\log p_k\left(x_k\right)-\log p_{k+1}\left(x_k\right)-\left(x_{k+1}-x_k\right) \nabla \log p_{k+1}\left(x_k\right)\right]
$$

---

# (Before)Methodology - Diffusion Schrödinger Bridge

同理：
$$
\begin{aligned}
q_{k \mid k+1}^n\left(x_k \mid x_{k+1}\right) & =p_{k+1 \mid k}^n\left(x_{k+1} \mid x_k\right) \exp \left[\log p_k^n\left(x_k\right)-\log p_{k+1}^n\left(x_{k+1}\right)\right] \\
& \approx \mathcal{N}\left(x_k ; x_{k+1}+\gamma_{k+1} b_{k+1}^n\left(x_{k+1}\right), 2 \gamma_{k+1} \mathbf{I}\right)
\end{aligned}
\\
\text{where, } b_{k+1}^n\left(x_{k+1}\right)=-f_k^n\left(x_{k+1}\right)+2 \nabla \log p_{k+1}^n\left(x_{k+1}\right)
$$


---

# Train

## Loss function

$$
\begin{aligned}
 \hat{\ell}_{n, I}^b(\beta)&=M^{-1} \sum_{(k, y) \in I}\left\|B_\beta\left(k+1, X_{k+1}^{\jmath}\right)-\left(X_{k+1}^{\jmath}+F_k^n\left(X_{k+1}^j\right)-F_k^n\left(X_k^{\jmath}\right)\right)\right\|^2 \\
 \hat{\ell}_{n+1, I}^{\jmath}(\alpha)&=M^{-1} \sum_{(k, y) \in I}\left\|F_\alpha\left(k, X_k^{\jmath}\right)-\left(X_k^j+B_{k+1}^n\left(X_{k+1}^j\right)-B_{k+1}^n\left(X_k^{\jmath}\right)\right)\right\|^2 
\end{aligned}
$$