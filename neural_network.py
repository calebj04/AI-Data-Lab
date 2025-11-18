from sklearn.preprocessing import StandardScaler
import pandas as pd
from tensorflow import keras
from tensorflow.keras import layers

df = pd.read_csv('data/kicker_seasons.csv')

X = df[["season", "kicks_in_season"]].copy()
y = df["lasted_5plus"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Define model
model = keras.Sequential([
    layers.Input(shape=(X_scaled.shape[1],)),
    layers.Dense(16, activation="relu"),
    layers.Dense(8, activation="relu"),
    layers.Dense(1, activation="sigmoid")  # binary output
])

# Compile model
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

# Train the model (you’d need a larger dataset in practice)
model.fit(X_scaled, y, epochs=50, batch_size=4, verbose=1)

# Predict whether each season’s player will last >5 years
predictions = (model.predict(X_scaled) > 0.5).astype(int)

df["predicted_lasted_5plus"] = predictions

