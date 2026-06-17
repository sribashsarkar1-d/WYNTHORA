import numpy as np

class ARIMAModel:
    """
    A lightweight, custom AutoRegressive (AR) forecasting model.
    Used for stable baseline predictions (like population or GDP growth)
    without relying on heavy external statistical libraries.
    """
    def __init__(self, p=1):
        self.p = p # AutoRegressive order
        self.coefficients = None
        self.intercept = 0.0

    def fit(self, timeseries):
        """
        Fits an AR(p) model using Ordinary Least Squares (OLS).
        """
        N = len(timeseries)
        if N <= self.p:
            raise ValueError("Time series too short for AR(p)")

        # Create X matrix of lagged values and Y vector
        X = np.zeros((N - self.p, self.p + 1))
        Y = np.zeros(N - self.p)

        for i in range(self.p, N):
            X[i - self.p, 0] = 1.0 # Intercept term
            for j in range(self.p):
                X[i - self.p, j + 1] = timeseries[i - 1 - j]
            Y[i - self.p] = timeseries[i]

        # OLS: beta = (X^T * X)^-1 * X^T * Y
        beta = np.linalg.inv(X.T @ X) @ X.T @ Y
        
        self.intercept = beta[0]
        self.coefficients = beta[1:]

    def predict(self, timeseries, steps=5):
        """
        Forecasts future values based on fitted model.
        """
        if self.coefficients is None:
            raise Exception("Model must be fitted before predicting.")

        predictions = []
        history = list(timeseries[-self.p:]) # Get last 'p' elements

        for _ in range(steps):
            next_val = self.intercept
            for j in range(self.p):
                next_val += self.coefficients[j] * history[-(j+1)]
            
            predictions.append(next_val)
            history.append(next_val)

        return predictions
