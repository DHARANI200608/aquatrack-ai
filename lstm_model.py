import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("  WATERBORNE EWS - LSTM FORECASTING")
print("=" * 60)

# LOAD CHOLERA TIME SERIES
print("\nLoading cholera time series data...")
df = pd.read_csv('../data/cholera_timeseries.csv')
print(f"Shape: {df.shape}")
print(df[['Year', 'Cases']].head(10))

# STEP 1: PREPARE DATA
print("\nStep 1: Preparing sequence data...")
scaler = MinMaxScaler()
cases  = df['Cases'].values.reshape(-1, 1)
cases_scaled = scaler.fit_transform(cases)

def create_sequences(data, seq_len=5):
    X, y = [], []
    for i in range(len(data) - seq_len):
        X.append(data[i:i+seq_len])
        y.append(data[i+seq_len])
    return np.array(X), np.array(y)

SEQ_LEN = 5
X, y = create_sequences(cases_scaled, SEQ_LEN)

split   = int(len(X) * 0.8)
X_train = X[:split]
X_test  = X[split:]
y_train = y[:split]
y_test  = y[split:]

print(f"Train sequences: {X_train.shape}")
print(f"Test sequences : {X_test.shape}")

# STEP 2: BUILD LSTM MODEL
print("\nStep 2: Building LSTM model...")
model = Sequential([
    LSTM(64, return_sequences=True, input_shape=(SEQ_LEN, 1)),
    Dropout(0.2),
    LSTM(32, return_sequences=False),
    Dropout(0.2),
    Dense(16, activation='relu'),
    Dense(1)
])
model.compile(optimizer='adam', loss='mse')
model.summary()

# STEP 3: TRAIN MODEL
print("\nStep 3: Training LSTM (takes 2-3 mins)...")
history = model.fit(
    X_train, y_train,
    epochs=100,
    batch_size=4,
    validation_data=(X_test, y_test),
    verbose=1
)

# STEP 4: EVALUATE
print("\nStep 4: Evaluating model...")
y_pred_scaled = model.predict(X_test)
y_pred        = scaler.inverse_transform(y_pred_scaled)
y_actual      = scaler.inverse_transform(y_test)

rmse = np.sqrt(mean_squared_error(y_actual, y_pred))
mae  = mean_absolute_error(y_actual, y_pred)
print(f"RMSE : {rmse:,.0f} cases")
print(f"MAE  : {mae:,.0f} cases")

# STEP 5: ACTUAL VS PREDICTED PLOT
print("\nStep 5: Saving forecast plot...")
plt.figure(figsize=(12, 6))
plt.plot(y_actual, label='Actual Cases',
         color='steelblue', linewidth=2, marker='o')
plt.plot(y_pred,   label='Predicted Cases',
         color='red', linewidth=2, linestyle='--', marker='x')
plt.title('LSTM - Cholera Outbreak Forecast',
          fontsize=16, fontweight='bold')
plt.xlabel('Time Steps')
plt.ylabel('Cases')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('../reports/lstm_forecast.png', dpi=150)
plt.close()
print("Saved: lstm_forecast.png")

# STEP 6: TRAINING LOSS PLOT
print("\nStep 6: Saving training loss plot...")
plt.figure(figsize=(10, 5))
plt.plot(history.history['loss'],
         label='Train Loss', color='steelblue')
plt.plot(history.history['val_loss'],
         label='Val Loss', color='red')
plt.title('LSTM Training Loss', fontsize=16, fontweight='bold')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('../reports/lstm_training_loss.png', dpi=150)
plt.close()
print("Saved: lstm_training_loss.png")

# STEP 7: FUTURE FORECAST
print("\nStep 7: Forecasting next 10 years...")
last_sequence = cases_scaled[-SEQ_LEN:].reshape(1, SEQ_LEN, 1)
future_preds  = []

for i in range(10):
    pred = model.predict(last_sequence, verbose=0)
    future_preds.append(pred[0][0])
    last_sequence = np.append(
        last_sequence[:, 1:, :],
        pred.reshape(1, 1, 1), axis=1)

future_preds = scaler.inverse_transform(
    np.array(future_preds).reshape(-1, 1))

last_year    = int(df['Year'].max())
future_years = list(range(last_year+1, last_year+11))

print("\nNext 10 year forecast:")
for yr, pred in zip(future_years, future_preds):
    print(f"  {yr} : {int(pred[0]):,} predicted cases")

# SAVE FUTURE FORECAST PLOT
plt.figure(figsize=(12, 6))
plt.plot(df['Year'], df['Cases'],
         label='Historical', color='steelblue', linewidth=2)
plt.plot(future_years, future_preds,
         label='Forecast', color='red',
         linewidth=2, linestyle='--', marker='o')
plt.title('LSTM - Cholera 10 Year Forecast',
          fontsize=16, fontweight='bold')
plt.xlabel('Year')
plt.ylabel('Cases')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('../reports/lstm_10year_forecast.png', dpi=150)
plt.close()
print("Saved: lstm_10year_forecast.png")

# STEP 8: SAVE MODEL
print("\nStep 8: Saving LSTM model...")
model.save('../models/lstm_model.h5')
print("Saved: lstm_model.h5")

print("\n" + "=" * 60)
print("  LSTM COMPLETE!")
print(f"  RMSE : {rmse:,.0f} cases")
print(f"  MAE  : {mae:,.0f} cases")
print("  Next: Dashboard - Week 3")
print("=" * 60)