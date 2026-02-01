from cog import BasePredictor, Input, Path
import subprocess
import tempfile
import os
import re

class Predictor(BasePredictor):
    def predict(self, code: str = Input(description="Manim code"), quality: str = Input(default="medium_quality")) -> Path:
        with tempfile.TemporaryDirectory() as tmpdir:
            script_path = os.path.join(tmpdir, "scene.py")
            with open(script_path, "w") as f:
                f.write(code)
            
            match = re.search(r'class\s+(\w+)\s*\(', code)
            class_name = match.group(1) if match else "Scene"
            
            quality_flags = {"low_quality": "-ql", "medium_quality": "-qm", "high_quality": "-qh"}
            flag = quality_flags.get(quality, "-qm")
            
            subprocess.run(["manim", flag, script_path, class_name, "--media_dir", tmpdir], check=True)
            
            for root, _, files in os.walk(tmpdir):
                for f in files:
                    if f.endswith(".mp4"):
                        return Path(os.path.join(root, f))

