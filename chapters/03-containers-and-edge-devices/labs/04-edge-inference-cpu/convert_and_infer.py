"""Build, quantize, and benchmark a small TensorFlow Lite model."""

from __future__ import annotations

import os
import time
from pathlib import Path

import numpy as np
import tensorflow as tf


OUTPUT_DIR = Path(
    os.getenv("OUTPUT_DIR", "artifacts")
)


def make_training_data(
    sample_count: int = 1000,
    seed: int = 42,
) -> tuple[np.ndarray, np.ndarray]:
    """Create deterministic classification data."""
    generator = np.random.default_rng(seed)

    features = generator.normal(
        loc=0.0,
        scale=1.0,
        size=(sample_count, 4),
    ).astype(np.float32)

    rule_scores = np.column_stack(
        (
            features[:, 0] - features[:, 1],
            features[:, 2] + features[:, 3],
            -features.sum(axis=1),
        )
    )

    labels = np.argmax(
        rule_scores,
        axis=1,
    ).astype(np.int32)

    return features, labels


def build_model(
    features: np.ndarray,
    labels: np.ndarray,
) -> tf.keras.Model:
    """Train a small neural network classifier."""
    model = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=(4,)),
            tf.keras.layers.Dense(
                8,
                activation="relu",
            ),
            tf.keras.layers.Dense(
                3,
                activation="softmax",
            ),
        ]
    )

    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    model.fit(
        features,
        labels,
        epochs=8,
        batch_size=32,
        verbose=0,
    )

    return model


def save_float_model(
    model: tf.keras.Model,
    output_path: Path,
) -> None:
    """Convert and save a float TensorFlow Lite model."""
    converter = tf.lite.TFLiteConverter.from_keras_model(
        model
    )

    output_path.write_bytes(converter.convert())


def save_dynamic_quantized_model(
    model: tf.keras.Model,
    output_path: Path,
) -> None:
    """Convert and save a dynamically quantized model."""
    converter = tf.lite.TFLiteConverter.from_keras_model(
        model
    )

    converter.optimizations = [
        tf.lite.Optimize.DEFAULT
    ]

    output_path.write_bytes(converter.convert())


def representative_dataset(
    calibration_features: np.ndarray,
):
    """Yield representative samples for integer quantization."""
    for feature_row in calibration_features[:100]:
        yield [
            feature_row.reshape(1, 4).astype(np.float32)
        ]


def save_full_integer_model(
    model: tf.keras.Model,
    calibration_features: np.ndarray,
    output_path: Path,
) -> None:
    """Convert and save a full INT8 model."""
    converter = tf.lite.TFLiteConverter.from_keras_model(
        model
    )

    converter.optimizations = [
        tf.lite.Optimize.DEFAULT
    ]

    converter.representative_dataset = lambda: (
        representative_dataset(calibration_features)
    )

    converter.target_spec.supported_ops = [
        tf.lite.OpsSet.TFLITE_BUILTINS_INT8
    ]

    converter.inference_input_type = tf.int8
    converter.inference_output_type = tf.int8

    output_path.write_bytes(converter.convert())


def quantize_input(
    values: np.ndarray,
    input_details: dict,
) -> np.ndarray:
    """Convert float input into the interpreter input dtype."""
    target_dtype = input_details["dtype"]

    if target_dtype == np.float32:
        return values.astype(np.float32)

    scale, zero_point = input_details["quantization"]

    if scale == 0:
        raise ValueError("Input quantization scale is zero")

    quantized = np.round(
        values / scale + zero_point
    )

    dtype_limits = np.iinfo(target_dtype)

    return np.clip(
        quantized,
        dtype_limits.min,
        dtype_limits.max,
    ).astype(target_dtype)


def dequantize_output(
    values: np.ndarray,
    output_details: dict,
) -> np.ndarray:
    """Convert quantized output back to float values."""
    if output_details["dtype"] == np.float32:
        return values.astype(np.float32)

    scale, zero_point = output_details["quantization"]

    return (
        values.astype(np.float32) - zero_point
    ) * scale


def benchmark_model(
    model_path: Path,
    sample: np.ndarray,
    iterations: int = 100,
) -> tuple[np.ndarray, float]:
    """Run inference and return output and average latency."""
    interpreter = tf.lite.Interpreter(
        model_path=str(model_path)
    )

    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()[0]
    output_details = interpreter.get_output_details()[0]

    prepared_input = quantize_input(
        sample.reshape(1, 4),
        input_details,
    )

    interpreter.set_tensor(
        input_details["index"],
        prepared_input,
    )

    interpreter.invoke()

    start_time = time.perf_counter()

    for _ in range(iterations):
        interpreter.set_tensor(
            input_details["index"],
            prepared_input,
        )
        interpreter.invoke()

    elapsed_seconds = time.perf_counter() - start_time

    raw_output = interpreter.get_tensor(
        output_details["index"]
    )

    output = dequantize_output(
        raw_output,
        output_details,
    )

    average_latency_ms = (
        elapsed_seconds / iterations
    ) * 1000.0

    return output, average_latency_ms


def main() -> None:
    """Train, convert, and benchmark all model formats."""
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    features, labels = make_training_data()
    model = build_model(features, labels)

    model_paths = {
        "float": OUTPUT_DIR / "model-float.tflite",
        "dynamic": OUTPUT_DIR / "model-dynamic.tflite",
        "full-int8": OUTPUT_DIR / "model-full-int8.tflite",
    }

    save_float_model(
        model,
        model_paths["float"],
    )

    save_dynamic_quantized_model(
        model,
        model_paths["dynamic"],
    )

    save_full_integer_model(
        model,
        features,
        model_paths["full-int8"],
    )

    sample = features[0]

    for model_name, model_path in model_paths.items():
        output, latency_ms = benchmark_model(
            model_path,
            sample,
        )

        predicted_class = int(
            np.argmax(output[0])
        )

        print(
            f"{model_name}: "
            f"size={model_path.stat().st_size} bytes, "
            f"latency={latency_ms:.4f} ms, "
            f"class={predicted_class}"
        )


if __name__ == "__main__":
    main()
