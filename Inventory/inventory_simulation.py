import numpy as np
import pandas as pd

from Inventory.Inventory_models import InventoryParams


class InventorySimulation:

    def __init__(self, params: InventoryParams):

        self.D = params.D
        self.T_total = params.T_total
        self.LD = params.LD
        self.T = params.T
        self.Q = params.Q
        self.initial_ioh = params.initial_ioh
        self.sigma = params.sigma
        self.S = params.S
        self.H = params.H

        self.D_day = self.D / self.T_total

        self.sim = pd.DataFrame({
            "time": np.arange(1, self.T_total + 1)
        })


    def order(self, t, T, Q, start_day=1):

        if t > start_day and (t - start_day) % T == 0:
            return Q

        return 0


    def order_leadtime(
        self,
        t,
        T,
        Q,
        LD,
        start_day=1
    ):

        if t > start_day and (
            (t - start_day) + (LD - 1)
        ) % T == 0:

            return Q

        return 0


    def calculate_inventory(self, sim):

        ioh = [self.initial_ioh]

        for t in range(1, len(sim)):

            new_ioh = (
                ioh[-1]
                - sim.loc[t, "demand"]
                + sim.loc[t, "receipt"]
            )

            ioh.append(new_ioh)

        sim["inventory_level"] = ioh

        return sim


    def simulation_1(self):

        sim = self.sim.copy()

        sim["demand"] = self.D_day

        T = int(self.T)
        Q = float(self.Q)
        LD = int(self.LD)

        sim["order"] = sim["time"].apply(
            lambda t: self.order(t, T, Q)
        )

        sim["receipt"] = (
            sim["order"]
            .shift(LD)
            .fillna(0)
        )

        return self.calculate_inventory(sim)


    def simulation_2(self):

        sim = self.sim.copy()

        sim["demand"] = self.D_day

        T = int(self.T)
        Q = float(self.Q)
        LD = int(self.LD)

        sim["order"] = sim["time"].apply(
            lambda t: self.order_leadtime(
                t,
                T,
                Q,
                LD
            )
        )

        sim["receipt"] = (
            sim["order"]
            .shift(LD)
            .fillna(0)
        )

        return self.calculate_inventory(sim)


    def simulation_3(self):

        sim = self.sim.copy()

        sim["demand"] = self.D_day

        T = int(self.T)
        LD = int(self.LD)

        Q_new = (
            self.D_day
            * (T + LD - 1)
        )

        sim["order"] = sim["time"].apply(
            lambda t: self.order(
                t,
                T,
                Q_new
            )
        )

        sim["receipt"] = (
            sim["order"]
            .shift(LD)
            .fillna(0)
        )

        return self.calculate_inventory(sim)


    def simulation_4(self):

        sim = self.sim.copy()

        T = int(self.T)
        Q = float(self.Q)
        LD = int(self.LD)

        np.random.seed(42)

        sim["demand"] = np.random.normal(
            loc=self.D_day,
            scale=self.sigma,
            size=self.T_total
        )

        sim["demand"] = sim["demand"].clip(
            lower=0
        )

        sim["order"] = sim["time"].apply(
            lambda t: self.order_leadtime(
                t,
                T,
                Q,
                LD
            )
        )

        sim["receipt"] = (
            sim["order"]
            .shift(LD)
            .fillna(0)
        )

        return self.calculate_inventory(sim)


    def simulation_5(self):

        sim = self.sim.copy()

        if self.H <= 0:

            raise ValueError(
                "Holding cost H must be greater than zero for EOQ."
            )

        Q_eoq = np.sqrt(
            (2 * self.D * self.S)
            / self.H
        )

        T_eoq = (
            Q_eoq
            / self.D_day
        )

        LD = int(self.LD)

        sim["demand"] = self.D_day

        sim["order"] = sim["time"].apply(
            lambda t: self.order(
                t,
                T_eoq,
                Q_eoq
            )
        )

        sim["receipt"] = (
            sim["order"]
            .shift(LD)
            .fillna(0)
        )

        return self.calculate_inventory(sim)


    def simulation_6(self):

        sim = self.sim.copy()

        T = int(self.T)
        Q = float(self.Q)
        LD = int(self.LD)

        np.random.seed(42)

        sim["demand"] = np.random.normal(
            loc=self.D_day,
            scale=self.sigma,
            size=self.T_total
        )

        sim["demand"] = sim["demand"].clip(
            lower=0
        )

        z = 1.645

        safety_stock = (
            z
            * self.sigma
            * np.sqrt(LD)
        )

        reorder_point = (
            self.D_day * LD
            + safety_stock
        )

        orders = []

        inventory_position = (
            self.initial_ioh
        )

        for t in range(len(sim)):

            if inventory_position <= reorder_point:

                orders.append(Q)

                inventory_position += Q

            else:

                orders.append(0)

            inventory_position -= (
                sim.loc[t, "demand"]
            )

        sim["order"] = orders

        sim["receipt"] = (
            sim["order"]
            .shift(LD)
            .fillna(0)
        )

        sim = self.calculate_inventory(sim)

        sim["safety_stock"] = safety_stock

        sim["reorder_point"] = reorder_point

        return sim