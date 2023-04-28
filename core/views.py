from rest_framework.views import APIView
from rest_framework import permissions, authentication, status
from rest_framework.response import Response
import numpy as np
import pandas as pd
import scipy.signal as signal
import matplotlib.pyplot as plt

# Create your views here.

class NormalizeView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        ecg_signal = request.data.get("signal")
        fs = 454.54

        # 1. Amplitude scaling (Normalization)
        normalized_signal = (ecg_signal - np.min(ecg_signal)) / (np.max(ecg_signal) - np.min(ecg_signal))

        # 2. Baseline correction (High-pass filter)
        high_pass_filter = signal.butter(2, 0.5, 'highpass', fs=fs)
        baseline_corrected_signal = signal.filtfilt(high_pass_filter[0], high_pass_filter[1], normalized_signal)
        baseline_corrected_signal = baseline_corrected_signal - np.mean(baseline_corrected_signal)

        # 3. Low-pass filter
        low_pass_filter = signal.butter(4, 100, 'lowpass', fs=fs)
        filtered_signal = signal.filtfilt(low_pass_filter[0], low_pass_filter[1], baseline_corrected_signal)

        # 4. Rescale signal to original range
        rescaled_signal = filtered_signal * 2.93
        print(rescaled_signal,"--------------")
        return Response(rescaled_signal)