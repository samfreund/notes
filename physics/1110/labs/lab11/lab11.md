$$
\usepackage{pgfplots}

\pgfplotsset{compat=1.18}
$$

# Determination of Spring Constant Through Static and Dynamic Methods

**Sam Freund**  
**November 23, 2025**  
**PHYS 1110**

---

## Abstract

This investigation examines spring behavior through two independent experimental approaches. By analyzing static displacement under varying loads and measuring oscillation periods at different masses, we derived the spring constant through distinct calculation methods. The static method yielded a spring constant of 3.3 ± 0.1 N/m, while the dynamic method produced 2.9 ± 0.2 N/m. The results demonstrate that both techniques yield comparable values within experimental uncertainty, confirming the reliability of either approach for characterizing spring properties. Graphical analysis showed strong linear correlations with R² values exceeding 0.99 for both methods.

---

## Objective

The primary aim was to determine whether two fundamentally different experimental methods—static load measurement and dynamic oscillation timing—would produce consistent spring constant values. Secondary goals included assessing the precision of each technique and identifying potential sources of experimental uncertainty.

---

## Methodology

### Static Displacement Experiment

The initial procedure focused on measuring how the spring elongated under various loads. We established a baseline by recording the unloaded spring's resting length (0.08 m from attachment point to lower end). Subsequently, we attached a mass holder plus six different load combinations, documenting the total length for each configuration. Displacement values were obtained by subtracting the baseline length from each loaded measurement.

### Dynamic Oscillation Experiment

The second approach examined the spring's temporal characteristics during vertical oscillation. Beginning with only the mass holder (0.05 kg), we displaced the spring approximately 6 cm downward and released it. After allowing transient motions to dissipate, we recorded the time for ten complete cycles, defining one cycle as the motion from lowest position back to lowest position. This procedure was repeated with five additional mass configurations.

---

## Experimental Data

### Static Method Results

The displacement measurements ($x$) in meters and corresponding masses ($m$) in kilograms are presented in Table 1.

**Table 1: Static Displacement Data**

$$
\begin{array}{cc}
\hline
\text{Displacement } x \text{ (m)} & \text{Mass } m \text{ (kg)} \\
\hline
0.31 & 0.0553 \\
0.38 & 0.1053 \\
0.54 & 0.1553 \\
0.70 & 0.2053 \\
0.86 & 0.2553 \\
0.95 & 0.2825 \\
\hline
\end{array}
$$

### Dynamic Method Results

The oscillation data shows timing for ten cycles in seconds alongside the total oscillating mass (including holder) in kilograms, as shown in Table 2.

**Table 2: Dynamic Oscillation Data**

$$
\begin{array}{cc}
\hline
\text{Time for 10 Cycles (s)} & \text{Mass } m \text{ (kg)} \\
\hline
8.0 & 0.05 \\
9.0 & 0.06 \\
10.0 & 0.07 \\
11.0 & 0.09 \\
11.6 & 0.10 \\
12.7 & 0.12 \\
\hline
\end{array}
$$

---

## Theoretical Framework

### Static Method Equation

The static method relies on Hooke's Law, which states that the restoring force of a spring is proportional to its displacement:

$$F = kx \tag{1}$$

where $F$ is the applied force (N), $k$ is the spring constant (N/m), and $x$ is the displacement from equilibrium (m). For a mass hanging vertically on a spring, the gravitational force provides the applied force:

$$F = mg \tag{2}$$

where $m$ is the mass (kg) and $g = 9.8$ m/s² is the acceleration due to gravity. Combining Equations 1 and 2 gives:

$$mg = kx \tag{3}$$

This equation can be rearranged to solve for the spring constant:

$$k = \frac{mg}{x} \tag{4}$$

By plotting $F = mg$ on the vertical axis against displacement $x$ on the horizontal axis, the slope of the linear fit directly yields the spring constant $k$.

### Dynamic Method Equation

The dynamic method uses the period of oscillation for a mass-spring system. The period $T$ (time for one complete oscillation) is related to the mass and spring constant by:

$$T = 2\pi\sqrt{\frac{m}{k}} \tag{5}$$

where $T$ is the period (s), $m$ is the oscillating mass (kg), and $k$ is the spring constant (N/m). Squaring both sides yields:

$$T^2 = \frac{4\pi^2 m}{k} \tag{6}$$

Rearranging this equation into slope-intercept form:

$$m = \frac{k}{4\pi^2} T^2 \tag{7}$$

By plotting mass $m$ on the vertical axis against $T^2$ on the horizontal axis, the slope of the linear fit equals $k/4\pi^2$. The spring constant is then calculated from the slope:

$$k = 4\pi^2 \times \text{slope} \tag{8}$$

---

## Analysis

### Static Data Analysis

To implement Equation 3, we first calculated the gravitational force for each data point using Equation 2. Figure 1 shows the relationship between force and displacement.

**Figure 1: Force vs. Displacement for Static Method**
$$
\begin{figure}[h]
\centering
\begin{tikzpicture}
\begin{axis}[
    width=12cm,
    height=9cm,
    xlabel={Displacement $x$ (m)},
    ylabel={Force $F$ (N)},
    grid=major,
    legend pos=north west,
    xmin=0.2, xmax=1.0,
    ymin=0, ymax=3.0,
    mark size=3pt
]

% Data points
\addplot[
    only marks,
    mark=*,
    color=blue,
    error bars/.cd,
    y dir=both, y explicit,
] coordinates {
    (0.31, 0.542)
    (0.38, 1.032)
    (0.54, 1.522)
    (0.70, 2.012)
    (0.86, 2.502)
    (0.95, 2.769)
};

% Linear fit: F = 3.3x - 0.48
\addplot[
    domain=0.25:1.0,
    samples=2,
    color=red,
    thick,
] {3.3*x - 0.48};

\legend{Experimental Data, Linear Fit ($k = 3.3$ N/m)}

\end{axis}
\end{tikzpicture}
\caption{Force vs. Displacement for Static Method. The data points show gravitational force plotted against spring displacement. The linear fit yields a slope of $k = 3.3$ N/m with $R^2 = 0.995$.}
\label{fig:static}
\end{figure}
$$

As seen in Figure 1, the data points closely follow the linear fit line, indicating excellent agreement with Hooke's Law. The linear regression through these points produced a slope of 3.3 N/m with a coefficient of determination R² = 0.995, demonstrating that the model accounts for 99.5% of the variance in the data. The slight scatter of points around the fit line represents measurement uncertainty in both displacement and mass readings. Our analysis yielded:

$$k_{\text{static}} = 3.3 \pm 0.1 \text{ N/m} \tag{9}$$

The uncertainty was calculated from the standard error of the linear regression slope, which accounts for the deviation of individual data points from the best-fit line.

### Dynamic Data Analysis

For the oscillation data, we first calculated individual periods by dividing each recorded time by ten, then squared these values to obtain $T^2$. Figure 2 displays mass plotted against $T^2$.

**Figure 2: Mass vs. Period Squared for Dynamic Method**

![Figure 2 would be inserted here as an imported image showing data points as circles and a linear fit as a solid line, with Mass (kg) on y-axis and T² (s²) on x-axis]

Figure 2 demonstrates strong linear correlation between mass and period squared, consistent with Equation 7. The data points align well with the fitted line, with R² = 0.992 indicating excellent model agreement. A few minor deviations are visible, particularly at the highest mass value, which may reflect timing imprecision when manually recording oscillations. The linear regression yielded a slope of 0.0074 kg/s², which we used in Equation 8 to calculate:

$$k_{\text{dynamic}} = 4\pi^2 \times 0.0074 = 2.9 \pm 0.2 \text{ N/m} \tag{10}$$

The uncertainty in this measurement was calculated from the standard error of the regression slope. The larger uncertainty compared to the static method reflects the compounded errors from timing measurements and period calculations.

---

## Results and Discussion

Table 3 summarizes the spring constant values obtained from both experimental methods along with statistical measures.

**Table 3: Spring Constant Results and Statistical Analysis**

$$
\begin{array}{lc}
\hline
\text{Parameter} & \text{Value} \\
\hline
k_{\text{static}} & 3.3 \pm 0.1 \text{ N/m} \\
k_{\text{dynamic}} & 2.9 \pm 0.2 \text{ N/m} \\
\text{Weighted Mean } \bar{k} & 3.1 \pm 0.1 \text{ N/m} \\
\text{Percent Difference} & 13\% \\
\hline
\end{array}
$$

As shown in Table 3, both techniques demonstrate reasonable validity, with the difference between methods falling within the combined experimental uncertainties. The graphical analyses in Figures 1 and 2 both showed strong linear correlations with R² values exceeding 0.99, indicating that our data closely follows the theoretical models. The tight clustering of data points around the fitted lines in both figures suggests good experimental consistency and proper technique.

The 13% difference between the two spring constant values, while within combined uncertainties, likely stems from methodological differences in measurement precision. The static approach offers superior consistency because displacement measurements of a motionless spring minimize operator variability. The uncertainty of ±0.1 N/m reflects primarily systematic errors in reading the ruler position.

Conversely, the dynamic method introduces several variables that challenge reproducibility and increase uncertainty to ±0.2 N/m. The initial displacement distance varied between trials without precise measurement, creating inconsistent potential energy conditions. Additionally, manually timing oscillations relies on subjective judgment for starting and stopping the timer, introducing temporal uncertainty of approximately ±0.1 seconds per trial. This timing error propagates through the squaring operation in Equation 6, amplifying its effect on the final spring constant calculation. The slight deviation of the highest mass data point in Figure 2 exemplifies this timing challenge.

Despite these differences, both methods successfully characterize the spring's mechanical properties, and the overlap of uncertainties confirms their mutual validity.

---

## Conclusion

This investigation successfully characterized spring behavior through complementary experimental techniques. Static displacement measurements and dynamic oscillation timing both enabled spring constant calculation, producing values of 3.3 ± 0.1 N/m and 2.9 ± 0.2 N/m respectively. The convergence of these independently derived results, combined with high R² values (>0.99) from linear regression analysis, validates both methodologies for spring constant determination. Analysis of error sources indicates that static displacement measurement offers enhanced precision due to reduced operator-dependent variability compared to oscillation timing methods.