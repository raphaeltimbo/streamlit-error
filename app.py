import streamlit as st
import json
import time

# parameters with name and label
flow_m_units = ["kg/h", "kg/min", "kg/s", "lbm/h", "lbm/min", "lbm/s"]
flow_v_units = ["m³/h", "m³/min", "m³/s"]
flow_units = flow_m_units + flow_v_units
pressure_units = ["bar", "kgf/cm²", "barg", "Pa", "kPa", "MPa", "psi", "mm*H2O*g0"]

parameters_map = {
    "flow": {
        "label": "Flow",
        "units": flow_units,
        "help": "Flow can be mass flow or volumetric flow depending on the selected unit.",
    },
    "discharge_pressure": {
        "label": "Discharge Pressure",
        "units": pressure_units,
    },
    "head": {
        "label": "Head",
        "units": ["kJ/kg", "J/kg", "m*g0", "ft"],
    },
    "eff": {
        "label": "Efficiency",
        "units": [""],
    },
    "power": {
        "label": "Gas Power",
        "units": ["kW", "hp", "W", "Btu/h", "MW"],
    },
}


# with st.expander("Curves", expanded=True):
#     # add upload button for each section curve
#     # check if fig_dict was created when loading state. Otherwise, create it
plot_limits = {}
fig_dict_uploaded = {}

# add button to load state from state.json

if st.button("Load state"):
    with open("session_state.json", "r") as f:
        session_state_data = json.load(f)
    st.session_state.update(session_state_data)


for curve in ["head", "eff", "discharge_pressure", "power"]:
    st.markdown(f"### {parameters_map[curve]['label']}")
    parameter_container = st.container()
    first_section_col, second_section_col = parameter_container.columns(
        2, gap="small"
    )
    plot_limits[curve] = {}
    # create upload button for each section
    for section in ["sec1", "sec2"]:
        plot_limits[curve][section] = {}
        if section == "sec1":
            section_col = first_section_col
        else:
            section_col = second_section_col

        time.sleep(1)

        # add container to x range
        for axis in ["x", "y"]:
            with st.container():
                (
                    plot_limit,
                    units_col,
                    lower_value_col,
                    upper_value_col,
                ) = section_col.columns(4, gap="small")
                plot_limit.markdown(f"{axis} range")
                plot_limits[curve][section][f"{axis}"] = {}
                plot_limits[curve][section][f"{axis}"][
                    "lower_limit"
                ] = lower_value_col.text_input(
                    f"Lower limit",
                    key=f"{axis}_{curve}_{section}_lower",
                    label_visibility="collapsed",
                )

                plot_limits[curve][section][f"{axis}"][
                    "upper_limit"
                ] = upper_value_col.text_input(
                    f"Upper limit",
                    key=f"{axis}_{curve}_{section}_upper",
                    label_visibility="collapsed",
                )

                if axis == "x":
                    plot_limits[curve][section][f"{axis}"][
                        "units"
                    ] = units_col.selectbox(
                        "flow units",
                        options=parameters_map["flow"]["units"],
                        key=f"{axis}_{curve}_{section}_flow_units",
                        label_visibility="collapsed",
                    )
                else:
                    plot_limits[curve][section][f"{axis}"][
                        "units"
                    ] = units_col.selectbox(
                        f"{curve} units",
                        options=parameters_map[curve]["units"],
                        key=f"{axis}_{curve}_{section}_units",
                        label_visibility="collapsed",
                    )
