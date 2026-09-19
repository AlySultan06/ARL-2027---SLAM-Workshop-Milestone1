import numpy as np
import Filter_visualizer


class KalmanFilter2D:

    def __init__(
        self,
        gps_measurement_var,
        speedometere_measurement_var,
        position_process_noise,
        velocity_process_noise,
        dt=1,
    ):
        pass

    def predict(self, X_past, P_past, U):
        pass

    def correct(self, X_pred, P_pred, Z):
        pass


if __name__ == "__main__":
    pass
