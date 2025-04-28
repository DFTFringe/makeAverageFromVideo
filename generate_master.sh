#!/usr/bin/env bash
rm -rf tests/expected_output/with_average/*
rm -rf tests/expected_output/blue_channel/*
./makeAverage.py --input tests/test_data/sample_video.mov --output_dir tests/expected_output/with_average --select_channel B --output_avg Y
./makeAverage.py --input tests/test_data/sample_video.mov --output_dir tests/expected_output/blue_channel --select_channel B
