
[] how to get cube template for video using ffmpeg
ffmpeg -i input.mp4 -vf "lut3d=file=cinematic.cube" output.mp4
2. Intel GPU (Quick Sync / QSV)
3. ffmpeg -hwaccel qsv -c:v h264_qsv -i input.mp4 -c:v hevc_qsv -preset slower -global_quality 28 -c:a copy output.mp4
-c:v hevc_qsv → Intel Quick Sync HEVC encoder

-global_quality 28 → quality control (similar to CRF)

-preset slower → better compression.

1. NVIDIA GPU (NVENC – most common)
2. ffmpeg -i input.mp4 -c:v hevc_nvenc -preset slow -cq 28 -c:a copy output.mp4
-c:v hevc_nvenc → use NVIDIA’s HEVC encoder

-preset slow → better compression (choices: default, fast, medium, slow, p1–p7)

-cq 28 → constant quality mode (lower = better quality, larger file)

Much faster than CPU libx265 with good quality.

[]