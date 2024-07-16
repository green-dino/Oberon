import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
import math
from prettytable import PrettyTable
from utilities.domain_models import GridGeometry2D, Unit


# Input fields for GridGeometry2D
st.header("Create GridGeometry2D")
rows = st.number_input("Rows", min_value=0, value=1)
cols = st.number_input("Columns", min_value=0, value=1)
dx = st.number_input("dx (width of each cell)", min_value=0.0, value=1.0, step=0.1)
dy = st.number_input("dy (height of each cell)", min_value=0.0, value=1.0, step=0.1)

if st.button("Create Grid"):
    try:
        grid = GridGeometry2D(rows, cols, dx, dy)
        st.success("Grid created successfully!")
        st.write(grid)
    except ValueError as e:
        st.error(e)

# Display grid properties
if 'grid' in locals():
    st.subheader("Grid Properties")
    st.write(f"Total Area: {grid.total_area()}")
    st.write(f"Perimeter: {grid.perimeter()}")
    st.write(f"Diagonal Length: {grid.diagonal_length()}")

    # Scale the grid
    scale_factor = st.number_input("Scale Factor", min_value=0.1, value=1.0, step=0.1)
    if st.button("Scale Grid"):
        try:
            grid.scale(scale_factor)
            st.success("Grid scaled successfully!")
            st.write(grid)
        except ValueError as e:
            st.error(e)

    # Serialize and deserialize the grid
    if st.button("Serialize Grid to Dict"):
        grid_dict = grid.to_dict()
        st.json(grid_dict)

    grid_json = st.text_area("Grid JSON", value="", height=200)
    if st.button("Deserialize Grid from Dict"):
        try:
            import json
            grid_data = json.loads(grid_json)
            deserialized_grid = GridGeometry2D.from_dict(grid_data)
            st.success("Grid deserialized successfully!")
            st.write(deserialized_grid)
        except (json.JSONDecodeError, ValueError) as e:
            st.error(e)

# Input fields for Unit
st.header("Create Unit")
unit_name = st.text_input("Unit Name")
if st.button("Create Unit"):
    try:
        unit = Unit(unit_name)
        st.success("Unit created successfully!")
        st.write(unit)
    except ValueError as e:
        st.error(e)


class RiskAssessment:
    DREAD_RISK_CAP = 54
    RISK_LEVELS = {
        (1, 12): "Notice",
        (13, 18): "Low",
        (19, 36): "Medium",
        (37, DREAD_RISK_CAP): "High",
    }

    def __init__(self, damage, reproducibility, exploitability, affected_users, discoverability):
        self.damage = damage
        self.reproducibility = reproducibility
        self.exploitability = exploitability
        self.affected_users = affected_users
        self.discoverability = discoverability
        self.results = {}

    def analyze_data(self):
        # Convert results to a DataFrame for easier analysis
        df = pd.DataFrame({
            "Parameter": ["Damage", "Reproducibility", "Exploitability", "Affected Users", "Discoverability"],
            "Value": [self.damage, self.reproducibility, self.exploitability, self.affected_users, self.discoverability],
            "Risk Value": [self.results.get("Risk Value", None)],
            "Risk Level": [self.results.get("Risk Level", None)]
        })

        # Statistical analysis
        st.subheader("Statistical Analysis")
        st.write(df.describe())

        # Correlation matrix
        st.subheader("Correlation Matrix")
        corr_matrix = df.corr()
        st.write(sns.heatmap(corr_matrix, annot=True, cmap='coolwarm').figure)

        # Distribution of risk levels
        st.subheader("Distribution of Risk Levels")
        risk_levels_df = df[df['Risk Level'].notna()]
        st.write(sns.countplot(x="Risk Level", data=risk_levels_df).figure)

    def calculate_dread_risk(self):
        damage_weight = 0.4
        reproducibility_weight = 0.3
        exploitability_weight = 0.5
        affected_users_weight = 0.01
        discoverability_weight = 0.5

        # Calculate the weighted sum of the parameters using math.prod()
        weighted_sum = math.prod([
            self.damage ** damage_weight,
            self.reproducibility ** reproducibility_weight,
            self.exploitability ** exploitability_weight,
            self.affected_users ** affected_users_weight,
            self.discoverability ** discoverability_weight
        ])

        # Simulate 10,000 random combinations
        risk_values = [
            sum([
                np.random.uniform(0, 10) ** damage_weight,
                np.random.uniform(0, 10) ** reproducibility_weight,
                np.random.uniform(0, 10) ** exploitability_weight,
                np.random.uniform(0, 10) ** affected_users_weight,
                np.random.uniform(0, 10) ** discoverability_weight
            ]) for _ in range(10000)
        ]

        # Calculate the percentile rank of the original risk value within the simulated values
        percentile = np.percentile(risk_values, (weighted_sum / len(risk_values)) * 100)

        # Scale the weighted sum logarithmically to fit within your desired range (0 to DREAD_RISK_CAP)
        scaled_risk_value = min((np.log1p(weighted_sum) / np.log1p(10)) * self.DREAD_RISK_CAP, self.DREAD_RISK_CAP)

        return max(0, scaled_risk_value)

    def determine_risk_level(self, risk_value):
        for (min_range, max_range), level in self.RISK_LEVELS.items():
            if min_range <= risk_value <= max_range:
                return level
        return f"Very High (Risk Value capped at {self.DREAD_RISK_CAP})"

    def assess_risk(self):
        if all(0 <= param <= 10 for param in [self.damage, self.reproducibility, self.exploitability, self.discoverability]) and 0 <= self.affected_users <= 100:
            risk_value = self.calculate_dread_risk()
            risk_level = self.determine_risk_level(risk_value)
            self.results["Risk Value"] = risk_value
            self.results["Risk Level"] = risk_level
            if risk_level == "High":
                self.results["High Risk Actions"] = self.take_actions_for_high_risk()
            return True
        else:
            st.error("Input values must be in the range 0-10 for Damage, Reproducibility, Exploitability, Discoverability, and 0-100 for Affected Users.")
            return False

    def display_results(self):
        parameter_names = ["Damage", "Reproducibility", "Exploitability", "Affected Users", "Discoverability"]
        parameter_values = [self.damage, self.reproducibility, self.exploitability, self.affected_users, self.discoverability]

        # Create a table for display
        table = PrettyTable(["Parameter", "Value"])
        for name, value in zip(parameter_names, parameter_values):
            table.add_row([name, value])

        for key, value in self.results.items():
            table.add_row([key, value])

        st.write("Risk Assessment Results:")
        st.table(table)

    def take_actions_for_high_risk(self):
        return ["Implement immediate mitigation measures.", "Allocate necessary resources to address the issue.", "Conduct a thorough security review"]

def main():
    st.title("Risk Assessment Tool")
    damage = st.slider("Damage (0-10)", 0.0, 10.0, 5.0)
    reproducibility = st.slider("Reproducibility (0-10)", 0.0, 10.0, 5.0)
    exploitability = st.slider("Exploitability (0-10)", 0.0, 10.0, 5.0)
    affected_users = st.slider("Affected Users", 0, 100, 50)
    discoverability = st.slider("Discoverability (0-10)", 0.0, 10.0, 5.0)

    if st.button("Assess Risk"):
        assessment = RiskAssessment(damage, reproducibility, exploitability, affected_users, discoverability)
        if assessment.assess_risk():
            assessment.display_results()
            st.success("Risk assessment completed successfully.")

if __name__ == "__main__":
    main()
