import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

from Inventory.Inventory_models import InventoryParams
from Inventory.inventory_simulation import InventorySimulation


st.set_page_config(
    page_title="Inventory Policy Analysis",
    layout="wide"
)


st.title("Inventory Policy Analysis")

st.write(
    "Evaluate and compare inventory replenishment policies "
    "under different demand and lead-time conditions."
)


with st.sidebar:

    st.header("Inventory Parameters")

    D = st.number_input(
        "Annual demand (units/year)",
        min_value=1.0,
        value=3650.0,
        step=50.0
    )

    T_total = st.number_input(
        "Simulation period (days)",
        min_value=1,
        value=365,
        step=1
    )

    LD = st.number_input(
        "Supplier lead time (days)",
        min_value=0,
        value=2,
        step=1
    )

    T = st.number_input(
        "Replenishment cycle (days)",
        min_value=1,
        value=5,
        step=1
    )

    Q = st.number_input(
        "Order quantity (units)",
        min_value=0.0,
        value=50.0,
        step=5.0
    )

    initial_ioh = st.number_input(
        "Starting inventory (units)",
        min_value=0.0,
        value=50.0,
        step=5.0
    )

    sigma = st.number_input(
        "Daily demand variability (units/day)",
        min_value=0.0,
        value=2.5,
        step=0.5
    )

    st.divider()

    st.header("Cost Parameters")

    S = st.number_input(
        "Ordering cost per order",
        min_value=0.0,
        value=100.0,
        step=10.0
    )

    H = st.number_input(
        "Annual holding cost per unit",
        min_value=0.0,
        value=2.0,
        step=0.5
    )

    st.divider()

    run = st.button(
        "Run Analysis",
        type="primary",
        use_container_width=True
    )


D_day = D / T_total


st.subheader("Selected Parameters")


col1, col2, col3, col4, col5, col6 = st.columns(6)


col1.metric(
    "Daily Demand",
    f"{D_day:.2f}"
)

col2.metric(
    "Lead Time",
    f"{LD} days"
)

col3.metric(
    "Replenishment Cycle",
    f"{T} days"
)

col4.metric(
    "Order Quantity",
    f"{Q:.0f}"
)

col5.metric(
    "Starting Inventory",
    f"{initial_ioh:.0f}"
)

col6.metric(
    "Demand Variability",
    f"{sigma:.2f}"
)


if run:

    params = InventoryParams(
        D=float(D),
        T_total=int(T_total),
        LD=int(LD),
        T=int(T),
        Q=float(Q),
        initial_ioh=float(initial_ioh),
        sigma=float(sigma),
        S=float(S),
        H=float(H)
    )


    simulation = InventorySimulation(params)


    results = {
        "Basic Periodic Ordering":
            simulation.simulation_1(),

        "Lead-Time-Aware Ordering":
            simulation.simulation_2(),

        "Lead-Time-Adjusted Quantity":
            simulation.simulation_3(),

        "Stochastic Demand":
            simulation.simulation_4(),

        "EOQ-Based Ordering":
            simulation.simulation_5(),

        "Safety Stock + Reorder Point":
            simulation.simulation_6()
    }


    st.divider()

    st.subheader("Policy Comparison")


    fig, axes = plt.subplots(
        3,
        1,
        figsize=(12, 9),
        sharex=True
    )


    for name, result in results.items():

        axes[0].plot(
            result["time"],
            result["demand"],
            label=name
        )

        axes[1].scatter(
            result["time"],
            result["order"],
            label=name,
            s=15
        )

        axes[2].plot(
            result["time"],
            result["inventory_level"],
            label=name
        )


    axes[0].set_title(
        "Demand Comparison"
    )

    axes[0].set_ylabel(
        "Demand"
    )

    axes[0].grid(True)

    axes[0].legend()


    axes[1].set_title(
        "Replenishment Orders"
    )

    axes[1].set_ylabel(
        "Orders"
    )

    axes[1].grid(True)

    axes[1].legend()


    axes[2].set_title(
        "Inventory Level Comparison"
    )

    axes[2].set_ylabel(
        "Inventory"
    )

    axes[2].set_xlabel(
        "Time (Days)"
    )

    axes[2].axhline(
        0,
        linestyle="--",
        label="Zero Inventory"
    )

    axes[2].grid(True)

    axes[2].legend()


    plt.tight_layout()

    st.pyplot(
        fig,
        clear_figure=True,
        use_container_width=True
    )


    st.divider()

    st.subheader(
        "Policy Performance"
    )


    comparison = []


    for name, result in results.items():

        stockout_days = (
            result["inventory_level"] < 0
        ).sum()

        minimum_inventory = (
            result["inventory_level"].min()
        )

        average_inventory = (
            result["inventory_level"].mean()
        )

        comparison.append({

            "Policy": name,

            "Stockout Days":
                int(stockout_days),

            "Minimum Inventory":
                round(
                    minimum_inventory,
                    2
                ),

            "Average Inventory":
                round(
                    average_inventory,
                    2
                )
        })


    comparison_df = pd.DataFrame(
        comparison
    )


    st.dataframe(
        comparison_df,
        use_container_width=True,
        hide_index=True
    )


    st.divider()

    st.subheader(
        "Recommended Policy"
    )


    best_policy = comparison_df.loc[
        comparison_df["Stockout Days"].idxmin(),
        "Policy"
    ]


    best_stockouts = comparison_df[
        "Stockout Days"
    ].min()


    st.success(
        f"{best_policy} has the lowest simulated "
        f"stockout risk with {best_stockouts} stockout days."
    )


    st.divider()

    st.subheader(
        "EOQ and Safety Stock"
    )


    if H > 0:

        Q_eoq = np.sqrt(
            (2 * D * S) / H
        )

        T_eoq = (
            Q_eoq / D_day
        )

    else:

        Q_eoq = 0
        T_eoq = 0


    z = 1.645


    safety_stock = (
        z
        * sigma
        * np.sqrt(LD)
    )


    reorder_point = (
        D_day * LD
        + safety_stock
    )


    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "EOQ",
        f"{Q_eoq:.2f} units"
    )

    col2.metric(
        "EOQ Cycle",
        f"{T_eoq:.2f} days"
    )

    col3.metric(
        "Safety Stock",
        f"{safety_stock:.2f} units"
    )

    col4.metric(
        "Reorder Point",
        f"{reorder_point:.2f} units"
    )


else:

    st.info(
        "Enter your inventory parameters in the sidebar "
        "and click Run Analysis."
    )