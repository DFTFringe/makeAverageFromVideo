import pytest
import os
import shutil
import numpy as np
import cv2
from pathlib import Path
from makeAverage import process_video

class TestVideoProcessor:
    @pytest.fixture
    def test_data_dir(self):
        """Fixture to provide test data directory path"""
        return Path("tests/test_data")

    @pytest.fixture
    def expected_output_dir(self):
        """Fixture to provide expected output directory path"""
        return Path("tests/expected_output")

    @pytest.fixture
    def temp_output_dir(self):
        """Fixture to provide temporary output directory path"""
        temp_dir = Path("tests/temp_output")
        # Create temp directory
        temp_dir.mkdir(parents=True, exist_ok=True)
        yield temp_dir
        # Cleanup after test
        shutil.rmtree(temp_dir)

    def compare_images(self, img1_path: Path, img2_path: Path, threshold: float = 0.01) -> bool:
        """
        Compare two images and return True if they are similar enough.

        Args:
            img1_path: Path to first image
            img2_path: Path to second image
            threshold: Maximum allowed average pixel difference (0-1 range)

        Returns:
            bool: True if images are similar enough, False otherwise
        """
        img1 = cv2.imread(str(img1_path))
        img2 = cv2.imread(str(img2_path))

        if img1 is None or img2 is None:
            return False

        if img1.shape != img2.shape:
            return False

        diff = np.abs(img1.astype(np.float32) - img2.astype(np.float32))
        avg_diff = np.mean(diff) / 255.0  # Normalize to 0-1 range

        return avg_diff <= threshold

    def verify_output_files(self, expected_dir: Path, actual_dir: Path) -> bool:
        """
        Verify that all expected files exist and match their counterparts.

        Args:
            expected_dir: Directory containing expected output files
            actual_dir: Directory containing actual output files

        Returns:
            bool: True if all files match, False otherwise
        """
        expected_files = sorted(p.name for p in expected_dir.glob('*.png'))
        actual_files = sorted(p.name for p in actual_dir.glob('*.png'))

        if expected_files != actual_files:
            print(f"File mismatch. Expected: {expected_files}, Got: {actual_files}")
            return False

        for filename in expected_files:
            expected_path = expected_dir / filename
            actual_path = actual_dir / filename

            if not self.compare_images(expected_path, actual_path):
                print(f"Image mismatch for file: {filename}")
                return False

        return True

    def test_blue_channel_processing(self, test_data_dir, expected_output_dir, temp_output_dir):
        """Test processing of blue channel"""
        input_file = test_data_dir / "sample_video.mov"
        process_video(str(input_file), str(temp_output_dir), 0, False)

        assert self.verify_output_files(
            expected_output_dir / "blue_channel",
            temp_output_dir
        )

    def test_with_average_output(self, test_data_dir, expected_output_dir, temp_output_dir):
        """Test processing with average output enabled"""
        input_file = test_data_dir / "sample_video.mov"
        process_video(str(input_file), str(temp_output_dir), 0, True)

        assert self.verify_output_files(
            expected_output_dir / "with_average",
            temp_output_dir
        )

    def test_invalid_input_file(self, temp_output_dir):
        """Test handling of invalid input file"""
        with pytest.raises(ValueError, match="Could not open video file"):
            process_video("nonexistent.mp4", str(temp_output_dir), 0, False)
