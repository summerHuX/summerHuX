import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Default Value
params = {
    "CF": 8400.0,
    "PUB_2022": 660.0,
    "r": 0.1437,
    "E_2030": 36.5,
    "C_2030": 0.30,
    "P_2030": 80.9,
    "P_mid": 35.0,
    "C_low": 0.30,
    "epsilon": 0.0028,
    "Lhighcp": 10.0,
    "VMS_2030": 10.0,
    "ICMS_2030": 210.0,
    "PRIV_2022": 683.0,
    "g": 0.0954,
    "Lhighpub": 0.6,
}

# Calculation
def calculate_values(params):
    PUB_2030 = params["PUB_2022"] * (1 + params["r"])**(2030 - 2022)
    PRIV_2030 = params["PRIV_2022"] * (1 + params["g"])**(2030 - 2022)
    PRIVpub_2030 = PUB_2030 * params["Lhighpub"]
    PRIVdom_2030 = (
        params["E_2030"]
        * params["epsilon"]
        * (
            params["P_2030"] * params["C_2030"] * params["P_2030"]
            + params["P_mid"] * params["C_low"] * params["P_mid"]
        )
        * params["Lhighcp"]
    )
    PRIVvol_2030 = params["VMS_2030"] * params["Lhighcp"]
    PRIVint_2030 = params["ICMS_2030"] * params["Lhighcp"]
    CFG = (
        params["CF"]
        - (
            PUB_2030
            + PRIV_2030
            + PRIVpub_2030
            + PRIVdom_2030
            + PRIVvol_2030
            + PRIVint_2030
        )
    )
    return PUB_2030, PRIV_2030, PRIVpub_2030, PRIVdom_2030, PRIVvol_2030, PRIVint_2030, CFG


# Streamlit UI
st.title("Enhanced Standard Waterfall Chart for Climate Finance Gap")
st.write("Adjust the parameters to calculate finance gap and components.")

# 动态生成用户可调整参数
for param_name, initial_value in params.items():
    min_value = 0.5 * initial_value
    max_value = 1.5 * initial_value
    if min_value == max_value:
        min_value, max_value = 0.0, 1.0

    step_value = 0.01 if isinstance(initial_value, float) else 1
    params[param_name] = st.slider(
        f"Set {param_name}",
        min_value=min_value,
        max_value=max_value,
        value=initial_value,
        step=step_value,
    )

# Results
PUB_2030, PRIV_2030, PRIVpub_2030, PRIVdom_2030, PRIVvol_2030, PRIVint_2030, CFG = calculate_values(params)

# Waterfall figure
categories = [
    "Total Finance Needed (CF)",
    "Public Finance (PUB_2030)",
    "Private Finance (PRIV_2030)",
    "Public Leverage (PRIVpub_2030)",
    "Domestic Carbon Pricing (PRIVdom_2030)",
    "Voluntary Markets (PRIVvol_2030)",
    "International Credits (PRIVint_2030)",
    "Remaining Gap (CFG)",
]
values = [
    params["CF"],  # Total need
    -PUB_2030,  # Negative contribution
    -PRIV_2030,
    -PRIVpub_2030,
    -PRIVdom_2030,
    -PRIVvol_2030,
    -PRIVint_2030,
    CFG,  # Final remaining gap
]

# Start Value
starts = [0]
for i in range(1, len(values)):
    starts.append(starts[-1] + values[i - 1])

# 绘制瀑布图
st.subheader("Enhanced Standard Waterfall Chart")
fig, ax = plt.subplots(figsize=(12, 6))

# Color
colors = [
    "dodgerblue", "lightsalmon", "lightcoral", "gold", "limegreen", "orchid", "deepskyblue", "tomato"
]
for i in range(len(values)):
    ax.bar(
        categories[i],
        values[i],
        bottom=starts[i],
        color=colors[i],
        edgecolor="black",
        width=0.8,
    )

# Label
for i, val in enumerate(values):
    text_color = "white" if abs(val) > 1000 else "black"
    ax.text(
        i,
        starts[i] + values[i] / 2,
        f"{abs(val):.2f}",
        ha="center",
        va="center",
        fontsize=10,
        color=text_color,
    )

# Title
ax.set_title(" Climate Finance Gap", fontsize=16)
ax.set_ylabel("Finance Amount (in billions)", fontsize=12)
ax.set_xticks(range(len(categories)))
ax.set_xticklabels(categories, rotation=45, ha="right", fontsize=10)
ax.set_xlim(-0.5, len(categories) - 0.5)
ax.grid(axis="y", linestyle="--", alpha=0.7)

st.pyplot(fig)
