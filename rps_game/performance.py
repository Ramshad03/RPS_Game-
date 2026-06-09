import cv2
import time
import psutil
import os
from gesture import detect_gesture

def measure_performance(duration=10):
    cap = cv2.VideoCapture(0)
    process = psutil.Process(os.getpid())

    frame_times = []
    cpu_usage = []
    ram_usage = []

    print(f"\n📊 Measuring performance for {duration} seconds...")
    print("Show your hand gestures during this time\n")

    start = time.time()

    while time.time() - start < duration:
        frame_start = time.time()

        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        frame, gesture = detect_gesture(frame)

        frame_end = time.time()
        frame_times.append(frame_end - frame_start)
        cpu_usage.append(psutil.cpu_percent())
        ram_usage.append(process.memory_info().rss / 1024 / 1024)

        cv2.putText(frame, f"Gesture: {gesture}", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Performance Test", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    avg_fps = 1 / (sum(frame_times) / len(frame_times))
    avg_cpu = sum(cpu_usage) / len(cpu_usage)
    avg_ram = sum(ram_usage) / len(ram_usage)
    min_fps = 1 / max(frame_times)
    max_fps = 1 / min(frame_times)

    print("=" * 40)
    print("📊 PERFORMANCE REPORT")
    print("=" * 40)
    print(f"Average FPS   : {avg_fps:.1f}")
    print(f"Min FPS       : {min_fps:.1f}")
    print(f"Max FPS       : {max_fps:.1f}")
    print(f"Average CPU   : {avg_cpu:.1f}%")
    print(f"Average RAM   : {avg_ram:.1f} MB")
    print("=" * 40)

    if avg_fps < 15:
        print("⚠️  FPS is LOW — optimization needed")
    elif avg_fps < 25:
        print("🟡 FPS is MODERATE — acceptable")
    else:
        print("✅ FPS is GOOD — no optimization needed")

    if avg_cpu > 70:
        print("⚠️  CPU usage is HIGH — optimization needed")
    else:
        print("✅ CPU usage is NORMAL")

if __name__ == "__main__":
    measure_performance()
    