# 🚗 SLAM & State Estimation Workshop

Welcome to the **SLAM & State Estimation Workshop!**

For milestone 1, you will build a **Kalman Filter (KF)** from scratch in Python to estimate the trajectory of an autonomous car using noisy **GPS** and **speedometer** sensor readings.

## 🎯 Workshop Objective

Your task is to implement a **Kalman Filter** class that estimates a 4D state vector in a 2D Cartesian plane and visualizes the **prediction**, **measurement**, and **corrected estimate** using the plotting function provided in `Filter_Visualizer.py`.

The state vector is:

$$
\mathbf{x} =
\begin{bmatrix}
p_x \\
p_y \\
v_x \\
v_y
\end{bmatrix}
$$

Where:

* $p_x, p_y$: Vehicle position along the X and Y axes (meters).
* $v_x, v_y$: Vehicle velocity along the X and Y axes (meters/second).

---

## 📐 Mathematical Formulation

### 1. Motion Model — Prediction Step

Assuming constant-velocity kinematics driven by acceleration control inputs:

$$
\mathbf{u}_k =
\begin{bmatrix}
a_x \\
a_y
\end{bmatrix}
$$

The prediction equations are:

$$
\mathbf{x}_k^- = A\mathbf{x}_{k-1} + B\mathbf{u}_k
$$

$$
P_k^- = AP_{k-1}A^T + Q
$$

#### State Transition Matrix

The state transition matrix $A \in \mathbb{R}^{4 \times 4}$ is:

$$
A =
\begin{bmatrix}
1 & 0 & \Delta t & 0 \\
0 & 1 & 0 & \Delta t \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

#### Control Matrix

The control matrix $B \in \mathbb{R}^{4 \times 2}$ is:

$$
B =
\begin{bmatrix}
\frac{1}{2}\Delta t^2 & 0 \\
0 & \frac{1}{2}\Delta t^2 \\
\Delta t & 0 \\
0 & \Delta t
\end{bmatrix}
$$

#### Process Noise Covariance

The Process noise covariance matrix $R \in \mathbb{R}^{4 \times 4}$ is:

$$
Q =
\begin{bmatrix}
\sigma_{\text{posx}}^2 & 0 & 0 & 0 \\
0 & \sigma_{\text{posy}}^2 & 0 & 0 \\
0 & 0 & \sigma_{\text{velx}}^2 & 0 \\
0 & 0 & 0 & \sigma_{\text{vely}}^2
\end{bmatrix}
$$

### 2. Sensor Model — Correction Step

The vehicle receives observations from two sensors:

1. **GPS** — Measures position $(p_x, p_y)$.
2. **Speedometer** — Measures velocity $(v_x, v_y)$.

Together, they form a 4D measurement vector:

$$
\mathbf{z} =
\begin{bmatrix}
z_{p_x} \\
z_{p_y} \\
z_{v_x} \\
z_{v_y}
\end{bmatrix}
$$

The correction step consists of the following equations.

#### Innovation Residual

$$
\mathbf{y}_k = \mathbf{z}_k - H\mathbf{x}_k^-
$$

#### Innovation Covariance

$$
S_k = HP_k^-H^T + R
$$

#### Kalman Gain

$$
K_k = P_k^-H^TS_k^{-1}
$$

#### State Update

$$
\mathbf{x}_k = \mathbf{x}_k^- + K_k\mathbf{y}_k
$$

#### Covariance Update

$$
P_k = (I-K_kH)P_k^-
$$

#### Measurement Matrix

The measurement matrix $H \in \mathbb{R}^{4 \times 4}$ is the identity matrix:

$$
H =
\begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
= I_4
$$



#### Measurement Noise Covariance

The measurement noise covariance matrix $R \in \mathbb{R}^{4 \times 4}$ is:

$$
R =
\begin{bmatrix}
\sigma_{\text{gps}}^2 & 0 & 0 & 0 \\
0 & \sigma_{\text{gps}}^2 & 0 & 0 \\
0 & 0 & \sigma_{\text{speedo}}^2 & 0 \\
0 & 0 & 0 & \sigma_{\text{speedo}}^2
\end{bmatrix}
$$

---

## 📊 Plotting Function

`Filter_Visualizer.py` provides the `plot_1d_gaussians()` function to visualize and compare the **prediction**, **measurement**, and **corrected estimate** for a single state variable.

```python
plot_1d_gaussians(
    x_pred, P_pred,
    z, R,
    x_upd, P_upd,
    state_idx=0,
    label='Position X'
)
```

### Parameters

| Parameter   | Description                              |
| ----------- | ---------------------------------------- |
| `x_pred`    | Predicted state vector from `predict()`. |
| `P_pred`    | Predicted covariance matrix.             |
| `z`         | Sensor measurement vector.               |
| `R`         | Measurement noise covariance matrix.     |
| `x_upd`     | Corrected state vector from `correct()`. |
| `P_upd`     | Corrected covariance matrix.             |
| `state_idx` | Index of the state variable to plot.     |
| `label`     | Name displayed on the plot.              |

### State Indices

The state vector is:

$$
\mathbf{x} =
\begin{bmatrix}
p_x & p_y & v_x & v_y
\end{bmatrix}^T
$$

| `state_idx` | State      |
| ----------: | ---------- |
|         `0` | Position X |
|         `1` | Position Y |
|         `2` | Velocity X |
|         `3` | Velocity Y |



Each plot shows three Gaussian distributions:

* **Prediction**: Estimate before sensor correction.
* **Measurement**: Sensor reading and its uncertainty.
* **Correction**: Final Kalman Filter estimate.

---

## 🛠️ What to do?

Complete the missing sections in `kalman_filter.py`.

### 1- Matrix Initialization

Implement the following matrices inside `__init__()`:

* $A$: State transition matrix
* $B$: Control matrix
* $H$: Measurement matrix
* $Q$: Process noise covariance
* $R$: Measurement noise covariance

> **Important:** Make sure the GPS and speedometer noise variables are assigned to the correct entries in $R$.

### 2- Prediction Step

Complete the `predict()` method to compute:

* Predicted state $\mathbf{x}_{\text{pred}}$
* Predicted covariance $P_{\text{pred}}$

Using:

$$
\mathbf{x}_{\text{pred}} = A\mathbf{x} + B\mathbf{u}
$$

$$
P_{\text{pred}} = APA^T + Q
$$

### 3- Correction Step

Complete the `correct()` method to compute:

* Innovation $\mathbf{y}$
* Innovation covariance $S$
* Kalman gain $K$
* Updated state $\mathbf{x}_{\text{upd}}$
* Updated covariance $P_{\text{upd}}$

Using the correction equations defined above.

### 4- Visualize the Outputs

Run the visualizer using the scenarios below.

For each scenario:

1. Initialize the Kalman Filter using the provided initial state $\mathbf{x}_0$.
2. Configure the appropriate process noise covariance $Q$ and sensor noise covariance $R$.
3. Provide the given measurement vector $\mathbf{z}$.
4. Run one complete Kalman Filter step:

   * Prediction
   * Correction
5. Generate two plots:

   * **Position X**: `state_idx=0`
   * **Velocity X**: `state_idx=2`
6. Compare the prediction, measurement, and corrected distributions with the expected behavior.

---

## 🧪 Scenario Table

| Scenario | State Initializer (`x0`) | Initial Covariance (`P0`) | Control Input (`u`) | Measurement (`z`) | Process Noise (`Q`) | Sensor Noise (`R`) |
|---|---|---|---|---|---|---|
| **1. Noisy Prediction** | `[0, 0, 10, 5]` | **Pos** = 1.0<br>**Vel** = 1.0 | **Ax** = 2.0<br>**Ay** = 1.0 | `[10.5, 5.2, 9.8, 4.9]` | **Pos** = 0.5<br>**Vel** = 1.0 | **GPS** = 4.0<br>**Speedometer** = 3.0 |
| **2. Noisy Measurement** | `[0, 0, 10, 5]` | **Pos** = 1.0<br>**Vel** = 1.0 | **Ax** = 2.0<br>**Ay** = 1.0 | `[10.5, 5.2, 9.8, 4.9]` | **Pos** = 0.05<br>**Vel** = 0.1 | **GPS** = 9.0<br>**Speedometer** = 4.0 |
| **3. GPS Outlier Glitch** | `[0, 0, 10, 5]` | **Pos** = 1.0<br>**Vel** = 1.0 | **Ax** = 2.0<br>**Ay** = 1.0 | `[35.0, 28.0, 10.1, 5.0]` | **Pos** = 0.05<br>**Vel** = 0.1 | **GPS** = 20.0<br>**Speedometer** = 1.0 |
| **4. Cold Start (Docked)** | `[0, 0, 0, 0]` | **Pos** = 0.01<br>**Vel** = 0.01 | **Ax** = 0.0<br>**Ay** = 0.0 | `[0.01, 0.0, 0.0, 0.0]` | **Pos** = 0.001<br>**Vel** = 0.01 | **GPS** = 0.04<br>**Speedometer** = 0.01 |

### 📸 Submission Requirements

For each scenario, generate and submit two plots:

- **Position X**: `state_idx=0`
- **Velocity X**: `state_idx=2`

You should submit **8 plots in total**:

- Scenario 1 → 2 plots
- Scenario 2 → 2 plots
- Scenario 3 → 2 plots
- Scenario 4 → 2 plots

In addition to the plots, submit a **brief PDF report** explaining the results.

### 📄 Report

The report should briefly explain, for each plot:

1. **Prediction**: Describe the predicted Gaussian distribution and how its mean and variance were affected by the initial state, control input, and process noise.
2. **Measurement**: Explain the sensor measurement distribution and how its uncertainty is determined by the sensor noise $R$.
3. **Correction**:  Explain how the Kalman Filter combines the prediction and measurement to produce the corrected estimate.
4. **Parameter Effects**: Discuss how changing the parameters affected the resulting distributions.

The report does not need to contain any mathematical derivations. Focus on **observing and explaining the behavior shown in the plots**.

### 📁 Submission Folder Structure

Your submission should follow this structure:

```text
.
├── kalman_filter.py
├── Images
│   ├── scenario_1_position_x.png
│   ├── scenario_1_velocity_x.png
│   ├── scenario_2_position_x.png
│   ├── scenario_2_velocity_x.png
│   ├── scenario_3_position_x.png
│   ├── scenario_3_velocity_x.png
│   ├── scenario_4_position_x.png
│   └── scenario_4_velocity_x.png
└── Report.pdf
```

---

### 🚀 Getting Started

Install the required Python dependencies:

```bash
pip install numpy matplotlib
```

Then complete the implementation in:

```text
kalman_filter.py
```

Finally, import `Filter_Visualizer.py` and run the required scenarios to generate the plots.
